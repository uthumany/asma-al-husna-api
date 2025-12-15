import json
import os

# Define the output directory and file
OUTPUT_DIR = "api"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "names.json")
INPUT_FILE = "asma_al_husna.json"

def load_and_process_data():
    """Loads the raw JSON data and extracts the required fields."""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return None

    processed_data = []
    # The actual list of names is under the "data" key
    names_list = raw_data.get("data", [])

    for item in names_list:
        # Extract the required fields
        name = item.get("name")
        transliteration = item.get("transliteration")
        # The meaning is nested under the "en" key
        meaning = item.get("en", {}).get("meaning")

        if name and transliteration and meaning:
            processed_data.append({
                "name": name,
                "transliteration": transliteration,
                "meaning": meaning
            })

    return processed_data

def save_processed_data(data):
    """Saves the processed data to the output file."""
    if not data:
        print("No data to save.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {len(data)} names to '{OUTPUT_FILE}'")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    processed_data = load_and_process_data()
    if processed_data:
        save_processed_data(processed_data)
