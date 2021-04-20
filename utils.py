"""
ProjectTM
utils.py
Small Python Functions to make patterns shorter and easier
"""

from os import path

API_KEY_FILENAME: str = "api_key.key"

# This function is called if Riot API key not defined, or file does not exist
# Typical Riot Games Development API Key expires every 24 hours
def read_key() -> str:
    key = ""
    if (not path.exists(API_KEY_FILENAME)):
        with open(API_KEY_FILENAME, 'w') as writer:
            key = input("Enter Riot API Key: ")
            writer.write(key)
            print("If the wrong key was entered, modify file: api_key.ignore")
    else:
        with open(API_KEY_FILENAME) as reader:
            key = reader.readline()
        if (len(key) == 0):
            with open(API_KEY_FILENAME, 'w') as writer:
                key = input("Enter Riot API Key: ")
                writer.write(key)
                print("If the wrong key was entered, modify file: api_key.ignore")
    return key
