import json
import csv

def print_json_items(file_path, output_file):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    with open(output_file, 'w') as f:
        for item in data:
            f.write(item + ',')
        f.write('\n')

print_json_items('src/alignments/allDisney.json', 'src/alignments/item_names.txt')