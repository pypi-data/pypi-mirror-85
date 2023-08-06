import sys
from typing import List, Optional

import editor
from gitlab import GitlabAuthenticationError, GitlabUpdateError

from mkmr.instance import Instance, InitOptions
from mkmr.utils import strtobool, msg, warn, err


def main():
    parser = InitOptions()
    parser.add_option(
        "-n",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Show which values would be changed",
    )
    parser.add_option(
        "--remote",
        dest="remote",
        action="store",
        type="string",
        help="Which remote to operate on",
    )
    parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Print only unrecoverable errors",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="quiet",
        action="store_false",
        help="Print recovered errors and warnings",
    )
    parser.set_defaults(
        dry_run=False,
        remote=None,
        quiet=None,
    )

    (options, args) = parser.parse_args(sys.argv)

    # Whether we only do offline operations, we don't need any online operations
    # for cleaning cache (first 2 options) or manipulating configuration (options.write)
    offline: bool = False
    if options.clean_branch_cache or options.reset_project_id or options.write:
        offline = True

    try:
        remote = Instance(options, offline=offline)
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

    if len(args) < 2:
        err("no merge request given")
        sys.exit(1)

    # Annotate some variables
    #
    # A string that corresponds to either an integer that corresponds to the internal-id
    # of the merge request, or the name of a branch, the later can have a branch file that
    # contains the internal-id of the merge request.
    mrnum: str
    iid: int

    mrnum = args[1]

    try:
        # This path should be, taking alpine/aports from gitlab.alpinelinux.org as example:
        # $XDG_CACHE_HOME/mkmr/gitlab.alpinelinux.org/alpine/aports/branches/$source_branch
        cachepath = remote.cache.branches / mrnum.replace("/", "-")
        mrnum = (
            cachepath.read_text()
        )  # Read the file, it should contain the internal-id, can raise FileNotFoundError
        iid = int(mrnum)  # Try converting it to int, it will raise ValueError if it isn't an int
    except ValueError:
        if mrnum.isdigit():
            iid = int(mrnum)
        else:
            err("File has invalid value '{}', it must be an integer".format(cachepath.read_text()))
            cachepath.unlink()  # Delete the file as it has an invalid value
            sys.exit(1)
    except FileNotFoundError:
        # The file isn't there, so assume the user named a branch an integer like '123'
        # but is actually trying to edit a merge request that has internal-id '123'
        if mrnum.isdigit():
            iid = int(mrnum)
        else:
            err(
                "branch name given, {}/branches/{}, has no corresponding cache file".format(
                    remote.cache.namespace, mrnum
                )
            )
            sys.exit(1)

    project = remote.gitlab.projects.get(
        remote.api.projectid, retry_transient_errors=True, lazy=True
    )
    mr = project.mergerequests.get(iid, include_rebase_in_progress=True)

    # Annotate some variables
    discussion_locked: bool  # Whether only team members can comment in the merge request
    input: str  # String the user can edit
    output: List[str]  # 'input' after presented to the user to modify, split by newline
    output_len: int  # number of lines there is in 'output'
    linenum: int  # needle to move which line we are parsing from 'output'

    # Annotate all the final_ variables, they are the result of parsing 'output'
    final_state: Optional[str]
    final_title: Optional[str]
    final_desc: Optional[str]
    final_labels: Optional[List[str]]
    final_remove_branch: Optional[bool]
    final_target_branch: Optional[str]
    final_lock_discussion: Optional[bool]
    final_squash: Optional[bool]
    final_collab: Optional[bool]

    # If discussion isn't locked then the value returned is a None instead of a false like it is
    # normally expected
    discussion_locked = mr.attributes["discussion_locked"]
    if not discussion_locked:
        discussion_locked = False
    else:
        discussion_locked = True

    # The input variable will hold all the values we allow the user to edit,
    # we show all of them to the user in a text editor (they decide it by
    # setting the EDITOR variable) and they modify as they wish, we send
    # them back to be parsed, if any errors are found we tell the user
    # and change the valid changes.
    input = "# Set to 'close' to close the merge request\n"
    input += "# set to 'reopen' to open a closed merge request\n"
    input += "State: {}\n".format(mr.attributes["state"])

    input += "\n# Everything after 'Title: ' is the title of the merge request\n"
    input += "Title: {}\n".format(mr.attributes["title"])

    input += "\n# Any long multi-line string, will consider everything until the first line\n"
    input += "# that starts with a hashtag (#)\n"
    input += "Description: {}\n".format(mr.attributes["description"])

    input += "\n# Whitespace-separated list of labels, have it empty to remove all labels\n"
    input += "Labels: {}\n".format(" ".join(mr.attributes["labels"]).strip())

    input += "\n# If this is true then the source branch of the Merge Request will de deleted\n"
    input += "# when this Merge Request is merged, takes 'true' or 'false'\n"
    input += "Remove source branch when merged: {}\n".format(
        mr.attributes["force_remove_source_branch"]
    )

    input += "\n# Name of the branch the branch the commit will be land on\n"
    input += "Target Branch: {}\n".format(mr.attributes["target_branch"])

    input += "\n# If 'true' then no users can comment, 'false' otherwise\n"
    input += "Lock Discussion: {}\n".format(discussion_locked)

    input += "\n# If 'true' then all commits will be squashed into a single one\n"
    input += "Squash on merge: {}\n".format(mr.attributes["squash"])

    input += "\n# If 'true' maintainers of the repository will be able to push commits\n"
    input += "# into your branch, this is required for people rebasing-and-merging\n"
    input += "Allow Maintainers to push: {}".format(mr.attributes["allow_maintainer_to_push"])

    # This is the result of the edits of the user, and what we will parse to get all the answers
    # we need from what the user edited. Use splitlines() to split it into a list we can walk at
    # the pace we require.
    output = editor.edit(contents=input).decode("utf-8").splitlines()
    output_len = len(output)
    linenum = 0

    final_state = None
    final_title = None
    final_desc = None
    final_labels = None
    final_remove_branch = None
    final_target_branch = None
    final_lock_discussion = None
    final_squash = None
    final_collab = None

    while linenum < output_len:
        if output[linenum].startswith("State: "):
            final_state = ":".join(output[linenum].split(":")[1:]).strip()
            if (
                final_state != mr.attributes["state"]
                and final_state != "close"
                and final_state != "reopen"
            ):
                if not options.quiet:
                    warn(
                        "'State' given must be either 'close' or 'reopen'"
                        + "was given {}, defaulting to {}".format(
                            final_state, mr.attributes["state"]
                        )
                    )
                final_state = mr.attributes["state"]
            linenum += 1
            continue
        if output[linenum].startswith("Title: "):
            final_title = ":".join(output[linenum].split(":")[1:]).strip()
            if len(final_title) >= 255:
                if not options.quiet:
                    warn("The title must be at most 254 characters, keeping old title")
                final_title = mr.attributes["title"]
            if final_title is None or len(final_title) < 1:
                if not options.quiet:
                    warn("The title must be at least 1 character, keeping old title")
                final_title = mr.attributes["title"]
            linenum += 1
            continue
        if output[linenum].startswith("Description: "):
            final_desc = "{}".format(":".join(output[linenum].split(":")[1:]).strip())
            linenum += 1
            while not output[linenum].startswith("#"):
                final_desc += "\n{}".format(output[linenum])
                linenum += 1
            # This value is given to us by the GitLab V4 API and is the hard limit for a description
            if len(final_desc) > 1048575:
                if not options.quiet:
                    warn("Can't change description, it be at most 1048576 characters")
                final_desc = mr.attributes["description"]
            continue
        if output[linenum].startswith("Labels: "):
            final_labels = ":".join(output[linenum].split(":")[1:]).strip().split()
            linenum += 1
            continue
        if output[linenum].startswith("Remove source branch when merged: "):
            final_remove_branch = strtobool(":".join(output[linenum].split(":")[1:]).strip())
            if final_remove_branch is None:
                if not options.quiet:
                    warn("'Remove source branch when merged' value given must be true or false")
                final_remove_branch = mr.attributes["force_remove_source_branch"]
            linenum += 1
            continue
        if output[linenum].startswith("Target Branch: "):
            final_target_branch = ":".join(output[linenum].split(":")[1:]).strip()
            if final_target_branch is None or len(final_target_branch) <= 0:
                if not options.quiet:
                    warn(
                        "Target branch must be at least 1 character long, keeping old target branch"
                    )
                final_target_branch = mr.attributes["target_branch"]
            linenum += 1
            continue
        if output[linenum].startswith("Lock Discussion: "):
            final_lock_discussion = strtobool(":".join(output[linenum].split(":")[1:]).strip())
            if final_lock_discussion is None:
                if not options.quiet:
                    warn("'Lock Discussion' value given must be true or false")
                final_lock_discussion = mr.attributes["discussion_locked"]
            linenum += 1
            continue
        if output[linenum].startswith("Squash on merge: "):
            final_squash = strtobool(":".join(output[linenum].split(":")[1:]).strip())
            if final_squash is None:
                if not options.quiet:
                    warn("'Squash on merge' must be true or false")
                final_squash = mr.attributes["squash"]
            linenum += 1
            continue
        if output[linenum].startswith("Allow Maintainers to push: "):
            final_collab = strtobool(":".join(output[linenum].split(":")[1:]).strip())
            if final_collab is None:
                if not options.quiet:
                    warn("'Allow Maintainers to push' value given must be true or false")
                final_collab = mr.attributes["allow_maintainer_to_push"]
            linenum += 1
            continue
        linenum += 1

    # The state can be one of the three following values:
    # close - closes the merge request, or
    # reopen - opens the merge request again, or
    # the old value, which happens when an invalid state is given to us
    setattr(mr, "state", final_state)

    # The title can be either a valid new title of up to 255 chars, or the old title.
    # The old title happens when an invalid title (len = 0) is given
    setattr(mr, "title", final_title)

    # final_desc will either be the value given to us by the user, or an empty string
    # which is completely valid as having no description is acceptable
    setattr(mr, "description", final_desc)

    # final_labels will either be a List[str] that holds the labels we want. Or it will
    # be None, passing None will remove all labels to the user and is a legitimate action
    setattr(mr, "labels", final_labels)

    # final_remove_branch can be either:
    # - True -> Remove the source branch
    # - False -> Don't remove the source branch
    setattr(mr, "force_remove_source_branch", final_remove_branch)

    # final_target_branch can be either a new value that we can pass to gitlab
    # or the old value, and there is no harming in updating the old value
    setattr(mr, "target_branch", final_target_branch)

    # final_lock_discussion can be either:
    # True -> New comments only by team members
    # False -> All users can be new comments
    setattr(mr, "discussion_locked", final_lock_discussion)

    # final_squash can be either:
    # - True -> Squash commits on merge
    # - False -> Don't squash commits on merge
    setattr(mr, "squash", final_squash)

    # final_collab can be either:
    # - True -> Allow maintainers to push
    # - False -> Don't allow maintainers to push
    setattr(mr, "allow_maintainer_to_push", final_collab)

    if options.dry_run is True:
        print("State:", final_state)
        print("Title:", final_title)
        print("Description:", final_desc)
        print("Labels:", final_labels)
        print("Remove source branch when merged:", final_remove_branch)
        print("Target Branch:", final_target_branch)
        print("Lock Discussion:", final_lock_discussion)
        print("Squash on merge:", final_squash)
        print("Allow Maintainers to push:", final_collab)
        sys.exit(0)

    try:
        mr.save()
    except GitlabAuthenticationError as e:
        err("Failed to update, authentication error\n\n{}".format(e))
    except GitlabUpdateError as e:
        err("Failed to update, update error\n\n{}".format(e))


if __name__ == "__main__":
    main()
