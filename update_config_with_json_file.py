#!/usr/bin/env python3
import os
import json
import pbxproj

def update_pbxproj_with_infoplist_check(project_path, flavors, target_infoplist):
    # Load the .pbxproj file
    project = pbxproj.XcodeProject.load(project_path)
    
    # Iterate over configurations and update based on the given conditions
    for configuration in project.objects.get_configurations_on_targets():
        config_name = configuration['name']
        build_settings = configuration['buildSettings']

        # Check if INFOPLIST_FILE matches the target value
        if config_name in flavors and 'INFOPLIST_FILE' in build_settings and build_settings['INFOPLIST_FILE'] == target_infoplist:
            # Update PRODUCT_BUNDLE_IDENTIFIER
            build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = flavors[config_name]['PRODUCT_BUNDLE_IDENTIFIER']
            print(f"Updated {config_name} with bundle ID {build_settings['PRODUCT_BUNDLE_IDENTIFIER']} for {target_infoplist}")

    # Save changes back to the .pbxproj file
    project.save()
    print(f"Saved changes to {project_path}")


# Example usage
if __name__ == "__main__":
    pbxproj_file_path = "ios/WLDemo.xcodeproj/project.pbxproj"
    json_config_file = "configurations.json"

    # Load configurations from JSON file
    if not os.path.exists(json_config_file):
        print(f"Error: Configurations file '{json_config_file}' not found.")
        exit(1)

    with open(json_config_file, "r") as file:
        data = json.load(file)

    # Ensure 'flavors' key exists
    if 'flavors' not in data:
        print("Error: Missing 'flavors' key in JSON file.")
        exit(1)

    # Extract flavors
    flavors = data['flavors']

    # Specify the target Info.plist file
    target_infoplist = "WLDemo/Info.plist"

    # Run the script
    update_pbxproj_with_infoplist_check(pbxproj_file_path, flavors, target_infoplist)
