from fastapi import FastAPI, Query, Response, HTTPException
from fastapi.responses import RedirectResponse
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
from dotenv import load_dotenv, find_dotenv
from app.utils.logger import logger
import asyncio

load_dotenv(find_dotenv())

data_cache = TTLCache(maxsize=1, ttl=1800)
chart_cache = TTLCache(maxsize=10, ttl=1800)
data_lock = asyncio.Lock()

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="https://github.com/FuseFairy/github-repo-traffic")

@app.get("/api")
async def get_traffic_chart(
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., '00000000' for transparent black, 'FFFFFF' for white without '#')"),
    clones_color: str = Query(None, description="Color for clones line (e.g., 'FF5733' for orange-red without '#')"),
    views_color: str = Query(None, description="Color for views line (e.g., '33FF57' for green without '#')"),
    clones_point_color: str = Query(None, description="Color for clone points (e.g., 'FF5733' for orange-red without '#')"),
    views_point_color: str = Query(None, description="Color for view points (e.g., '33FF57' for green without '#')"),
    radius: int = Query(20, description="Corner radius for the chart's rectangular background"),
    height: int = Query(400, ge=400, description="Chart height in pixels"),
    width: int = Query(800, ge=800, description="Chart width in pixels"),
    exclude_repos: str = Query(None, description="Comma-separated list of repository names to exclude from the chart"),
    ticks: int = Query(5,ge=5, description="Number of y-axis ticks"),
):
    """
    Endpoint to get the traffic chart for a GitHub user's repository.
    It fetches traffic data from the GitHub API and generates a chart in SVG format.
    
    Args:
        - username: GitHub username whose traffic data is to be fetched.
        - theme: The theme to be applied to the chart.
        - bg_color: Optional background color for the chart.
        - clones_color: Optional clones stroke color for the chart.
        - views_color: Optional views stroke color for the chart.
        - clones_point_color: Optional clones point color for the chart.
        - views_point_color: Optional views point color for the chart.
        - radius: Corner radius for the chart's rectangular background.
        - height: Height of the chart.
        - width: Width of the chart.
        - exclude_repos: Comma-separated list of repository names to exclude from the chart.
        - ticks: Number of y-axis ticks.

    Returns:
        A response containing the chart in SVG format.
    """
    try:
        chart_cache_key = f"{username}_{theme}_{bg_color}_{clones_color}_{views_color}_{clones_point_color}_{views_point_color}_{radius}_{height}_{width}_{exclude_repos}_{ticks}"
        
        # Check if traffic data is already cached
        traffic_results_key = f"traffic_data_{username}"
        profile_name_key = f"profile_name_{username}"

        # Get or generate data
        if traffic_results_key not in data_cache and profile_name_key not in data_cache:
            async with data_lock:
                # chack again to avoid race condition
                if traffic_results_key not in data_cache and profile_name_key not in data_cache:
                    await generate_new_data(username, traffic_results_key, profile_name_key)

        if chart_cache_key not in chart_cache:
            traffic_results = data_cache[traffic_results_key]
            profile_name = data_cache[profile_name_key]

            chart_params = {
                "profile_name": profile_name,
                "traffic_results": traffic_results,
                "theme": theme,
                "height": height,
                "width": width,
                "radius": radius,
                "ticks": ticks,
                "bg_color": bg_color,
                "clones_color": clones_color,
                "views_color": views_color,
                "clones_point_color": clones_point_color,
                "views_point_color": views_point_color,
                "exclude_repos": exclude_repos
            }
            
            # Generate chart
            chart_cache[chart_cache_key] = generate_chart(**chart_params)

        
        chart_svg = chart_cache[chart_cache_key]

        # Set headers
        headers = {
            "Content-Type": "image/svg+xml; charset=utf-8",
            "Cache-Control": "public, max-age=0, s-maxage=1800, stale-while-revalidate=86400"
        }

        return Response(
            content=chart_svg,
            media_type="image/svg+xml",
            headers=headers
        )

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Function to generate new data
async def generate_new_data(username, traffic_results_key, profile_name_key):
    logger.info("Generating new data...")
    traffic_results = await get_all_traffic_data(username)
    profile_name = await get_profile_name()
    
    # Update cache
    data_cache[traffic_results_key] = traffic_results
    data_cache[profile_name_key] = profile_name
