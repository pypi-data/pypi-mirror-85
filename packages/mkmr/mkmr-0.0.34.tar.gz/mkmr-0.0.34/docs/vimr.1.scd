vimr(1)

# NAME

vimr - Interactively edit attributes of merge requests like git rebase -i

# SYNOPSIS

*vimr* [options] <MRNUM...>

# OPTIONS

*--version*
	Show version number and quit

*-h, --help*
	Show help message and quit

*--token* <TOKEN>
	GitLab Personal Access Token

*-c, --config* <CONFIG>
	Full path to configuration directory

*--save*
	If any value option is passed, save it to configuration

*--write*
	Write any value option passed to configuration and then exit

*--reset-project-id*
	Remove branch files that are empty or don't match a local branch

*--clean-cached-branches*
	Remove project-id cache file (needed if the project changes its internal id)

*--timeout* <TIMEOUT>
	Set timeout for making calls to the gitlab API

*-n, --dry-run*
	Show which values would be changed

*--remote* <REMOTE>
	Which remote to operate on

*-q, --quiet*
	Print only unrecoverable errors

*-v, --verbose*
	Print recovered errors and warnings

# DESCRIPTION

vimr is a python3 script that allows an user to edit attributes of the merge
requests that are allowed by the gitlab v4 API.

it makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

# SEE ALSO

*mkmr-config(7)*, *mkmr-remotes(7)*, *mkmr-cache(7)*

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
