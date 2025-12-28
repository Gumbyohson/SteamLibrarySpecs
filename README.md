# Getting Python

If you don't already have Python 3.7 or newer installed, you can easily get it using Ninite:

- Go to [https://ninite.com/python-python3-pythonx3/](https://ninite.com/python-python3-pythonx3/)
- Download and run the installer. This will automatically install the latest version of Python 3 for you, with no extra toolbars or adware.

After installation, you may need to restart your terminal or computer for the `python` command to become available.
# SteamLibrarySpecs

SteamLibrarySpecs is a command-line tool that checks your Steam library games against your PC's hardware specifications. It fetches system requirements for each game from the Steam Store and compares them to your detected CPU, GPU, RAM, and disk space, providing a summary of which games your system can run.

## Features
- Automatically detects your PC's CPU, GPU, RAM, and disk space
- Fetches minimum and recommended requirements for each game in your Steam library
- Compares your specs to each game's requirements and highlights unmet requirements
- Caches Steam API responses for faster repeated checks
- Prints a summary table with game titles, scores, status, and unmet requirements

## Usage
### How to Get Your Steam Web API Key
1. Go to https://steamcommunity.com/dev/apikey
2. Log in with your Steam account.
3. Fill in the 'Domain Name' field (you can use `localhost` if unsure).
4. Click 'Register'.
5. Your Steam Web API key will be displayed. Copy and use it when prompted by the script.

### How to Find Your Steam ID
1. Log in to https://store.steampowered.com/ and click your profile name at the top.
2. Click 'View my profile'.
3. Your Steam ID is the long number in the URL (e.g., `https://steamcommunity.com/profiles/12345678901234567`).
	- If you see a custom name instead, click 'Edit Profile' and look for your Steam ID number.
4. You can also use your custom profile name (the part after `/id/` in the URL) when prompted.


## Installation & Running

### Install dependencies

- Python 3.7+
- Required packages: `requests`, `psutil`, `GPUtil`, `wmi`
- The script will check for these packages and prompt to install any missing ones automatically.

### Run the script

1. Open a terminal in this directory.
2. Run: `python steam_library_specs_checker.py`
3. Follow prompts:
	- Enter your Steam API key and Steam ID when prompted.
	- The script will detect your PC specs and check your games.

### New: Print or export matched games

- To print the list of games your PC meets requirements for (sorted by score):

```powershell
python steam_library_specs_checker.py --matches
```

- To export the matched list to a JSON file:

```powershell
python steam_library_specs_checker.py --export-matches matches.json
```

The `--matches` flag prints a concise sorted list after the main table. `--export-matches` writes a JSON array of matched games with `appid`, `title`, `score`, and `status`.

## Output
The script prints a table like:

```
Title                        Score   Status    Note      Unmet     
------------------------     -----   -------   -------   --------- 
Half-Life: Alyx              93      NO        [LIVE]    GPU,VRAM  
Portal 2                     95      REC       [CACHED]  -         
...
```

## Notes
- Your API key is masked in output for privacy.
- Results are cached in `appdetails_cache.json` for efficiency.
- Unmet requirements are shown as CPU, GPU, RAM, DISK, VRAM, or DirectX.
- The CPU parsing was improved to handle requirement strings like `1.7+ GHz` (some Steam entries use a `+` suffix). If a game previously reported a false negative on CPU, re-run the script to get updated results.

## License
MIT License. See LICENSE for details.

