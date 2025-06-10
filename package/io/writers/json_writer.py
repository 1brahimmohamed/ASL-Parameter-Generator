import json


class JSONWriter:

    @staticmethod
    def write(data, filepath):
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)
