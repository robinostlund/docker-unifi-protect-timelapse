#!/usr/bin/env python3
import os
import configparser
import requests

from datetime import datetime

# global variables
config_file = "/app.conf"
storage_folder = "/storage"
date_now = datetime.now()

class UbiquitiCamera(object):
    def __init__(self, name: str, ip: str):
        self.camera_name = name.replace(" ", "_").lower()
        self.camera_ip = ip

        # build camera folder structure
        self.camera_folder = os.path.join(storage_folder, self.camera_name) # create camera name folder
        self.camera_folder = os.path.join(self.camera_folder, date_now.strftime("%Y")) # create year folder
        self.camera_folder = os.path.join(self.camera_folder, date_now.strftime("%m")) # create month folder
        self.camera_folder = os.path.join(self.camera_folder, date_now.strftime("%d")) # create day folder
        self.camera_folder = os.path.join(self.camera_folder, date_now.strftime("%H")) # create hour folder

        # check if camera folder exists
        if not os.path.exists(self.camera_folder):
            print(f'WARN: "{self.camera_folder}" does not exist, creating it!')
            os.makedirs(self.camera_folder)

    def download_screenshot(self) -> None:
        url = f'http://{self.camera_ip}/snap.jpeg'
        print(f'INFO: fetching image from "{url}')
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            file_path = os.path.join(self.camera_folder, f'{date_now.strftime("%M:%S")}.jpg')
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(f'INFO: saved image to "{file_path}')
                return True
        else:
            print(f'ERROR: could not access "{url}')
            return False


def main():
    # read config
    if not os.path.exists(config_file):
        print(f'ERROR: "{config_file}" does not exist, please create it!')
        return False
    
    config = configparser.ConfigParser()
    config.read(config_file)

    # check if base folder exists
    if not os.path.exists(storage_folder):
        print(f'ERROR: "{base_folder}" does not exist, you need to create it before this script starts to work!')
        return False

    # verify config
    config_error = False
    for camera in config.sections():
        # check if we have a name
        if 'name' not in config[camera]:
            print(f'ERROR: "{camera}" has no name!')
            config_error = True
        
        # check if we have an ip
        if 'ip' not in config[camera]:
            print(f'ERROR: "{camera}" has no ip address!')
            config_error = True
    
    # if we dont have any config error we can continue
    if not config_error:
        # loop through each camera
        exit_status = True
        for camera in config.sections():
            cam = UbiquitiCamera(name = config[camera].get('name'), ip = config[camera].get('ip'))
            camera_status = cam.download_screenshot()
            if not camera_status:
                exit_status = False
        return exit_status
    else:
        return False

if __name__ == "__main__":
    status = main()
    # return our status
    if status:
        exit(0)
    else:
        exit(1)