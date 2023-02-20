import yaml
import os
import requests
from pprint import pprint


def main():
    daily = []
    hourly = []

    print("Getting weather data")
    res = requests.get("http://wttr.in/Cape%20Town?format=j1")
    if res.ok:
        try:
            weather_data = res.json()
            pprint(weather_data.keys())
            for item in weather_data["weather"]:
                # First figure out the hourly weather
                emojis = []
                for hr in item["hourly"]:
                    hour = int(hr["time"]) // 100
                    start = item["date"] + "T" + f"{hour:0>2}:00:00"
                    if hour + 3 == 24:
                        hour = 23
                        minute = 59
                    else:
                        hour = hour + 3
                        minute = 0
                    end = item["date"] + "T" + f"{hour:0>2}:{minute:0>2}:00"
                    temp = hr["tempC"]
                    pressure = hr["pressure"]
                    desc: str = WWO_CODE[hr["weatherCode"]]
                    emoji = WEATHER_SYMBOL.get(desc, "")
                    emojis.append(emoji)
                    desc = (
                        "".join([(c if c.islower() else " " + c.lower()) for c in desc])
                        .strip()
                        .capitalize()
                    )
                    lines = [
                        f"Feels Like: {hr['FeelsLikeC']}",
                        f"Wind Speed: {hr['windspeedKmph']}km/h",
                        f"Wind Direction: {hr['winddir16Point']}",
                        f"Wind Gust: {hr['WindGustKmph']}km/h",
                        f"Cloud Cover: {hr['cloudcover']}%",
                        f"Humidity: {hr['humidity']}%",
                        f"Precipitation: {hr['precipMM']}mm",
                        f"Pressure: {hr['pressure']}hPa",
                        f"visibility: {hr['visibility']}km",
                        f"Chance of Rain: {hr['chanceofrain']}%",
                        f"Chance of Sunshine: {hr['chanceofsunshine']}%",
                    ]
                    hourly.append(
                        {
                            "title": f"{emoji} {desc} {temp}°C {pressure}hPa",
                            "description": "\n".join(lines),
                            "start": start + "+02:00",
                            "end": end + "+02:00",
                        }
                    )
                temp = item["avgtempC"]
                sunset = item["astronomy"][0]["sunset"]
                emojis = "".join(emojis)
                daily.append(
                    {
                        "title": f"{emojis} {item['mintempC']}-{item['maxtempC']}°C",
                        "description": f"Sunset at {sunset}",
                        "start": item["date"] + "+02:00",
                        "end": item["date"] + "+02:00",
                    }
                )
        except Exception as e:
            print(f"Failed to get weather events: {e}")
    else:
        print("Failed to get weather data")

    # Create a directory to contain our calendars
    print("Creating directory `calendars/`")
    os.makedirs("calendars", exist_ok=True)

    # Write the events list as yaml files into the calendars directory
    daily_name = "cape-town-daily"
    print(f"Writing events to `calendars/{daily_name}.yaml`")
    pprint(daily)
    with open(f"calendars/{daily_name}.yaml", "w") as file:
        yaml.dump({"events": daily}, file)
    # Write the events list as yaml files into the calendars directory
    hourly_name = "cape-town-hourly"
    print(f"Writing events to `calendars/{hourly_name}.yaml`")
    pprint(hourly)
    with open(f"calendars/{hourly_name}.yaml", "w") as file:
        yaml.dump({"events": hourly}, file)

    print(f"Python script finished")


WWO_CODE = {
    "113": "Sunny",
    "116": "PartlyCloudy",
    "119": "Cloudy",
    "122": "VeryCloudy",
    "143": "Fog",
    "176": "LightShowers",
    "179": "LightSleetShowers",
    "182": "LightSleet",
    "185": "LightSleet",
    "200": "ThunderyShowers",
    "227": "LightSnow",
    "230": "HeavySnow",
    "248": "Fog",
    "260": "Fog",
    "263": "LightShowers",
    "266": "LightRain",
    "281": "LightSleet",
    "284": "LightSleet",
    "293": "LightRain",
    "296": "LightRain",
    "299": "HeavyShowers",
    "302": "HeavyRain",
    "305": "HeavyShowers",
    "308": "HeavyRain",
    "311": "LightSleet",
    "314": "LightSleet",
    "317": "LightSleet",
    "320": "LightSnow",
    "323": "LightSnowShowers",
    "326": "LightSnowShowers",
    "329": "HeavySnow",
    "332": "HeavySnow",
    "335": "HeavySnowShowers",
    "338": "HeavySnow",
    "350": "LightSleet",
    "353": "LightShowers",
    "356": "HeavyShowers",
    "359": "HeavyRain",
    "362": "LightSleetShowers",
    "365": "LightSleetShowers",
    "368": "LightSnowShowers",
    "371": "HeavySnowShowers",
    "374": "LightSleetShowers",
    "377": "LightSleet",
    "386": "ThunderyShowers",
    "389": "ThunderyHeavyRain",
    "392": "ThunderySnowShowers",
    "395": "HeavySnowShowers",
}

WEATHER_SYMBOL = {
    "Unknown": "✨",
    "Cloudy": "☁️",
    "Fog": "🌫",
    "HeavyRain": "🌧",
    "HeavyShowers": "🌧",
    "HeavySnow": "❄️",
    "HeavySnowShowers": "❄️",
    "LightRain": "🌦",
    "LightShowers": "🌦",
    "LightSleet": "🌧",
    "LightSleetShowers": "🌧",
    "LightSnow": "🌨",
    "LightSnowShowers": "🌨",
    "PartlyCloudy": "⛅️",
    "Sunny": "☀️",
    "ThunderyHeavyRain": "🌩",
    "ThunderyShowers": "⛈",
    "ThunderySnowShowers": "⛈",
    "VeryCloudy": "☁️",
}


if __name__ == "__main__":
    main()
