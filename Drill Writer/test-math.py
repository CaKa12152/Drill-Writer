import json

# Function to read the JSON data from the file
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data


# Function to write the modified JSON data to the file
def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Data has been written to {file_path}")

# Function to update a value in the JSON data
def update_value(data, key, x=None, y=None):
    if key in data:
        if x is not None:
            data[key]["x"] = x
        if y is not None:
            data[key]["y"] = y

# Main function
def main():
    file_path = 'data.json'

    # Read data from JSON file
    data = read_json(file_path)

    # Example: Read the value for key '0'
    if data:
        print("Current data:", data)
        print(f"Value for key '0': {data.get('0', 'Not found')}")

        # Example: Update values for key '1'
        update_value(data, '1', x=300, y=300)

        # Write updated data back to the file
        write_json(file_path, data)

if __name__ == "__main__":
    main()