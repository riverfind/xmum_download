# xmum_download
xmum_download is a Cli tool for download slides in XMUM moodle.

## Pre-requirement
`fzf` is required. You may check this link https://github.com/junegunn/fzf to download it.
after clone this project, you should execute

For apt user, you may execute follow command
```bash
sudo apt install fzf
```

### Windows

```pwsh
pip install -r requirements.txt
```

### Bash user
execute following command
```bash
chmod +x setup.sh xmum.sh
./setup.sh
```
Setup.sh script will configure all staffs. Just Jump to usage.
## Startup

1. (Windows) Create a pwsh script called 'xmum.ps1' in the same directory of the folder to launch the tool and add it into the environment path
```pwsh
  $basepath = Join-Path -Path $PSScriptRoot -ChildPath "Moodle"
  $activate = Join-Path -Path $basepath -ChildPath ".venv/Scripts/python"
  $main = Join-Path -Path $basepath -ChildPath "main.py"
  &$activate $main @args
```
```

2. Add a .env file
```text
  ac=xxx
  ps=xxx
```
- 'ac' is your account
- 'ps' is your password

## Usage

```pwsh
  xmum cc # will print out the resource of the specific course
  xmum dld # will download the resource of the specific course
```

