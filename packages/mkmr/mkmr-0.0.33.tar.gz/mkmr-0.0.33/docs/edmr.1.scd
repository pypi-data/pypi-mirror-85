edmr(1)

# NAME

edmr - Programmatically edit attributes of merge requests

# SYNOPSIS

*edmr* [options] <MRNUM> <commands...>

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
	Show which values would be changed but not change them

*-q, --quiet*
	Don't print warnings of invalid values

*-v, --verbose*
	Print warnings of invalid values

*--remote* <REMOTE>
	which remote to operate on

*-l, --list*
	Show list of attributes that can be modified

# DESCRIPTION

edmr is a python3 script that allows an user to edit attributes of the merge
requests that are allowed by the gitlab v4 API.

It can be used programmatically from a shellscript or from the command-line.

it makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

# EXAMPLES

## Setting a title

```
edmr 1000 title="This is a new title"
```

## Appending or Prefixing a title

```
edmr 1000 :title="This comes before"
edmr 1000 title:="This comes after"
```

# SEE ALSO

*mkmr-config(7)*, *mkmr-remotes(7)*, *mkmr-cache(7)*

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
