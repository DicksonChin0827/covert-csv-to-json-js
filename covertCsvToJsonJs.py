import csv
import argparse
import os

def generate_mongo_script(csv_file):
    mongo_data = []

    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            mongo_entry = '{'
            for key, value in row.items():
                cleaned_value = value.strip() if value is not None else ""
                mongo_entry += f' "{key}": "{cleaned_value}",'
            mongo_entry = mongo_entry.rstrip(',') + ' }'
            mongo_data.append(mongo_entry)

    script = f"[\n  {',\n  '.join(mongo_data)}\n];"
    return script

def process_file(csv_path, output_folder):
    base_filename = os.path.splitext(os.path.basename(csv_path))[0]
    output_filename = os.path.join(output_folder, f"{base_filename}.js")

    mongo_script = generate_mongo_script(csv_path)

    with open(output_filename, 'w', encoding='utf-8') as js_file:
        js_file.write(mongo_script)

    print(f"✅ Converted '{csv_path}' to '{output_filename}'")

def main():
    parser = argparse.ArgumentParser(description='Generate MongoDB insert scripts from CSV files.')
    parser.add_argument('path', help='CSV file or folder containing CSV files')

    args = parser.parse_args()
    input_path = args.path

    # Create output directory
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(input_path):
        if input_path.lower().endswith(".csv"):
            process_file(input_path, output_dir)
        else:
            print(f"❌ The file '{input_path}' is not a CSV.")
    elif os.path.isdir(input_path):
        csv_files = [f for f in os.listdir(input_path) if f.lower().endswith(".csv")]
        if not csv_files:
            print(f"⚠️ No CSV files found in folder '{input_path}'.")
            return
        for csv_file in csv_files:
            full_csv_path = os.path.join(input_path, csv_file)
            process_file(full_csv_path, output_dir)
    else:
        print(f"❌ The path '{input_path}' does not exist.")

if __name__ == '__main__':
    main()

