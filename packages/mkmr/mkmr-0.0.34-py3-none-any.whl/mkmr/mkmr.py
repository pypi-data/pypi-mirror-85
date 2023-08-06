import sys
from typing import Optional, Dict, List
from copy import deepcopy

import editor
import inquirer
from git import exc
from gitlab import GitlabCreateError

from mkmr.instance import Instance, InitOptions
from mkmr.utils import msg, warn, err


def aports_stable_prefix(str: str) -> Optional[str]:
    """Get version of an alpine stable release by looking at the start of the string

    Args:
        str (str): string to be checked

    Returns:
        Optional[str]: The version number of the release, or None if not version was found
    """
    if str.startswith("3.8-"):
        return "3.8"
    elif str.startswith("3.9-"):
        return "3.9"
    elif str.startswith("3.10-"):
        return "3.10"
    elif str.startswith("3.11-"):
        return "3.11"
    elif str.startswith("3.12-"):
        return "3.12"
    else:
        return None


def main():
    parser = InitOptions()
    parser.add_option(
        "--target",
        dest="target",
        action="store",
        type="string",
        help="Branch to make the merge request against",
    )
    parser.add_option(
        "--source",
        dest="source",
        action="store",
        type="string",
        help="Branch from which to make the merge request",
    )
    parser.add_option(
        "--origin",
        dest="origin",
        action="store",
        type="string",
        help="Git remote that points to your fork of the repo",
    )
    parser.add_option(
        "--upstream",
        dest="upstream",
        action="store",
        type="string",
        help="Git remote that points to upstream repo",
    )
    parser.add_option(
        "-e",
        "--edit",
        dest="edit",
        action="store_true",
        help="Open editor to edit the attributes of the merge request",
    )
    parser.add_option(
        "--no-edit",
        dest="edit",
        action="store_false",
        help="Don't open editor to edit the attributes of the merge request",
    )
    parser.add_option(
        "-y",
        "--yes",
        dest="yes",
        action="store_true",
        help="Don't prompt for user confirmation before making merge request",
    )
    parser.add_option(
        "-a",
        "--ask",
        dest="yes",
        action="store_false",
        help="Prompt for user confirmation before making merge request",
    )
    parser.add_option(
        "-n",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Don't make the merge request, just show how it would look like",
    )
    parser.set_defaults(
        target=None,
        source=None,
        origin=None,
        Upstream=None,
        edit=None,
        yes=None,
        dry_run=False,
    )

    (options, _) = parser.parse_args(sys.argv)

    # Whether we only do offline operations, we don't need any online operations
    # for cleaning cache (first 2 options) or manipulating configuration (options.write)
    offline: bool = False
    if options.clean_branch_cache or options.reset_project_id or options.write:
        offline = True

    try:
        # Deep copy the dictionary so the changes done to it don't affect the next
        # initialization of the remote with already-set values from the previous
        # initialization
        tmp_options = deepcopy(options)
        origin = Instance(tmp_options, origin=True, offline=offline)
    except (ValueError, AttributeError) as e:
        err(e)
        sys.exit(1)
    except (
        Instance.BranchCacheCleaned,
        Instance.BranchNothingCleaned,
        Instance.ProjectIdReset,
    ) as e:
        msg(e)
    except (Instance.BranchNoCache) as e:
        warn(e)
    else:
        # Copy the only value we care about from the options of this remote to the main
        # one that will be used to start the other remote
        options.origin = tmp_options.origin

    try:
        upstream = Instance(options, offline=offline)
    except (ValueError, AttributeError) as e:
        err(e)
        sys.exit(1)
    except (
        Instance.BranchCacheCleaned,
        Instance.BranchNothingCleaned,
        Instance.ProjectIdReset,
    ) as e:
        msg(e)
    except (Instance.BranchNoCache) as e:
        warn(e)

    if offline:
        sys.exit(0)

    # Annotate variables
    source_branch: str  # Branch we are making the merge request from

    aports: bool  # If we are contributing to alpine/aports
    aports_prefix: Optional[str]  # If we are contributing to a stable branch

    if options.source is not None:
        source_branch = options.source
    else:
        source_branch = origin.repo.active_branch.name

    # These are alpine-specific features, check if we are on
    # gitlab.alpinelinux.org and enable them if we have them
    if (
        "gitlab.alpinelinux.org" in upstream.gitlab.url
        and upstream.api.user == "alpine"
        and upstream.api.project == "aports"
    ):
        aports = True
        aports_prefix = aports_stable_prefix(source_branch)
    else:
        aports = False
        aports_prefix = None

    # options.target default to master, if we are in aports try to use the alpine
    # prefix
    if aports_prefix is not None:
        options.target = aports_prefix + "-stable"

    # git pull --rebase the source branch on top of the target branch
    if options.dry_run is False:
        # Check if we are dirty and abort if we are
        if origin.repo.is_dirty():
            err("The repo has untracked files, please commit or stash the changes")
            sys.exit(1)

        # Switch to another branch if we were given --source
        # otherwise we will do a git pull into the wrong branch
        if origin.repo.head.reference != source_branch:
            origin.repo.head.reference = source_branch
            origin.repo.heads[source_branch].checkout()

        try:
            msg(
                "Rebasing {} on top of {}/{}".format(
                    source_branch, options.upstream, options.target
                )
            )
            origin.repo.git.pull("--quiet", options.upstream, "--rebase", options.target)
        except exc.GitCommandError as e:
            # There are multiple reasons that GitCommandError can be raised, try to guess based on
            # the string that is given to us, it would be better if it raised GitCommandError with a
            # specific subtype that would tell us what it is but we can not rely on that
            if "You have unstaged changes" in e.stderr:
                err(
                    "Rebasing {} on top of {}/{} failed!\n There are unstaged changes, please "
                    "commit or stash them".format(source_branch, options.upstream, options.target)
                )
            if "Failed to merge in the changes" in e.stderr:
                err(
                    "Rebasing {} on top of {}/{} failed!\n Please check the output below:\n\n"
                    "{}".format(source_branch, options.upstream, options.target, e.stdout)
                )
            sys.exit(1)
        else:
            msg(
                "Rebased {} on top of {}/{}".format(
                    source_branch, options.upstream, options.target
                )
            )

        try:
            # Overwrite the changes in the upstream branch by force-pushing
            # This is equivalent to:
            #
            # git push --quiet --force origin source_branch
            #
            msg("Pushing {0} to {1}/{0}".format(source_branch, options.origin))
            origin.repo.git.push("--quiet", "--force", options.origin, source_branch)
        except exc.GitCommandError as e:
            err(
                "Failed to push changes from {0} to {1}/{0}. See error below\n{2}".format(
                    source_branch, options.origin, e.stderr
                )
            )
            sys.exit(1)
        else:
            msg("Pushed {0} to {1}/{0}".format(source_branch, options.origin))

    # Annotate variables
    query: str  # Command to check if we have any commits between source and target
    commits: List[str]  # List of commits we have between source and target
    commit_count: int  # Number of commits between source and target

    # Construct the query from $upstream/$target_branch..$source_branch
    query = options.upstream + "/" + options.target
    query = query + ".." + source_branch

    # Turn all the commits given (which with the query command are newline separated)
    # into a list
    commits = list(origin.repo.iter_commits(query))

    # Fail early if we are creating a merge request without commits in difference
    # to the target branch
    commit_count = len(commits)
    if commit_count < 1:
        err("no commits in difference between {}".format(query.replace("..", " and ")))
        sys.exit(1)

    # Annotate commits
    commit_titles: Dict[str, str]  # Dictionary of commit titles to their full description
    labels: Optional[List[str]]  # List of labels of a merge request

    commit_titles = dict()  # Start the empty Dict, we can't update an undefined variable
    for c in commits:
        cstr = getattr(c, "message").partition("\n")
        commit_titles.update([(cstr[0], c)])

    labels = []  # Start the empty List, we can't update an undefined variable

    # Automatically add nice labels to help Alpine Linux
    # reviewers and developers sort out what is important
    if aports is True:
        for s in commit_titles:
            if ": new aport" in s and "aports:add" not in labels:
                labels.append("aports:add")
                continue
            if ": move from " in s and "aports:move" not in labels:
                labels.append("aports:move")
                continue
            if ": upgrade to " in s and "aports:upgrade" not in labels:
                labels.append("aports:upgrade")
                continue
            if (
                ": security upgrade to " in s or ": fix CVE-" in s
            ) and "tag:security" not in labels:
                labels.append("tag:security")
                continue
        if aports_prefix is not None:
            labels.append("aports:backport")
            labels.append("v" + aports_prefix)

    if commit_count == 1:
        commit = list(commit_titles.values())[0]
    else:
        # Annotate some variables
        questions: List[str]  # List of commit titles the user can pick
        answers: Dict[str, str]  # Dictionary with a commit title and its full description

        questions = [
            inquirer.List(
                "commit",
                message="Please pick a commit",
                choices=commit_titles,
                carousel=True,
            ),
        ]
        answers = inquirer.prompt(questions)
        commit = commit_titles[answers["commit"]]

    # Annotate some variables
    message: str  # Full commit title and description
    title: str  # Title of the merge request
    description: str  # Description of the merge request

    message = getattr(commit, "message").splitlines()

    title = message[0]
    if aports_prefix is not None:
        title = "[" + aports_prefix + "] " + title

    # Don't do [1:] because git descriptions have one blank line separating
    # between the title and the description
    description = "\n".join(message[2:])

    if options.edit is True:
        # Annotate some variables
        input: str  # The text we show to the user, a long multiline str

        output: List[str]  # What the user returns to us, but aas a newline-separated list
        output_len: int  # How many newlines there are in the program
        linenum: int  # Counter for which line we are in the List[str] in output

        final_title: Optional[str]  # title given to us by the user
        final_desc: Optional[str]  # description given to us by the user
        final_labels: Optional[List[str]]  # List of labels to be used

        input = "{}\n".format(title)
        input += "\nlabels:"
        if labels:
            input += " {}".format(" ".join(labels))
        input += "\n\n"
        if description.strip() != "":  # Only add description if it is not empty
            input += "{}\n\n".format(description)
        input += "# First line that is not a comment or empty is the title\n"
        input += "#\n"
        input += "# Next line that is not empty or a comment starts the description\n"
        input += "# all following lines are part of the description until the first\n"
        input += "# comment line\n"
        input += "#\n"
        input += "# Any line that starts with 'label: ' and is not between the start\n"
        input += "# and the end of the description denotes the labels, it is separated\n"
        input += "# by whitespace, it can be left empty to not apply any labels\n"
        input += "#\n"
        input += "# If every non-comment line is removed then the values presented above\n"
        input += "# will be used\n"

        # Open in a text editor and let the user fiddle with it, then turn
        # the bytes into str with utf-8 encoding and split everything into
        # a List[str]
        output = editor.edit(contents=input).decode("utf-8").splitlines()
        output_len = len(output)
        linenum = 0

        final_title = None
        final_desc = None
        final_labels = None

        while linenum < output_len:
            if output[linenum].startswith("#") or output[linenum].strip() == "":
                linenum += 1
                continue
            if final_title is None:
                if len(output[linenum]) > 254:
                    warn("The title must be at most 254 characters, keeping old title")
                    final_title = None
                else:
                    final_title = output[linenum]
                linenum += 1
                continue
            if final_labels is None:
                if output[linenum].startswith("labels: "):
                    final_labels = ":".join(output[linenum].split(":")[1:]).strip().split()
                    linenum += 1
                    continue
            if final_desc is None:
                final_desc = "{}".format(output[linenum])
                linenum += 1
                if linenum >= output_len:
                    break  # We need to break here as the description can be a one-liner
                while linenum < output_len and not output[linenum].startswith("#"):
                    final_desc += "\n{}".format(output[linenum])
                    linenum += 1
            linenum += 1

        if final_title is not None:
            title = final_title
        if final_desc is not None:
            if len(final_desc) > 1048575:
                warn("The description must be at most 1048576 characters, keeping old description")
            else:
                description = final_desc
        labels = final_labels

    if options.yes is False or options.dry_run is True:
        print("GitLab Instance:", upstream.gitlab.url)
        print("Source Project:", (origin.api.user + "/" + origin.api.project))
        print("Target Project:", (upstream.api.user + "/" + upstream.api.project))
        print("Source Branch:", source_branch)
        print("Target Branch:", options.target, "\n")

        print("title:", title)
        for line in description.splitlines():
            print("description:", line)
        for line in commit_titles:
            print("commit:", line)
        if labels:
            for line in labels:
                print("label:", line)

        # This is equivalent to git rev-list
        print("commit count:", commit_count)

    # If the user passed --dry-run to us then exit here
    # If the user didn't pass --yes and answered No
    # to the question given to us then exit here
    if options.dry_run is True or (
        not options.yes
        and not inquirer.confirm("Create Merge Request with the values shown above?", default=True)
    ):
        sys.exit(0)

    origin_project = upstream.gitlab.projects.get(
        origin.api.projectid, retry_transient_errors=True, lazy=True
    )

    try:
        mr = origin_project.mergerequests.create(
            {
                "source_branch": source_branch,
                "target_branch": options.target,
                "title": title,
                "description": description,
                "target_project_id": upstream.api.projectid,
                "labels": labels,
                "allow_maintainer_to_push": True,
                "remove_source_branch": True,
            },
            retry_transient_errors=True,
        )
    except GitlabCreateError as e:
        if e.response_code in (403, 409):
            err(
                "Failed to create merge request see below for error message:\n{}".format(
                    e.error_message
                )
            )
            sys.exit(1)

    print("id:", mr.attributes["iid"])
    print("title:", mr.attributes["title"])
    print("state:", mr.attributes["state"])
    print("url:", mr.attributes["web_url"])

    try:
        # This path should be, taking alpine/aports from gitlab.alpinelinux.org as example:
        # $XDG_CACHE_HOME/mkmr/gitlab.alpinelinux.org/alpine/aports/branches/$source_branch
        upstream.cache.save(source_branch, str(mr.attributes["iid"]))
    except ValueError:
        err(
            "Failed to write to cache"
            + ", merging by passing the name of the branch won't be available"
            + "\n{}".format(sys.exc_info()[0])
        )


if __name__ == "__main__":
    main()
