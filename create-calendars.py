import yaml
import os
import requests
from pprint import pprint


def main():
    daily = []
    hourly = []

    res = requests.get("http://wttr.in/Cape%20Town?format=j1")
    if res.ok:
        try:
            weather_data = res.json()
            pprint(weather_data.keys())
            for item in weather_data["weather"]:
                temp = item["avgtempC"]
                sunset = item["astronomy"][0]["sunset"]
                daily.append(
                    {
                        "title": f"{temp}°C",
                        "description": f"Sunset at {sunset}",
                        "start": item["date"],
                        "end": item["date"],
                    }
                )
                for hr in item["hourly"]:
                    hour = int(hr["time"]) // 100
                    start = item["date"] + "T" + f"{hour:0>2}:00:00"
                    if hour + 3 == 24:
                        hour = 23
                        minute = 59
                    else:
                        minute = 0
                    end = item["date"] + "T" + f"{hour:0>2}:{minute:0>2}:00"
                    temp = hr["tempC"]
                    pressure = hr["pressure"]
                    hourly.append(
                        {
                            "title": f"{temp}°C, {pressure}hPa",
                            "description": f"no description",
                            "start": start,
                            "end": end,
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
    print(f"Writing events to `calendars/{daily_name}.yaml`:\n{daily}")
    with open(f"calendars/{daily_name}.yaml", "w") as file:
        yaml.dump({"events": daily}, file)
    # Write the events list as yaml files into the calendars directory
    hourly_name = "cape-town-hourly"
    print(f"Writing events to `calendars/{hourly_name}.yaml`:\n{hourly}")
    with open(f"calendars/{hourly_name}.yaml", "w") as file:
        yaml.dump({"events": hourly}, file)

    print(f"Python script finished")


if __name__ == "__main__":
    main()
