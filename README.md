# PowerShell Configuration Profile

> [!IMPORTANT]
>
> - Open a terminal on the main root path to execute the commands.
> - Maybe on linux or mac you need to specify your python version.

## Table of Contents

- [PowerShell Configuration Profile](#powershell-configuration-profile)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation (NO ENV)](#installation-no-env)
    - [Install aiohttp](#install-aiohttp)
    - [Usage 1](#usage-1)
    - [Usage 2](#usage-2)
  - [Installation (ENV)](#installation-env)
    - [Create a env](#create-a-env)
    - [Activate env on windows](#activate-env-on-windows)
    - [Activate env on (linux, mac, termux)](#activate-env-on-linux-mac-termux)
    - [Check and upgrade env pip](#check-and-upgrade-env-pip)
    - [Requirements install](#requirements-install)
    - [Usage](#usage)
  - [Format to 'accounts.txt' file](#format-to-accountstxt-file)
    - [First format](#first-format)
    - [Second format](#second-format)
    - [Third format](#third-format)

## Prerequisites

> [!WARNING]
> Tested on latest version of Python (3.12.4).

- Have some version of python installed, making sure you have a custom installation having selected the option 'pip' and 'Add Python x.x to PATH'.

## Installation (NO ENV)

### Install aiohttp

> [!TIP]
> If the installation of aiohttp generates errors, you can try with the stable version tested in ENV option.

```bash
pip install aiohttp
```

### Usage 1

> [!NOTE]
> This method does not need a terminal.

Just double click on 'main.py'.

### Usage 2

- Execute the next command on your terminal.

```bash
python main.py
```

## Installation (ENV)

> [!NOTE]
> The next are terminal commands.

### Create a env

```bash
python -m venv .venv
```

### Activate env on windows

```bash
.\.venv\Scripts\activate
```

### Activate env on (linux, mac, termux)

```bash
source .venv/bin/activate
```

### Check and upgrade env pip

```bash
python -m pip install --upgrade pip
```

### Requirements install

```bash
pip install -U -r requirements.txt
```

### Usage

```bash
python main.py
```

## Format to 'accounts.txt' file

> [!NOTE]
>
> - All formats can be mixed with each other.
> - You can see some other examples on 'accounts.txt' file.

It was decided to make a natural format with the thought of saving this file as a good source of information. So the following examples can be used as a valid one.

### First format

> [!TIP]
> This is the best format to have everything organized.

```text
USERNAME
EMAIL
PASSWORD
```

OR

```text
USERNAME
EMAIL
PASSWORD
OPTIONAL NOTE
```

OR

```text
USERNAME
EMAIL
PASSWORD
OPTIONAL NOTE
WITH MULTIPLE LINES JUST NO LEAVE A BLANK LINE
```

### Second format

> [!NOTE]
> It's not the best format, but it can be used to have basic control of accounts.

```text
USERNAME
PASSWORD
```

### Third format

> [!CAUTION]
> This format is not recommended, use it only if you have forgotten the email and password.

```text
USERNAME
```
