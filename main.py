import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
import os

app = FastAPI(
    title="Asma Al Husna API with Fonts",
    description="A simple API for the 99 names of Allah (Asma Al Husna) with Arabic font support.",
    version="2.1.0"
)

# Define the path to the pre-processed data file
DATA_FILE = os.path.join("api", "names.json")

# Font configuration
FONTS = {
    "default": {
        "name": "Default (Scheherazade New)",
        "url": "https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;500;600;700&display=swap",
        "family": "'Scheherazade New', serif"
    },
    "reem-kufi-fun": {
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
    "scheherazade-new": {
        "name": "Scheherazade New",
        "url": "https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;500;600;700&display=swap",
        "family": "'Scheherazade New', serif"
    },
    "fustat": {
        "name": "Fustat",
        "url": "https://fonts.googleapis.com/css2?family=Fustat:wght@200..800&display=swap",
        "family": "'Fustat', serif"
    },
    "badeen-display": {
        "name": "Badeen Display",
        "url": "https://fonts.googleapis.com/css2?family=Badeen+Display&display=swap",
        "family": "'Badeen Display', cursive"
    },
    "el-messiri": {
        "name": "El Messiri",
        "url": "https://fonts.googleapis.com/css2?family=El+Messiri:wght@400..700&display=swap",
        "family": "'El Messiri', sans-serif"
    },
    "kufam": {
        "name": "Kufam",
        "url": "https://fonts.googleapis.com/css2?family=Kufam:ital,wght@0,400..900;1,400..900&display=swap",
        "family": "'Kufam', sans-serif"
    },
    "beiruti": {
        "name": "Beiruti",
        "url": "https://fonts.googleapis.com/css2?family=Beiruti:wght@200..900&display=swap",
        "family": "'Beiruti', sans-serif"
    },
    "reem-kufi-ink": {
        "name": "Reem Kufi Ink",
        "url": "https://fonts.googleapis.com/css2?family=Reem+Kufi+Ink&display=swap",
        "family": "'Reem Kufi Ink', sans-serif"
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
    
    font_list_text = ", ".join(FONTS.keys())
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Asma Al Husna - 99 Names of Allah</title>
        <style>
            * {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            body {{ max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #333; }}
            .controls {{ margin: 20px 0; text-align: center; background: #f8f9fa; padding: 20px; border-radius: 8px; }}
            select {{ padding: 10px; font-size: 16px; border-radius: 4px; border: 1px solid #ddd; min-width: 250px; }}
            .names-list {{ 
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 30px; 
            }}
            .name-item {{ 
                padding: 20px; 
                background: #fff; 
                border: 1px solid #eee;
                border-radius: 8px;
                transition: transform 0.2s;
                text-align: center;
            }}
            .name-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            .arabic {{ 
                font-size: 36px; 
                margin-bottom: 15px; 
                direction: rtl; 
                color: #2c3e50;
                min-height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .transliteration {{ font-weight: bold; color: #e67e22; font-size: 18px; }}
            .meaning {{ color: #7f8c8d; margin-top: 8px; font-style: italic; }}
            .api-info {{ background: #e3f2fd; padding: 15px; border-radius: 4px; margin-bottom: 20px; }}
            .api-info p {{ margin: 5px 0; }}
            code {{ background: #eee; padding: 2px 5px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Asma Al Husna - The 99 Names of Allah</h1>
            
            <div class="api-info">
                <p><strong>API Endpoints:</strong></p>
                <p>JSON API: <code>/api/names?font=reem-kufi-fun</code></p>
                <p>Available fonts: <code>{font_list_text}</code></p>
            </div>
            
            <div class="controls">
                <label for="font-select"><strong>Choose Arabic Font:</strong> </label>
                <select id="font-select" onchange="updateFont()">
                    {font_options}
                </select>
            </div>
            
            <div class="names-list" id="names-container"></div>
        </div>
        
        <script>
            const FONTS_DATA = {json.dumps(FONTS)};
            
            async function loadNames(fontKey = 'default') {{
                try {{
                    const response = await fetch(`/api/names?font=${{fontKey}}`);
                    const data = await response.json();
                    const container = document.getElementById('names-container');
                    container.innerHTML = '';
                    
                    // Ensure font is loaded
                    const fontData = FONTS_DATA[fontKey] || FONTS_DATA['default'];
                    await loadFont(fontData);
                    
                    data.names.forEach((item) => {{
                        const div = document.createElement('div');
                        div.className = 'name-item';
                        div.innerHTML = `
                            <div class="arabic" style="font-family: ${{fontData.family}}">${{item.name}}</div>
                            <div class="transliteration">${{item.transliteration}}</div>
                            <div class="meaning">${{item.meaning}}</div>
                        `;
                        container.appendChild(div);
                    }});
                }} catch (error) {{
                    console.error('Error:', error);
                }}
            }}
            
            function loadFont(fontData) {{
                return new Promise((resolve) => {{
                    const linkId = 'dynamic-font-link';
                    let link = document.getElementById(linkId);
                    if (!link) {{
                        link = document.createElement('link');
                        link.id = linkId;
                        link.rel = 'stylesheet';
                        document.head.appendChild(link);
                    }}
                    link.href = fontData.url;
                    // Small delay to allow font to start loading
                    setTimeout(resolve, 100);
                }});
            }}
            
            function updateFont() {{
                const font = document.getElementById('font-select').value;
                loadNames(font);
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
    - font: Font family key (e.g., reem-kufi-fun, cairo, lemonada, etc.)
    """
    if "error" in asma_al_husna_data:
        return JSONResponse(status_code=500, content=asma_al_husna_data)
    
    font_info = FONTS.get(font, FONTS["default"])
    
    response_data = {
        "font": font,
        "font_name": font_info["name"],
        "font_family": font_info["family"],
        "font_url": font_info["url"],
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
    return {"status": "ok", "version": "2.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
