# SteamLibrarySpecs

SteamLibrarySpecs is a command-line tool that checks your Steam library games against your PC's hardware specifications. It fetches system requirements for each game from the Steam Store and compares them to your detected CPU, GPU, RAM, and disk space, providing a summary of which games your system can run.

## Features
- Automatically detects your PC's CPU, GPU, RAM, and disk space
- Fetches minimum and recommended requirements for each game in your Steam library
- Compares your specs to each game's requirements and highlights unmet requirements
- Caches Steam API responses for faster repeated checks
- Prints a summary table with game titles, scores, status, and unmet requirements

## Usage
1. **Install dependencies:**
	- Python 3.7+
	- Required packages: `requests`
	- Install with: `pip install requests`

2. **Run the script:**
	- Open a terminal in this directory.
	- Run: `python steam_library_specs_checker.py`

3. **Follow prompts:**
	- Enter your Steam API key and Steam ID when prompted.
	- The script will detect your PC specs and check your games.

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

## License
MIT License. See LICENSE for details.

