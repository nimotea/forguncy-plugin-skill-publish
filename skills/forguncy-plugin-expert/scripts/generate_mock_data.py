import json
import random
import uuid
import argparse
import os
from datetime import datetime, timedelta

def generate_value(field_type, index):
    """
    Generates a random value based on the field type definition.
    Supported types:
    - uuid: Generates a UUID string.
    - string:prefix_{index}: Generates a string with prefix and index.
    - int:min,max: Generates a random integer between min and max.
    - date:today/future_Xd/past_Xd: Generates a date string (YYYY-MM-DD).
    - enum:val1,val2,val3: Picks a random value from the list.
    - bool: Generates a random boolean.
    """
    if field_type == "uuid":
        return str(uuid.uuid4())
    
    if field_type.startswith("string:"):
        template = field_type.split(":", 1)[1]
        return template.replace("{index}", str(index))
    
    if field_type.startswith("int:"):
        try:
            range_str = field_type.split(":", 1)[1]
            min_val, max_val = map(int, range_str.split(","))
            return random.randint(min_val, max_val)
        except ValueError:
            return 0

    if field_type.startswith("date:"):
        mode = field_type.split(":", 1)[1]
        today = datetime.now()
        if mode == "today":
            return today.strftime("%Y-%m-%d")
        elif mode.startswith("future_"):
            days = int(mode.split("_")[1][:-1])
            return (today + timedelta(days=random.randint(1, days))).strftime("%Y-%m-%d")
        elif mode.startswith("past_"):
            days = int(mode.split("_")[1][:-1])
            return (today - timedelta(days=random.randint(1, days))).strftime("%Y-%m-%d")
        return today.strftime("%Y-%m-%d")

    if field_type.startswith("enum:"):
        options = field_type.split(":", 1)[1].split(",")
        return random.choice(options)

    if field_type == "bool":
        return random.choice([True, False])

    return field_type  # Return literal if no match

def generate_data(config_path, output_dir):
    """
    Reads the config file and generates mock data files in the output directory.
    """
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON config: {e}")
        return

    for item in config.get("outputs", []):
        filename = item.get("filename", "output.json")
        count = item.get("count", 10)
        schema = item.get("schema", {})
        
        data_list = []
        for i in range(1, count + 1):
            record = {}
            for key, field_type in schema.items():
                record[key] = generate_value(field_type, i)
            data_list.append(record)
        
        output_path = os.path.join(output_dir, filename)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data_list, f, indent=4, ensure_ascii=False)
            print(f"Generated {count} records in {output_path}")
        except IOError as e:
            print(f"Error writing file {output_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mock data based on a JSON configuration.")
    parser.add_argument("--config", required=True, help="Path to the JSON configuration file.")
    parser.add_argument("--output", default=".", help="Directory to save generated files.")
    
    args = parser.parse_args()
    generate_data(args.config, args.output)
