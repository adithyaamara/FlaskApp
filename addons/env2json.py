import json
import os

def convert_env_to_json(env_file_path=None, json_file_path=None):
    """
        Reads env file from given directory or app root directory by default and converts it to a json format, writes it to a file with given name. 
    """
    app_root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Handle default arguments
    
    if env_file_path is None:
        env_file_path = os.path.join(app_root_directory, '.env')
    if json_file_path is None:
        json_file_path = os.path.join(app_root_directory, 'config.json')    
    
    # Open env , json file pointers.
    fp_env = open(env_file_path, 'r')
    fp_json = open(json_file_path,'w')     # JSON will be created.
    config_dict = {}
    
    # convert each line in env to dictionary item
    for line in fp_env.readlines():
        if line[0] == '#':
            print("Skipping the line because it is a comment!!")
            continue
        config_item = line.split('\n')[0].split('=')  # REMOVE TRAILING NEW LINE CHARACTER, SEPARATE LEFT AND RIGHT STRINGS.
        config_dict[config_item[0]] = config_item[1]  # Add each item taken from env as a dictionary item.

    json.dump(config_dict, fp_json, indent=4)  # Finally write converted config from env to dictionary. 

    # Close files.
    fp_env.close()
    fp_json.close()
