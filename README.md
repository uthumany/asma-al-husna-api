# asma-al-husna-api

A simple, static JSON API endpoint containing the 99 names of Allah (Asma Al Husna), including the Arabic name, transliteration, and English meaning.

This project was created by extracting data from the AlAdhan API.

## API Endpoint

The data is served as a static JSON file via GitHub Pages.

**Endpoint URL:** `https://uthumany.github.io/asma-al-husna-api/api/names.json`

## Data Structure

The endpoint returns a JSON array of objects, where each object has the following structure:

```json
[
  {
    "name": "الرَّحْمَنُ",
    "transliteration": "Ar Rahmaan",
    "meaning": "The Beneficent"
  },
  // ... 98 more names
]
```

## Local Development

While the primary endpoint is the static JSON file, the project also includes a basic FastAPI application (`main.py`) that can be run locally to serve the data.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the API:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000/`.
