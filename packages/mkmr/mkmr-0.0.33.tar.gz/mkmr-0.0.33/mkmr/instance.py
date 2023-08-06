import os
import sys
from optparse import OptionParser
from typing import Optional, Set, Union
from pathlib import Path

from git import Repo
from gitlab import Gitlab

from mkmr.utils import strtobool

from . import __version__

__BIN__ = os.path.basename(sys.argv[0])


def InitOptions() -> OptionParser:
    """Initialize an Options object from Optparse with all the default options that must
    be specified in EVERY program based on mkmr

    Returns:
        Options: object with default options for an mkmr program
    """
    parser = OptionParser(version=__version__)
    parser.add_option(
        "--token",
        dest="token",
        action="store",
        type="string",
        default=None,
        help="GitLab Personal Access Token",
    )
    parser.add_option(
        "-c",
        "--config",
        dest="config",
        action="store",
        type="string",
        default=None,
        help="Full path to configuration directory",
    )
    parser.add_option(
        "--save",
        dest="save",
        action="store_true",
        default=False,
        help="If any value option is passed, save it to configuration",
    )
    parser.add_option(
        "--write",
        dest="write",
        action="store_true",
        default=False,
        help="Write any value option passed to configuration and then exit",
    )
    parser.add_option(
        "--clean-cached-branches",
        dest="clean_branch_cache",
        action="store_true",
        default=False,
        help="Remove branch files that are empty or don't match a local branch",
    )
    parser.add_option(
        "--reset-project-id",
        dest="reset_project_id",
        action="store_true",
        default=False,
        help="Remove project-id cache file (needed if the project changes its internal id)",
    )
    parser.add_option(
        "--timeout",
        dest="timeout",
        action="store",
        type="int",
        default=None,
        help="Set timeout for making calls to the gitlab API",
    )
    return parser


# Helper functions that can only be used in this file
def init_repo(path: Path = None) -> Repo:
    from git import InvalidGitRepositoryError

    # If no path is given to us, assume they want the repo from the
    # current working directory
    if not path:
        path = Path.cwd()

    try:
        repo = Repo(path)
    except InvalidGitRepositoryError:
        if path == Path("/"):
            raise
        return init_repo(path=path.parent)
    else:
        return repo


def create_dir(path: Path) -> Path:
    """Create or re-create a directory with 700 permissions, and its parents

    Args:
        path (Path): full path to the directory to be created

    Returns:
        Path: full path to the directory that was created
    """
    if path.exists() and not path.is_dir():
        path.unlink()

    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path


def create_file(path: Path) -> Path:
    """Create a file or re-creates it with 600 permissions, create parent directories with 700
    permissions

    Args:
        path (Path): full path to the file to be created

    Returns:
        Path: full path to the file that was created
    """
    # Get the parent
    create_dir(path.parent)

    # If the file exists but is not a file then remove
    # it is as well
    if path.exists() and not path.is_file():
        path.unlink()

    # Create it with nice permissions for a file that
    # hold secrets
    path.touch(mode=0o600)
    return path


class Instance:
    """
    Superclass that holds all classes that one needs to interact with mkmr, you can
    instantiante this only once and then call the proper subclass and its members
    """

    class BranchCacheCleaned(Exception):
        """This is raised after the branch cache is cleaned (all dangling references
        and empty files removed), you can catch this and sys.exit(0)
        """

    class BranchNoCache(Exception):
        """This is raised if we ask to clean the branch cache, but it has no cache
        to be cleaned, in this case the user should be told there is nothing to clean
        """

    class BranchNothingCleaned(Exception):
        """This is raised if we ask to clean the branch cache, and we check the files
        in the cache and none of them need to be cleaned, we should tell the user
        that nothing needs to be cleaned or that the cache is already cleaned
        """

    class ProjectIdReset(Exception):
        """This is raised after the project id is reset (project-id file removed),
        you can catch this and sys.exit(0)
        """

    def reset_project_id(self):
        if self.cache.project_id.exists():
            self.cache.project_id.unlink()
        raise self.ProjectIdReset(f"Reset project-id for remote: '{self.remote}'")

    def clean_branch_cache(self):
        from git import GitCommandError
        from os import listdir
        from os.path import getsize

        from mkmr.utils import msg

        # Annotate some variables
        filepath: Path  # Path to the branch cache file
        has_cleaned: bool = False  # If true, we cleaned stuff up
        if not self.cache.branches.is_dir():
            raise self.BranchNoCache(f"No branch cache for remote: '{self.remote}'")
        for branch in listdir(self.cache.branches):
            filepath = self.cache.branches / branch
            # If the files are empty they are of no use to us, just remove them
            if getsize(filepath) == 0:
                msg("removed: {} (empty file)".format(filepath))
                filepath.unlink()
                has_cleaned = True
                continue
            try:
                self.repo.git.rev_parse("--verify", branch)
            except GitCommandError:
                msg("removed: {} (no local branch)".format(filepath))
                filepath.unlink()
                has_cleaned = True
        if has_cleaned:
            raise self.BranchCacheCleaned(
                f"Removed dangling branch references for remote: '{self.remote}'"
            )
        else:
            raise self.BranchNothingCleaned(
                f"Nothing in the cache needs to cleaned for remote: '{self.remote}'"
            )

    def __init__(self, options, origin: bool = False, offline: bool = False):
        """Initialize everything for the Instance object, except if offline=True is passed
        then initialize everything but not what is required to interface with GitLab, we
        allow that for cases where only local operations are done

        Args:
            options (OptParser): Objects with all parsed options we can deal with
            origin (optional): Look at the origin key instead of upstream key. Defaults to False.
            offline (bool, optional): Whether to perform network operations. Defaults to False.
        """
        # Initialize our repo object based on the local repo we have
        try:
            self.repo = init_repo()
        except ValueError:
            raise

        # Initialize the configuration so we get all the important information
        self.config = self.Config(options)

        # Check if 'remote=' was passed to us, if not check if we have options.remote
        # if we have options.remote then check options.remote is not None, if it is None
        # then try to get key from the configuration file and default to upstream if it
        # not found.
        #
        # If there is no options.remote option then try to get the remote from the configuration
        # file, default to origin in that case
        if not origin:
            if hasattr(options, "remote"):
                if options.remote is None:
                    options.remote = self.config.get("upstream")
                    if options.remote is None:
                        options.remote = "upstream"  # Default value
                self.remote = options.remote
            elif hasattr(options, "upstream"):
                if options.upstream is None:
                    options.upstream = self.config.get("upstream")
                    if options.upstream is None:
                        options.upstream = "upstream"  # Default value
                self.remote = options.upstream
        else:
            if options.origin is None:
                options.origin = self.config.get("origin")
                if options.origin is None:
                    options.origin = "origin"  # Default value
            self.remote = options.origin

        # Write down the remote we have, if it doesn't exist in the configuration, or
        # if it exists in the configuration and we were passed --save
        if origin:
            if (
                not self.config.get("origin")
                or self.config.get("origin")
                and (options.save or options.write)
            ):
                self.config.set("origin", options.origin)
        else:
            if hasattr(options, "remote"):
                if (
                    not self.config.get("upstream")
                    or self.config.get("upstream")
                    and (options.save or options.write)
                ):
                    self.config.set("upstream", options.remote)
            elif hasattr(options, "upstream"):
                if (
                    not self.config.get("upstream")
                    or self.config.get("upstream")
                    and (options.save or options.write)
                ):
                    self.config.set("upstream", options.upstream)

        # Write down preferences from the user, this maze allows us to save whatever
        # value is given to us whenever there isn't a value written and when the user
        # passes --save
        if options.timeout is None:
            options.timeout = self.config.getint("timeout", subsection=__BIN__)
            if options.timeout is None:
                options.timeout = 0  # Default value
        elif (options.save or options.write) and self.config.getint(
            "timeout", subsection=__BIN__
        ) != options.timeout:
            self.config.set("timeout", options.timeout, subsection=__BIN__)
        if hasattr(options, "yes"):
            if options.yes is None:
                options.yes = self.config.getboolean("yes", subsection=__BIN__)
                if options.yes is None:
                    options.yes = False  # Default value
            elif (options.save or options.write) and self.config.getboolean(
                "yes", subsection=__BIN__
            ) != options.yes:
                self.config.set("yes", options.yes, subsection=__BIN__)
        if hasattr(options, "quiet"):
            if options.quiet is None:
                options.quiet = self.config.getboolean("quiet", subsection=__BIN__)
                if options.quiet is None:
                    options.quiet = False  # Default value
            elif (options.save or options.write) and self.config.getboolean(
                "quiet", subsection=__BIN__
            ) != options.quiet:
                self.config.set("quiet", options.quiet, subsection=__BIN__)
        if hasattr(options, "edit"):
            if options.edit is None:
                options.edit = self.config.getboolean("edit", subsection=__BIN__)
                if options.edit is None:
                    options.edit = False  # Default value
            elif (options.save or options.write) and self.config.getboolean(
                "edit", subsection=__BIN__
            ) != options.edit:
                self.config.set("edit", options.edit, subsection=__BIN__)
        if hasattr(options, "wait"):
            if options.wait is None:
                options.wait = self.config.getint("wait", subsection=__BIN__)
                if options.wait is None:
                    options.wait = 1  # Default value
            elif (options.save or options.write) and self.config.getint(
                "wait", subsection=__BIN__
            ) != options.wait:
                self.config.set("wait", options.wait, subsection=__BIN__)
        if hasattr(options, "target"):
            if options.target is None:
                options.target = self.config.get("target", subsection=__BIN__)
                if options.target is None:
                    options.target = "master"  # Default value
            elif (options.save or options.write) and self.config.get(
                "target", subsection=__BIN__
            ) != options.target:
                self.config.set("target", options.target, subsection=__BIN__)

        self.api = self.API(self.repo, remote=self.remote)

        self.cache = self.Cache(self.api.domain.replace("/", "."), self.api.user, self.api.project)

        # Now that we have initialized self.api initialize the remotes section of
        # the configuration, as that requires us the domain of the project, this
        # will write down the proper configuration to the remotes file
        self.config.remotes(options, self.api.domain)

        if options.reset_project_id:
            self.reset_project_id()

        if options.clean_branch_cache:
            self.clean_branch_cache()

        # Only run the following code if the user expects us to do operations online
        # if the user is simply passing --clean-cache then there is no reason to
        # perform **potentially** expensive operations like querying the project-id
        # (it can not be cached, even though it is cached aggressively).
        #
        # While the getting of self.gitlab is purely offline there is also the possibility
        # that it will fail and offline operations don't need GitLab.
        if not offline:
            # Start a GitLab configuration by loading from the function get_gitlab()
            # which is defined in the 'config' class
            self.gitlab = Gitlab.from_config(self.api.domain, [self.config.remotes_path])
            # If the user passed --token to us then override the token acquired
            # from private_token
            if options.token:
                self.gitlab.private_token = options.token
            # If the user passed --timeout to us then override the token acquired
            # from timeout or the default value
            if options.timeout:
                self.gitlab.timeout = options.timeout

            # Set the value of projectid from API by calling the load_project_id, which needs
            # to access the Cache object
            self.api.projectid = self.load_project_id()

    class API:
        domain: str  # Domain. Example: gitlab.alpinelinux.org
        projectid: int  # ID of the Project. Example: 1
        user: str  # User of the Project. Example: alpine
        project: str  # Name of the Project. Example: aports

        def __init__(self, repo: Repo, remote: str):
            from giturlparse import parse

            """
            Check that we were given a valid remote
            """
            if remote in repo.remotes:
                uri = repo.remotes[remote].url
            else:
                raise ValueError(
                    "We were passed the remote '{}' which does not exist in the repository".format(
                        remote
                    )
                )

            """
            Parse the url with giturlparse and check what values we got from it
            """
            p = parse(uri)
            self.domain = p.domain

            try:
                "".join(["https://", self.domain])
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no valid URL: {}".format(remote, uri)
                )
            try:
                # Some people have a remote that is
                # git@gitlab.alpinelinux.org:/User/Project.git
                # The / in /User causes problems when using pathlib, so strip it here to avoid any
                # future problems
                if p.owner[0] == "/":
                    p.owner = p.owner[1:]
                self.user = p.owner
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no component owner in its url: '{}'".format(
                        remote, uri
                    )
                )
            try:
                self.project = p.repo
            except AttributeError:
                raise AttributeError(
                    "url from remote '{}' has no repo component in its url: '{}'".format(
                        remote, uri
                    )
                )

    class Config:
        config_path: Path
        remotes_path: Path
        confdir: Path
        section: str

        def get(self, option: str, fallback: str = None, subsection: str = None) -> Optional[str]:
            """Get a value from the configuration file, with an optional fallback

            Args:
                option (str): option to get the value from
                fallback (str, optional): if nothing is found, return this. Defaults to None.

            Returns:
                Optional[str]: value returned, can be either a string or None
            """
            from configparser import ConfigParser

            section = self.section
            if subsection:
                section = section + " " + subsection

            parser = ConfigParser()
            parser.read(self.config_path)

            if not parser.has_section(section) or not parser.has_option(section, option):
                return fallback

            return parser.get(section, option)

        def getboolean(
            self, option: str, fallback: str = None, subsection: str = None
        ) -> Optional[bool]:
            """Same as get, but coerce the value into a boolean, or return None if not there

            Returns:
                Optional[bool]: a boolean coerced from the value of the option, or None if not found
            """
            result = self.get(option, fallback=fallback, subsection=subsection)
            return strtobool(result)

        def getint(
            self, option: str, fallback: str = None, subsection: str = None
        ) -> Optional[int]:
            """Same as get, but coerce the value into an int, or return None if not there, or
            couldn't convert

            Returns:
                Optional[int]: a int coerced from the value of the option, or None if not found or
                badly-formatted value
            """
            result = self.get(option, fallback=fallback, subsection=subsection)
            if result is None:
                return None
            try:
                re = int(result)
            except ValueError:
                return None
            else:
                return re

        def set(self, option: str, value: Union[str, int, bool], subsection: str = None) -> None:
            """Set a value on the configuration file and save it

            Args:
                option (str): Option to put the value in
                value (str): what to put as the value of the option
                subsection (str, Optional): append to section with ' ' as a way to identify uniquely
            """
            from configparser import ConfigParser

            section = self.section
            if subsection:
                section = section + " " + subsection

            parser = ConfigParser()
            parser.read(self.config_path)

            if not parser.has_section(section):
                parser.add_section(section)

            parser[section][option] = str(value)

            with open(self.config_path, "w") as c:
                parser.write(c)

        def __init__(self, options):
            xdgpath: Optional[str]  # Value of XDG_CONFIG_HOME, can be none if unset
            homepath: Optional[str]  # Value of HOME, required if xdgpath is None

            # Store the section of our package in relation to config_path
            # take the name of the directory we are, which in this case
            # is the git repository, so if you're in /usr/src/aports then
            # your section will be 'aports'
            self.section = Path.cwd().name

            if options.config:
                path = Path(options.config)
                self.confdir = create_dir(path)
                self.config_path = create_file(self.confdir / "config")
                self.remotes_path = create_file(self.confdir / "remotes")

            if not options.config:
                xdgpath = os.getenv("XDG_CONFIG_HOME")
                if xdgpath is not None:
                    self.confdir = Path(xdgpath) / "mkmr"
                    self.config_path = create_file(self.confdir / "config")
                    self.remotes_path = create_file(self.confdir / "remotes")

                if xdgpath is None:
                    homepath = os.getenv("HOME")
                    if homepath is None:
                        raise ValueError(
                            "Neither XDG_CONFIG_HOME or HOME are set, please set XDG_CONFIG_HOME"
                        )

                    if xdgpath is None:
                        self.confdir = Path(homepath) / ".mkmr"
                        self.config_path = create_file(self.confdir / "config")
                        self.remotes_path = create_file(self.confdir / "remotes")

            # Keep backwards compatibility by moving 'config' to 'remotes' if there
            # are sections with the options 'url' and 'private_token', those are
            # for usage by python-gitlab for authenticating so they should be in
            # remotes_path
            if self.config_path.stat().st_size > 0 and self.remotes_path.stat().st_size == 0:
                from configparser import ConfigParser

                reader = ConfigParser()
                reader.read(self.config_path)

                for section in reader.sections():
                    opts: Set[str] = set(reader.options(section))
                    if "url" in opts and "private_token" in opts:
                        self.config_path.rename(self.remotes_path)
                        create_file(self.config_path)

        def remotes(self, options, domain: str):
            from configparser import ConfigParser
            from os.path import basename
            from sys import argv

            """
                Write the configuration passed to us via the CLI to the config
                file if it's not there already or the user wants to overwrite it
            """
            parser = ConfigParser()
            parser.read(self.remotes_path)

            if parser.has_section(domain) is False:
                parser.add_section(domain)

            # In case the 'url' options is not set in the section we are looking for
            # then just write it out.
            if parser.has_option(domain, "url") is False:
                parser[domain]["url"] = "https://" + domain

            if not parser.has_option(domain, "private_token"):
                # If --token is not passed to us then drop out with a long useful
                # message, if it is passed to us write it out in the configuration
                # file
                if options.token is None:
                    raise ValueError(
                        "Visit https://"
                        + domain
                        + "/profile/personal_access_tokens to generate your token\n\n"
                        + "Then run {} with --token <TOKEN>".format(basename(argv[0]))
                    )
                else:
                    parser[domain]["private_token"] = options.token

            # Write to configuration only at the end, so we don't have malformed
            # sections in case things fail
            with open(self.remotes_path, "w") as c:
                parser.write(c)

    class Cache:
        # Combination of $domain/$user/$project to separate caches for different
        # projects
        namespace: Path

        cachedir: Path  # Full path to the cache directory
        project_id: Path  # Full path to the project-id file
        branches: Path  # Full path to the branches directory

        # Save the name of a branch after normalizing it
        def save(self, branch: str, value: str):
            # '/' causes errors, normalize it into '-'
            branch = branch.replace("/", "-")
            (self.branches + branch).write_text(value)

        def __init__(self, domain: str, user: str, project: str):
            self.namespace = Path() / domain / user / project

            # Annotate some variables
            xdgpath: Optional[str]  # Value of XDG_CACHE_HOME, can be none if unset
            homepath: Optional[str]  # Value of HOME, required if xdgpath is None

            xdgpath = os.getenv("XDG_CACHE_HOME")
            if xdgpath is not None:
                path = Path(xdgpath)
                self.cachedir = create_dir(path / "mkmr")

            if xdgpath is None:
                homepath = os.getenv("HOME")
                if homepath is None:
                    raise ValueError(
                        "Neither XDG_CACHE_HOME or HOME are set, please set XDG_CACHE_HOME"
                    )

                if homepath is not None:
                    path = Path(homepath)
                    self.cachedir = create_dir(path / ".cache" / "mkmr")

            self.project_id = create_file(self.cachedir / self.namespace / "project-id")
            self.branches = create_dir(self.cachedir / self.namespace / "branches")

    def load_project_id(self) -> int:
        # The path should be, as an example taking alpine/aports from gitlab.alpinelinux.org
        # $XDG_CACHE_HOME/mkmr/gitlab.alpinelinux.org/alpine/aports/project-id
        cachepath = self.cache.project_id
        if cachepath.is_file():
            potential_id: str = cachepath.read_text()
            try:
                self.projectid = int(potential_id)
            except ValueError:
                # We were given a project-id that is not even an integer, it is
                # very clearly wrong, try removing it
                cachepath.unlink()
                # Create a new cachefile that will hold the file and move on
                # to getting it from a request
                create_file(cachepath)
            else:
                return self.projectid
        """
        Call into the gitlab API to get the project id
        """
        from urllib.request import Request, urlopen
        import json

        req = Request(
            self.gitlab.api_url + "/projects/" + self.api.user + "%2F" + self.api.project
        )
        req.add_header("Private-Token", self.gitlab.private_token)
        f = urlopen(req).read()
        j = json.loads(f.decode("utf-8"))
        cachepath.write_text(str(j["id"]))
        self.projectid = j["id"]
        return self.projectid
