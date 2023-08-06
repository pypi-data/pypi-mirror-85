mkmr-config(7)

# NAME

*mkmr-config* - Configuration for mkmr and utilities

# DESCRIPTION

The *config* file, in ini-format consists of various sections, the sections are
all named after the current directory of where the repo was initialized.

The section can also have a second name (these types of sections will be
referred as *tool-section*), which is the name of one of the tools that mkmr
provides.

sections can have the following options:

- origin -> name of the remote that refers to your fork of the repo
- upstream -> name of the remote that refers to upstream
- remote -> same as upstream, for tools that only deal with upstream

tool-sections can have the following options:

> NOTE: some options only affect certain tools, and options have different
> effects depending on the tool.

- yes (Boolean) Default: False
- quiet (Boolean) Default: False
- edit (Boolean) Default: False
- timeout (Integer) Default: 0
- wait (Integer) Default: 4

## Saving and Writing

All mkmr tools accept the following options to write configuration changes to a
file:

1. *--save*
2. *--write*

*--save* will save the changes to the configuration file and continue with the
normal operation of the tool, *--write* will save the changes to the
configuration and exit.

## Temporary Configuration

All mkmr tools accept --config to point to the directory where the config and
remotes file reside, they will be created if they do not exist

# EXAMPLES

```
[aports]
origin = origin
upstream = upstream

[aports mkmr]
edit = False
yes = True

[aports mgmr]
wait = 6
```

# AUTHORS

Maintained by Leo <thinkabit.ukim@gmail.com>
