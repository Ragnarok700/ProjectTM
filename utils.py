from os import path

API_KEY_FILENAME: str = "api_key.ignore"

def read_key() -> str:
    # if key not defined, or file does not exist
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