import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
import os

app = FastAPI(
    title="Asma Al Husna API with Fonts",
    description="A simple API for the 99 names of Allah (Asma Al Husna) with Arabic font support.",
    version="2.0.0"
)

# Define the path to the pre-processed data file
DATA_FILE = os.path.join("api", "names.json")

# Font configuration
FONTS = {
    "default": {
        "name": "Default (Arabic Default)",
        "url": "https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;500;600;700&display=swap",
        "family": "'Scheherazade New', serif"
    },
    "reem-kufi": {
        "name": "Reem Kufi Fun",
        "url": "https://fonts.googleapis.com/css2?family=Reem+Kufi+Fun:wght@400..700&display=swap",
        "family": "'Reem Kufi Fun', sans-serif"
    },
    "cairo": {
        "name": "Cairo",
        "url": "https://fonts.googleapis.com/css2?family=Cairo:wght@200..1000&display=swap",
        "family": "'Cairo', sans-serif"
    },
    "lemonada": {
        "name": "Lemonada",
        "url": "https://fonts.googleapis.com/css2?family=Lemonada:wght@300..700&display=swap",
        "family": "'Lemonada', cursive"
    },
    "scheherazade": {
        "name": "Scheherazade New",
        "url": "https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;500;600;700&display=swap",
        "family": "'Scheherazade New', serif"
    },
    "fustat": {
        "name": "Fustat",
        "url": "https://fonts.googleapis.com/css2?family=Fustat:wght@200..800&display=swap",
        "family": "'Fustat', serif"
    }
}

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

asma_al_husna_data = load_data()

@app.get("/", summary="Get all 99 names of Allah", response_class=HTMLResponse)
async def get_root():
    """Returns an HTML page with font selection interface."""
    font_options = "".join([
        f'<option value="{key}">{value["name"]}</option>'
        for key, value in FONTS.items()
    ])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Asma Al Husna - 99 Names of Allah</title>
        <style>
            * {{ font-family: Arial, sans-serif; }}
            body {{ max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #333; }}
            .controls {{ margin: 20px 0; text-align: center; }}
            select {{ padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ddd; }}
            .names-list {{ margin-top: 30px; }}
            .name-item {{ padding: 15px; margin: 10px 0; background: #f9f9f9; border-left: 4px solid #007bff; border-radius: 4px; }}
            .arabic {{ font-size: 28px; margin-bottom: 5px; direction: rtl; }}
            .transliteration {{ font-weight: bold; color: #555; }}
            .meaning {{ color: #777; margin-top: 5px; }}
            .api-info {{ background: #e3f2fd; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
            .api-info p {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Asma Al Husna - The 99 Names of Allah</h1>
            
            <div class="api-info">
                <p><strong>API Endpoints:</strong></p>
                <p>JSON API: <code>/api/names</code> or <code>/api/names?font=reem-kufi</code></p>
                <p>Available fonts: default, reem-kufi, cairo, lemonada, scheherazade, fustat</p>
            </div>
            
            <div class="controls">
                <label for="font-select">Select Arabic Font:</label>
                <select id="font-select" onchange="updateFont()">
                    {font_options}
                </select>
            </div>
            
            <div class="names-list" id="names-container"></div>
        </div>
        
        <script>
            async function loadNames(font = 'default') {{
                try {{
                    const response = await fetch(`/api/names?font=${{font}}`);
                    const data = await response.json();
                    const container = document.getElementById('names-container');
                    container.innerHTML = '';
                    
                    data.forEach((item, index) => {{
                        const div = document.createElement('div');
                        div.className = 'name-item';
                        div.innerHTML = `
                            <div class="arabic" id="font-style">${{item.name}}</div>
                            <div class="transliteration">${{item.transliteration}}</div>
                            <div class="meaning">${{item.meaning}}</div>
                        `;
                        container.appendChild(div);
                    }});
                    applyFontStyle(font);
                }} catch (error) {{
                    console.error('Error:', error);
                }}
            }}
            
            function updateFont() {{
                const font = document.getElementById('font-select').value;
                loadNames(font);
            }}
            
            function applyFontStyle(font) {{
                const fontMap = {json.dumps(FONTS)};
                const fontData = fontMap[font];
                if (fontData) {{
                    const style = document.createElement('link');
                    style.rel = 'stylesheet';
                    style.href = fontData.url;
                    document.head.appendChild(style);
                    
                    const elements = document.querySelectorAll('.arabic');
                    elements.forEach(el => {{
                        el.style.fontFamily = fontData.family;
                    }});
                }}
            }}
            
            // Load default font on page load
            loadNames('default');
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/names", summary="Get all 99 names with font support")
async def get_all_names(font: str = Query("default", description="Font family to use")):
    """
    Returns a JSON array containing all 99 names of Allah.
    
    Parameters:
    - font: Font family (default, reem-kufi, cairo, lemonada, scheherazade, fustat)
    """
    if "error" in asma_al_husna_data:
        return JSONResponse(status_code=500, content=asma_al_husna_data)
    
    response_data = {
        "font": font,
        "font_name": FONTS.get(font, FONTS["default"])["name"],
        "font_family": FONTS.get(font, FONTS["default"])["family"],
        "font_url": FONTS.get(font, FONTS["default"])["url"],
        "names": asma_al_husna_data
    }
    
    return response_data

@app.get("/api/names/fonts", summary="Get available fonts")
async def get_fonts():
    """Returns a list of all available fonts."""
    return {
        "fonts": {
            key: {
                "name": value["name"],
                "family": value["family"],
                "url": value["url"]
            }
            for key, value in FONTS.items()
        }
    }

@app.get("/health", summary="Health check endpoint")
async def health_check():
    """Returns a simple status message."""
    return {"status": "ok", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
