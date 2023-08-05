# Manage Wine Prefixes

The goal of this tool is to manage Wine prefixes from the command line.

It is a very thin wrapper around Wine commands to make it simple to
manage multiple prefixes and usual commands (winetricks, dxvk).

## Installation

You can install it using PyPI:

    pip install wine-ctl

Or you can run it in-place since it has very few dependencies (you only
need the ansible-roles-ctl script, version.py is only used in the build
process).

You need the following dependencies:
* Wine (any version)
* Python >= 3.6 with the following libraries:
    * pyyaml
    * jsonschema

On Debian systems you can install them using:

    apt install wine64-development wine32-development python3-yaml python3-jsonschema

These are also recommended:

    apt install winetricks dxvk-wine64-development dxvk-wine32-development

You can use the stable version of Wine on Debian too, but if
wine-development is available then it will be preferred.

## Configuration file

The `~/.config/wine-ctl.yml` configuration file is required but very
simple. In fact only `install_path` is needed to know the path of your
Wine prefixes.

If you have a library, for e.g. on GoG, then you can specify the path
(`app_lib_path`) where your downloaded files (with lgogdownloader) are
stored. Then if you create prefixes with the same game directory name it
will reflect on the listing and suggest installers to run at creation
time.

If you wish certain files to be present in your home directory in the
Wine prefix (your Windows home), then you can specify the path of files
to be copied (`home_skel`) when the prefix is created.

You may also wish to define specific environment variables to be set
when running Wine in a prefix. This can be handy to pass parameters for
your driver (RADV\_PERFTEST), libraries (SDL\_VIDEODRIVER, recommend
empty on Wayland at the moment), or tools (DXVK\_\*).

## Usage

Syntax is as follow:

    wine-ctl [global options] [subcommand] [subcommand options]

You can use -h/--help option to list all available options at command
and subcommand level, as well as all available subcommands.

Follows documentation about the various subcommands.

### List

    wine-ctl list

This subcommand display the list of properly setup prefixes. The `L`
flag indicates it is part of your library.

### create

    wine-ctl create <prefix-name>

This subcommand creates a new prefix. You may also specify the `-u`
option if you wish to update an already created prefix.

If you wish to lookup for an installer in your library then use the `-l`
option. The prefix name needs to match the game directory in your
library.

### config

    wine-ctl config <prefix-name>

This subcommand is a shortcut for the winecfg command. It is equivalent
to `wine-ctl run <prefix-name> winecfg`.

### run

    wine-ctl run <prefix-name>

This subcommand runs a command in the prefix. If not specified then a
list of available executables will be presented.

The command can be either a UNIX path (practical to select an installer)
or a command which should be available in the prefix already (like [usual Wine commands: winecfg, winefile, control, wineconsole…](https://wiki.winehq.org/List_of_Commands)).
If you wish to specify command options the you need to quote the
command, for e.g.:

    wine-ctl run <prefix-name> "reg query 'HKEY_CURRENT_USER\Software\Wine\DllOverrides'"

If you need to debug a command with `winecfg` then you can add the
`--debug` option.

### dxvk

    wine-ctl dxvk <prefix-name>

This subcommand is a wrapper to install or uninstall [DXVK](https://github.com/doitsujin/dxvk)
in the prefix.

If run without action then it displays the current installation status.


### trick

    wine-ctl trick <prefix-name>

This subcommand is a wrapper to run [winetricks](https://wiki.winehq.org/Winetricks)
in the prefix.

