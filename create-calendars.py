import yaml
import os
import requests
from pprint import pprint


def main():
    events = []

    res = requests.get("http://wttr.in/Cape%20Town?format=j1")
    if res.ok:
        try:
            weather_data = res.json()
            pprint(weather_data.keys())
            for item in weather_data["weather"]:
                temp = item["avgtempC"]
                sunset = item["astronomy"][0]["sunset"]
                events.append(
                    {
                        "title": f"{temp}°C",
                        "description": f"Sunset at {sunset}",
                        "start": item["date"],
                        "end": item["date"],
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
    print(f"Writing events to `calendars/simple-calendar.yaml`:\n{events}")
    with open("calendars/simple-calendar.yaml", "w") as file:
        yaml.dump({"events": events}, file)

    print(f"Python script finished")


if __name__ == "__main__":
    main()
