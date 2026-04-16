# MLSfetch

Commandline tool designed to search and download MLS data using the 
`earthaccess` API during runtime. This enables quick and easy way to
download MLS data directly from the terminal.

## Installation

This tutorial is aimed to show how to install mlsfetch with uv. If still have not installed uv on 
your machine see tutorial at [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/). To create 
a new environment for this tool, and also install all necessary dependencies uv have one single 
command for this and should be run from the project root:

```bash
uv sync
```

With this command is a virtual environment installed in `.venv`. To activate this you need to know 
which shell you are using. Most likely you are using `zsh` or `bash`. To activate the environment 
run:

```bash
source .venv/bin/activate
```

and if you are using `fish`

```bash
source .venv/bin/activate.fish
```

## Usage

To use this tool you need to have an active account Earth Data account, which is a free account 
that enables you to download NASA data. You can register for it here: [Earth Data Account](https://urs.earthdata.nasa.gov/).

### Login

To login to the account, and start using this tool you simply give the following command:

```bash
mlsfetch login
```

When giving this command will `earthaccess` look for a .netrc file, within your home directory, for login 
credentials. If they are not found it will then look for the same credentials as environment variables in 
your shell. If no credentials is found will `earthaccess` prompt you to type these in.

If you want to save your credentials for further use you can give the optional argument `--persist` when trying
to log in:

```bash
mlsfetch login --persist
```
> [!CAUTION]
> When using `--persist` will a .netrc file be created in your home directory. This file will contain your login
credentials in plain text.

### Search for data

Once logged in you will be greeted with your Earth Data username and a new prompt will appear within 
your active shell. To make a search you simply type *search* followed by the product you want to search
for followed by the year for the collected data. Below you can see an example where I search for Ozone 
data from 2020:

```bash
search O3 2020
```

If you instead would like to search for all available Ozone data replace the year with *__all__*.
To list all the files found in the search type `list` in the prompt

### Download data and exiting

To download the data you first have to search for the data as explained in the section above. To save it 
locally you simply type `download` in the prompt.

> [!CAUTION]
> As currently configured, the data will be downloaded into a directory named *MLS* located in your home directory. 
Please ensure that you do not already have a directory with that name that you wish to preserve. Future versions
of this software will allow users to specify a custom download location.

To exit the software simply type `exit` in the prompt
