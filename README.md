# FLAC to MP3 Converter

This Python script converts FLAC audio files to MP3 format. It traverses a specified directory, finds all FLAC files, and converts them using FFmpeg. The script also allows for various post-conversion actions on the original FLAC files.

## Features

- Traverses directories to find and convert FLAC files to MP3.
- Configurable through a JSON file.
- Dry run mode to list FLAC files without converting.
- Customizable logging levels.
- Options to delete, leave, or move the original FLAC files after conversion.
- Real-time log tailing in the console (configurable).

## Configuration

The script is configurable through a `config.json` file located in the same directory. This file allows you to set various options such as the search path for FLAC files, dry run mode, logging level, post-conversion actions for FLAC files, and the real-time log tailing feature.

### Configurable Options

- `flac_search_path`: Directory path to search for FLAC files.
- `dry_run`: Set to `true` for a dry run without converting files.
- `log_level`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- `flac_action`: Action for FLAC files post-conversion (`leave`, `delete`, `move`).
- `new_flac_location`: New location for moved FLAC files.
- `tail_log`: Set to `true` to enable real-time log tailing in the console.

```json
{
    "flac_search_path": "path_to_your_flac_files",
    "dry_run": false,
    "log_level": "INFO",
    "flac_action": "leave",
    "new_flac_location": "path_to_new_location_for_flac_files",
    "tail_log": true
}
```
## Logging Levels

The script supports various logging levels, which determine the amount and type of information logged. The primary levels used in this script are `DEBUG` and `INFO`.

### INFO Level

- **Description**: This is the default logging level.
- **Use-case**: Use this level for normal operation.
- **Details Logged**: At this level, the script logs key events like the start and completion of FLAC file conversions, any errors encountered, and summaries of actions taken (e.g., files converted, moved, or deleted).

### DEBUG Level

- **Description**: This level logs more detailed information.
- **Use-case**: Use `DEBUG` for in-depth troubleshooting or debugging.
- **Details Logged**: Includes everything logged at the `INFO` level, plus more detailed information such as each FLAC file discovered during directory traversal, detailed FFmpeg command execution data, and more granular status updates of the script's processing steps.

Adjust the logging level in the `config.json` file based on your needs. For everyday use, `INFO` is recommended. Switch to `DEBUG` if you need detailed insights into the script's operation, especially for diagnosing issues or understanding the script's behavior in depth.


## Requirements

- Python 3
- FFmpeg installed and added to the system's PATH.

## Usage

1. Ensure Python 3 and FFmpeg are installed on your system.
2. Place the script and `config.json` in the same directory.
3. Configure `config.json` as needed.
4. Run the script with `python script_name.py`.

## License


## Author

Kelly Norton
