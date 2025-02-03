#!/usr/bin/env python3
import os
import pbxproj


def update_pbxproj_with_infoplist_check(project_path, configurations, target_infoplist):
    # Load the .pbxproj file
    project = pbxproj.XcodeProject.load(project_path)
    
    # Iterate over configurations and update based on the given conditions
    for configuration in project.objects.get_configurations_on_targets():
        config_name = configuration['name']
        build_settings = configuration['buildSettings']

        # Check if INFOPLIST_FILE matches the target value
        if config_name in configurations and 'INFOPLIST_FILE' in build_settings and build_settings['INFOPLIST_FILE'] == target_infoplist:
            # Update PRODUCT_BUNDLE_IDENTIFIER
            build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = configurations[config_name]['PRODUCT_BUNDLE_IDENTIFIER']
            print(f"Updated {config_name} with bundle ID {build_settings['PRODUCT_BUNDLE_IDENTIFIER']} for {target_infoplist}")

    # Save changes back to the .pbxproj file
    project.save()
    print(f"Saved changes to {project_path}")


# Example usage
if __name__ == "__main__":
    pbxproj_file_path = "ios/WLDemo.xcodeproj/project.pbxproj"
    
    # Define the configurations and their bundle identifiers
    configurations = {
        'Debug': {
            'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.debug',
        },
        'Release': {
            'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.release',
        },
        'ReleaseProd': {
            'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.releaseprod',
        },
        'ReleaseStage': {
            'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.releasestage',
        },
    }

    # Specify the target Info.plist file
    target_infoplist = "WLDemo/Info.plist"

    # Run the script
    update_pbxproj_with_infoplist_check(pbxproj_file_path, configurations, target_infoplist)



# def update_pbxproj_with_configurations(project_path, configurations):
#     # Load the .pbxproj file
#     project = pbxproj.XcodeProject.load(project_path)

#     # Iterate over configurations and update PRODUCT_BUNDLE_IDENTIFIER
#     for configuration in project.objects.get_configurations_on_targets():
#         config_name = configuration['name']
#         if config_name in configurations:
#             build_settings = configuration['buildSettings']

#             # Update PRODUCT_BUNDLE_IDENTIFIER
#             build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = configurations[config_name]['PRODUCT_BUNDLE_IDENTIFIER']
#             print(f"Updated {config_name} with bundle ID {build_settings['PRODUCT_BUNDLE_IDENTIFIER']}")

#     # Save changes back to the .pbxproj file
#     project.save()
#     print(f"Saved changes to {project_path}")

# # Example usage
# if __name__ == "__main__":
#     pbxproj_file_path = "ios/WLDemo.xcodeproj/project.pbxproj"
    
#     # Define the configurations and their bundle identifiers
#     configurations = {
#         'Debug': {
#             'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.debug',
#         },
#         'Release': {
#             'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.release',
#         },
#         'ReleaseProd': {
#             'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.releaseprod',
#         },
#         'ReleaseStage': {
#             'PRODUCT_BUNDLE_IDENTIFIER': 'org.reactjs.native.example.releasestage',
#         },
#     }
    
#     update_pbxproj_with_configurations(pbxproj_file_path, configurations)






# def update_pbxproj_with_infoplist_check(project_path, config_name, new_bundle_id, target_infoplist):
#     # Load the .pbxproj file
#     project = pbxproj.XcodeProject.load(project_path)

#     # Iterate through configurations and update based on conditions
#     for configuration in project.objects.get_configurations_on_targets():
#         if config_name == configuration['name']:
#             build_settings = configuration['buildSettings']

#             # Check if the INFOPLIST_FILE matches the target value
#             if 'INFOPLIST_FILE' in build_settings and build_settings['INFOPLIST_FILE'] == target_infoplist:
#                 build_settings['PRODUCT_BUNDLE_IDENTIFIER'] = new_bundle_id
#                 print(f"Updated {config_name} for {target_infoplist} with bundle ID {new_bundle_id}")

#     # Save the changes back to the .pbxproj file
#     project.save()
#     print(f"Saved changes to {project_path}")

# # Example usage
# if __name__ == "__main__":
#     pbxproj_file_path = "ios/WLDemo.xcodeproj/project.pbxproj"
#     target_config = "Release"  # Example: Replace with your target configuration name
#     target_infoplist = "WLDemo/Info.plist"
#     bundle_identifier = "org.reactjs.native.example.WLDemo3"
    
#     update_pbxproj_with_infoplist_check(pbxproj_file_path, target_config, bundle_identifier, target_infoplist)







# #!/usr/bin/env python3
# import os
# import pbxproj

# def update_pbxproj_using_library(project_path, config_name, new_bundle_id):
#     project = pbxproj.XcodeProject.load(project_path)

#     # Iterate through build configurations and update the bundle ID
#     for configuration in project.objects.get_configurations_on_targets():
#         print(f"Checking configuration: {configuration['name']}")
#         if config_name == configuration['name']:
#             configuration['buildSettings']['PRODUCT_BUNDLE_IDENTIFIER'] = new_bundle_id

#     project.save()
#     print(f"Updated {config_name} with bundle ID {new_bundle_id}")


# update_pbxproj_using_library('ios/WLDemo.xcodeproj/project.pbxproj', 'Release', 'org.reactjs.native.example.debug2')