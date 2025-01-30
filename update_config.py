#!/usr/bin/env python3
import json
import re
import os

# Paths
CONFIG_FILE = "config.json"
GRADLE_FILE = "android/app/build.gradle"

# Load JSON configuration
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

# Read the existing build.gradle content
with open(GRADLE_FILE, "r") as f:
    gradle_content = f.read()

# Function to update product flavors in build.gradle
def update_android_flavor(flavor, values):
    pattern = rf"{flavor}\s*{{[^}}]+manifestPlaceholders=\[hostName:\".*?\"\][^}}]*}}"

    replacement = f"""
        {flavor} {{
            manifestPlaceholders=[hostName:"{values['hostName']}"]
            dimension 'envirnoment'
            {'applicationId ' + "'" + values['applicationId'] + "'" if 'applicationId' in values else ''}
            {'applicationIdSuffix ' + "'" + values['applicationIdSuffix'] + "'" if 'applicationIdSuffix' in values else ''}
        }}
    """.strip()

    return re.sub(pattern, replacement, gradle_content, flags=re.DOTALL)


if __name__ == "__main__":
    # Update each product flavor
    for flavor, values in config.items():
        gradle_content = update_android_flavor(flavor, values)

    # Write the updated content back to build.gradle
    with open(GRADLE_FILE, "w") as f:
        f.write(gradle_content)

print("✅ build.gradle updated successfully!")