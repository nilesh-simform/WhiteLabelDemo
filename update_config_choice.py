#!/usr/bin/env python3
import os
import json
import shutil
import logging
import re
import curses
from subprocess import run, CalledProcessError

CONFIG_FILE = 'config.json'
COLORS_FILE = 'colors.ts'
STRINGS_FILE = 'strings.ts'
IOS_INFO_PLIST = 'ios/WLDemo/Info.plist'
ANDROID_GRADLE_FILE = 'android/app/build.gradle'
ANDROID_STRINGS_XML = 'android/app/src/main/res/values/strings.xml'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_json(app_folder):
    """Reads the JSON configuration file from the given app folder."""
    src_config_path = os.path.join(app_folder, CONFIG_FILE)
    logging.info(f'Reading JSON configuration from {src_config_path}')

    try:
        with open(src_config_path, 'r') as file:
            data = json.load(file)
        logging.info(f'Configuration data: {data}')
        return data
    except FileNotFoundError:
        logging.error(f"Configuration file '{src_config_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in file '{src_config_path}': {e}")
        raise


def replace_file(src_path, dest_path):
    """Replaces a file from source to destination."""
    try:
        shutil.copyfile(src_path, dest_path)
        logging.info(f'Replaced {os.path.basename(src_path)} with the file from {src_path}')
    except IOError as e:
        logging.error(f"Error copying file from {src_path} to {dest_path}: {e}")
        raise


def replace_colors_file(app_folder):
    """Replaces the colors.ts file."""
    logging.info('Replacing colors.ts file')
    src_colors_path = os.path.join(app_folder, COLORS_FILE)
    dest_colors_path = 'src/config/colors.ts'
    replace_file(src_colors_path, dest_colors_path)


def replace_strings_file(app_folder):
    """Replaces the strings.ts file."""
    logging.info('Replacing strings.ts file')
    src_strings_path = os.path.join(app_folder, STRINGS_FILE)
    dest_strings_path = 'src/config/strings.ts'
    replace_file(src_strings_path, dest_strings_path)


def update_ios_config(data):
    """Updates iOS app configuration (bundle ID and app name)."""
    logging.info('Updating iOS configuration')

    try:
        # Update iOS bundle ID
        run(f"plutil -replace CFBundleIdentifier -string {data['bundleId']} {IOS_INFO_PLIST}", shell=True, check=True)
        logging.info('Updated iOS bundle ID')

        # Update iOS app name
        run(f"plutil -replace CFBundleDisplayName -string \"{data['appName']}\" {IOS_INFO_PLIST}", shell=True, check=True)
        logging.info('Updated iOS app name')
    except CalledProcessError as e:
        logging.error(f"Error updating iOS configuration: {e}")
        raise


def update_android_config(data):
    """Updates Android app configuration (bundle ID and app name)."""
    logging.info('Updating Android configuration')

    try:
        # Update Android bundle ID in build.gradle
        run(f"sed -i '' 's/applicationId .*/applicationId \"{data['bundleId']}\"/' {ANDROID_GRADLE_FILE}", shell=True, check=True)
        logging.info('Updated Android bundle ID')

        # Update app name in strings.xml
        with open(ANDROID_STRINGS_XML, 'r') as file:
            strings_xml_content = file.read()

        new_app_name = data['appName']
        strings_xml_content = re.sub(r'(<string name="app_name">)[^<]*(</string>)', rf'\1{new_app_name}\2', strings_xml_content)

        with open(ANDROID_STRINGS_XML, 'w') as file:
            file.write(strings_xml_content)

        logging.info('Updated app name in strings.xml')

    except CalledProcessError as e:
        logging.error(f"Error updating Android configuration: {e}")
        raise
    except IOError as e:
        logging.error(f"Error reading or writing to file: {e}")
        raise


def menu(stdscr, options):
    """Displays a menu in the terminal using curses."""
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr("Use arrow keys to navigate and Enter to select.\n\n")

        for i, option in enumerate(options):
            if i == selected:
                stdscr.addstr(f"> {option}\n", curses.A_REVERSE)  # Highlight selected option
            else:
                stdscr.addstr(f"  {option}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key == 10:  # Enter key
            return options[selected]


def main(app):
    """Main function to handle the workflow of replacing files and updating configs."""
    app_folder = os.path.join('apps', app)

    try:
        # Read the JSON configuration file
        data = read_json(app_folder)

        # Replace color and string files
        replace_colors_file(app_folder)
        replace_strings_file(app_folder)

        # Update iOS and Android configuration files
        update_ios_config(data)
        update_android_config(data)

    except Exception as e:
        logging.error(f"An error occurred during the execution: {e}")
        raise


if __name__ == "__main__":
    options = ["app1", "app2"]

    # Run the menu and select the app
    selected_option = curses.wrapper(menu, options)
    logging.info(f"You selected: {selected_option}")

    main(selected_option)
