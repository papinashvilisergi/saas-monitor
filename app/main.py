from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/weather/{city}")
async def get_weather(city: str):
    # თბილისის კოორდინატები
    lat, lon = 41.7151, 44.8271
    
    async with httpx.AsyncClient() as client:
        # ვიძახებთ Open-Meteo-ს API-ს
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
        response = await client.get(url)
        data = response.json()
        
        return {
            "city": city,
            "temperature": f"{data['current']['temperature_2m']}°C",
            "source": "Open-Meteo API"
        }

@app.get("/status")
def get_system_status():
    return {
        "status": "online",
        "version": "1.0.0",
        "feature": "Live Weather Integration"
    }