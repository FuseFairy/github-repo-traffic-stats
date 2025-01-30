import asyncio
import os
import yaml
from src.services.github_api import get_all_traffic_data, get_profile_name
from src.services.chart_generator import generate_chart

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
traffic_data_lock = asyncio.Lock()

def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

async def generate_new_data():
    print("Fetching GitHub traffic data...")

    async with traffic_data_lock:
        traffic_results, profile_name = await asyncio.gather(
            get_all_traffic_data(GITHUB_USERNAME),
            get_profile_name()
        )
        return traffic_results, profile_name

async def main():
    try:
        config = load_config()
        traffic_results, profile_name = await generate_new_data()

        chart_params = {
            "profile_name": profile_name,
            "traffic_results": traffic_results,
            **config
        }

        print("Generating chart...")
        chart_svg = generate_chart(**chart_params)

        os.makedirs("generated", exist_ok=True)
        with open("generated/traffic_chart.svg", "w", encoding="utf-8") as f:
            f.write(chart_svg)
        print(f"SVG saved finished!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
