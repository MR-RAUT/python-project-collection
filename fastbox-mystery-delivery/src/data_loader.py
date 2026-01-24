import json

# Load data from a JSON file
def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)