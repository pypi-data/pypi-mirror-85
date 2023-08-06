mkmr-remotes(7)

# NAME

*mkmr-remotes* - GitLab remotes database

# DESCRIPTION

The *remotes* file, in ini-format consists of various sections, inside each
section 2 options reside, *url* and *private_token*.

## url

The *url* option's value is a https:// (if your server redirects http to https
then use https://) or http:// followed by the domain of the GitLab Instance.

## private_token

The value of *private_token* is the Personal Access Token that is created from
a GitLab user, it is used for authentication against the GitLab

# PATH

The file (if not overridden with --config), resides in these directories:

- $XDG_CONFIG_HOME/mkmr/remotes (if XDG_CONFIG_HOME is set)
- $HOME/.config/mkmr/remotes (if XDG_CONFIG_HOME is not set)

# EXAMPLES

```
[gitlab.alpinelinux.org]
url = https://gitlab.alpinelinux.org
private_token = XXXXXXXXXXXXXXXXXX
```

# SEE ALSO

*https://python-gitlab.readthedocs.io/en/stable/cli.html#cli-configuration*

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
