mkmr(1)

# NAME

mkmr - Make merge requests to a GitLab instance

# SYNOPSIS

*mkmr* [options]

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

*--target* <TARGET>
	Branch to make the merge request against

*--source* <SOURCE>
	Branch from which to make the merge request

*--origin* <ORIGIN>
	Git remote that points to your fork of the repo

*--upstream* <UPSTREAM>
	Git remote that points to upstream repo

*-e, --edit*
	Open editor to edit the attributes of the merge request

*--no-edit*
	Don't Open editor to edit the attributes of the merge request

*-y, --yes*
	Don't prompt for user confirmation before making merge request

*-a, --ask*
	Prompt for user confirmation before making merge request

*-n, --dry-run*
	Don't make the merge request, just show how it would look like

# DESCRIPTION

mkmr is a python3 script that allows a user to create merge requests to any
GitLab instance.

it makes uses of an ini-format configuration file to store the url of the
instance and the personal access token used to interact with the GitLab API of
the hosted instance. And it uses information stored in the git repository in
the form of remotes to guess which GitLab instance it should interact with.

## Project IDs

Every time one of the utilities needs to interact with a project in GitLab it
needs to know the project id assigned to that project. So instead of making an
API call every time it just stores that in a value in a file within the
following path, with the following name:

```
$domain/$user/$project/project-id
```

As an example if one contributes to alpine/aports from gitlab.alpinelinux.org
the file would be:

```
gitlab.alpinelinux.org/alpine/aports/project-id
```

The content present within the file is the project id

## branch - merge request relation

Every time that a merge request is created with mkmr, a file will be created
in the following location under the mkmr cache directory.

```
$XDG_CACHE_HOME/mkmr/$domain/$user/$project/branches/$source_branch
```

domain is the domain of the hosted GitLab instance, user and project correspond
to the user that owns the project and the name of the project, and branch is
the name of the source branch

The content within the file is the internal id (the one that appears in the
web interface) of the merge request that was made from the source branch.

This is done so programs can directly relate a branch and a merge request
without having to resort to network calls.

# EXAMPLES

The following show examples of how to use the different options that mkmr
provides, note that almost all options can be mixed and match as you please:

## Targeting other branches

```
mkmr --source=FOO --target=BAR
```

## Use another configuration directory

```
mkmr --config=/path/to/temporary/configuration
```

# ALPINE LINUX

mkmr is written by Alpine Linux developers, while it desires to work with all
GitLab instances, as noted by avoiding to hardcode Alpine Linux stuff, mkmr
does offer special support for Alpine Linux handling of GitLab

The following is a write-up of things mkmr does to better integrate with Alpine
Linux:

We automatically add Alpine Linux specific labels like aports:add, aports:move,
aports:upgrade, aports:backport, tag:security and others as appropriate.

We automatically guess the target branch in case your source branch name
matches a specific pattern, namely that it starts with a version number
that matches Alpine Linux's one. As an example, 3.11-dns as a source
branch will lead to mkmr guessing that the user wants to make the merge
request against 3.11-stable.

It will also prefix the title with a version number if one is making
merge requests against one of the branches, merge requests targeting
3.x-stable will have [3.x] prefixed to their title.

# SEE ALSO

*mkmr-config(7)*, *mkmr-remotes(7)*, *mkmr-cache(7)*

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
