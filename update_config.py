#!/usr/bin/env python3
import json
import os
import re
import logging
import argparse

CONFIG_JSON = "config.json"
HOME_STYLES_JS = "src/modules/Home/HomeStyles.js"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def read_json(file_path=CONFIG_JSON):
    """Reads and returns parsed JSON data from the specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = json.load(file)
        logging.info("✅ Successfully loaded JSON data.")
        return config.get("styles", {})
    except FileNotFoundError:
        logging.error(f"❌ Error: {file_path} not found!")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"❌ JSON decoding error in {file_path}: {e}")
        raise


def generate_js_style_block(style_dict):
    """Converts a dictionary of styles into JavaScript object format."""
    style_block = "{\n"
    for key, value in style_dict.items():
        formatted_value = f"'{value}'" if isinstance(value, str) else value
        style_block += f"    {key}: {formatted_value},\n"
    style_block += "}"
    return style_block


def update_home_styles(styles, file_path=HOME_STYLES_JS):
    """Updates 'textStyle' section in HomeStyles.js with new styles."""
    if "textStyle" not in styles:
        logging.warning("⚠️ No 'textStyle' found in JSON. Skipping update.")
        return

    # Convert JSON style to JavaScript format
    new_text_style = f"textStyle: {generate_js_style_block(styles['textStyle'])}"

    # Read the current content of HomeStyles.js
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        logging.error(f"❌ Error: {file_path} not found!")
        raise

    # Regular expression to find the 'textStyle' block
    pattern = re.compile(r"textStyle:\s*{\s*[^}]+}", re.MULTILINE)

    # Update the content by replacing the old 'textStyle' block with the new one
    updated_content = pattern.sub(new_text_style, content)

    # Write the updated content back to HomeStyles.js
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

    logging.info("✅ Successfully updated 'textStyle' in HomeStyles.js!")


def main():
    """Main function to orchestrate the update process."""

    try:
        styles = read_json()
        update_home_styles(styles)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error("❌ Terminating due to previous errors.")
        exit(1)


if __name__ == "__main__":
    main()
