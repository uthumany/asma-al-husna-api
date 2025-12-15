import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI(
    title="Asma Al Husna API",
    description="A simple API for the 99 names of Allah (Asma Al Husna).",
    version="1.0.0"
)

# Define the path to the pre-processed data file
DATA_FILE = os.path.join("api", "names.json")

# Load the data once on startup
def load_data():
    """Loads the pre-processed JSON data."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"Data file not found at {DATA_FILE}. Please ensure it exists."}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON data."}

# Load the data once on startup
asma_al_husna_data = load_data()

@app.get("/", summary="Get all 99 names of Allah")
async def get_all_names():
    """
    Returns a JSON array containing all 99 names of Allah,
    including the Arabic name, transliteration, and English meaning.
    """
    if "error" in asma_al_husna_data:
        return JSONResponse(status_code=500, content=asma_al_husna_data)
    
    return asma_al_husna_data

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """Returns a simple status message."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
