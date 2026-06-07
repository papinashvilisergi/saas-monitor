from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# HTML გვერდისთვის (მთავარ გვერდზე)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>🌍 SaaS Weather Monitor</h1>
            <input type="text" id="city" placeholder="შეიყვანეთ ქალაქი (მაგ: Tbilisi)">
            <button onclick="getWeather()">ნახე ამინდი</button>
            <div id="result" style="margin-top: 20px; font-size: 24px; font-weight: bold;"></div>
            <script>
                async function getWeather() {
                    const city = document.getElementById('city').value;
                    const res = await fetch('/weather/' + city);
                    const data = await res.json();
                    document.getElementById('result').innerText = data.city + ': ' + data.temperature;
                }
            </script>
        </body>
    </html>
    """

@app.get("/weather/{city}")
async def get_weather(city: str):
    # იპოვის ქალაქს კოორდინატებით
    async with httpx.AsyncClient() as client:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_resp = await client.get(geo_url)
        geo_data = geo_resp.json()
        
        if not geo_data.get('results'):
            return {"city": city, "temperature": "ქალაქი ვერ მოიძებნა"}
        
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m"
        w_resp = await client.get(weather_url)
        w_data = w_resp.json()
        
        return {
            "city": city,
            "temperature": f"{w_data['current']['temperature_2m']}°C"
        }