import os
import subprocess
import json
import logging
import shutil

PROGRAM_VERSION = "1.0.0"

def load_config():
    default_config = {
        "flac_search_path": "./",
        "dry_run": True,
        "log_level": "INFO",
        "flac_action": "leave",
        "new_flac_location": "./moved_flac",
        "tail_log": False
    }

    if not os.path.exists('config.json'):
        with open('config.json', 'w') as file:
            json.dump(default_config, file, indent=4)
        logging.info("config.json not found. Created with default configuration.")
        return default_config

    with open('config.json', 'r') as file:
        return json.load(file)

def set_log_level(log_level_str, tail_log):
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    log_level = levels.get(log_level_str, logging.INFO)
    logging.basicConfig(filename='logfile.log', level=log_level, format='%(asctime)s %(levelname)s:%(message)s')

    if tail_log:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

def check_directory_exists(directory):
    if not os.path.exists(directory):
        logging.error(f"Directory not found: {directory}")
        return False
    return True

def handle_flac_file(flac_file, action, new_location, config):
    if action == "delete":
        os.remove(flac_file)
        logging.info(f'Deleted FLAC file: {flac_file}')
    elif action == "move":
        # Extract the lowest level folder from the original path
        lowest_level_folder = os.path.basename(os.path.dirname(flac_file))
        # Construct new path with this folder within new_location
        new_path = os.path.join(new_location, lowest_level_folder, os.path.basename(flac_file))

        if os.path.exists(new_path):
            logging.info(f'File already exists, not moving: {new_path}')
            return

        new_dir = os.path.dirname(new_path)
        if not os.path.exists(new_dir):
            try:
                os.makedirs(new_dir)
                logging.debug(f"Created directory: {new_dir}")
            except OSError as e:
                logging.error(f"Could not create directory {new_dir}: {e}")
                return

        try:
            shutil.move(flac_file, new_path)
            logging.info(f'Moved FLAC file from {flac_file} to {new_path}')
        except OSError as e:
            logging.error(f"Could not move file {flac_file} to {new_path}: {e}")

def convert_flac_to_mp3(flac_file, mp3_file, action, new_location, config):
    # Check if the MP3 file already exists
    if os.path.exists(mp3_file):
        logging.info(f"MP3 file already exists, skipping conversion: {mp3_file}")
        return

    # Update FFmpeg command to include -n flag and -loglevel error
    cmd = f'ffmpeg -n -loglevel error -i "{flac_file}" -ab 320k "{mp3_file}"'
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f'Successfully converted {flac_file} to {mp3_file}')
        handle_flac_file(flac_file, action, new_location, config)
    except subprocess.CalledProcessError as e:
        logging.error(f'Error converting {flac_file}: {e}')


def find_and_log_flac_files(directory, dry_run, action, new_location, config):
    total_flac_files = 0  # Initialize counter for total FLAC files found

    if not check_directory_exists(directory):
        return
    if action == "move" and not check_directory_exists(new_location):
        return

    for root, dirs, files in os.walk(directory):
        if new_location.startswith(directory) and os.path.commonpath([root, new_location]) == new_location:
            continue

        for file in files:
            if file.endswith('.flac'):
                total_flac_files += 1  # Increment the counter
                flac_file = os.path.join(root, file)
                mp3_file = os.path.splitext(flac_file)[0] + '.mp3'

                if dry_run:
                    logging.debug(f'Found FLAC file ({total_flac_files}): {flac_file} (Dry run, not converting)')
                else:
                    logging.debug(f'Found FLAC file ({total_flac_files}): {flac_file} (Converting)')
                    convert_flac_to_mp3(flac_file, mp3_file, action, new_location, config)

    # Optionally, log the total count after the search
    logging.info(f"Total FLAC files found: {total_flac_files}")


def main():
    config = load_config()
    tail_log = config.get('tail_log', False)
    set_log_level(config.get('log_level', 'INFO'), tail_log)

    logging.info(f"Starting FLAC to MP3 Converter v{PROGRAM_VERSION}")
    logging.info(f"Configuration: {json.dumps(config, indent=4)}")

    flac_search_path = config.get('flac_search_path')
    dry_run = config.get('dry_run', False)
    flac_action = config.get('flac_action', 'leave')
    new_flac_location = config.get('new_flac_location', '')

    if check_directory_exists(flac_search_path):
        find_and_log_flac_files(flac_search_path, dry_run, flac_action, new_flac_location, config)

if __name__ == "__main__":
    main()
