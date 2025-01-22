from fastapi import FastAPI, Query, Response, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.concurrency import run_in_threadpool
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
from dotenv import load_dotenv, find_dotenv
import asyncio
import traceback
import hashlib
import json
import os

load_dotenv(find_dotenv())

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
USER_TRAFFIC_CACHE_KEY = f"traffic_data_{GITHUB_USERNAME}"
USER_PROFILE_CACHE_KEY = f"profile_name_{GITHUB_USERNAME}" 

user_traffic_cache = TTLCache(maxsize=2, ttl=7200)
chart_svg_cache = TTLCache(maxsize=10, ttl=7200)

traffic_data_lock = asyncio.Lock()

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="https://github.com/FuseFairy/github-repo-traffic")

@app.get("/api")
async def get_traffic_chart(
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
        chart_cache_key = _generate_cache_key(
            username=GITHUB_USERNAME,
            theme=theme,
            bg_color=bg_color,
            clones_color=clones_color,
            views_color=views_color,
            clones_point_color=clones_point_color,
            views_point_color=views_point_color,
            radius=radius,
            height=height,
            width=width,
            exclude_repos=exclude_repos,
            ticks=ticks
        )

        # Get or generate data
        if USER_TRAFFIC_CACHE_KEY not in user_traffic_cache:
            await generate_new_data(USER_TRAFFIC_CACHE_KEY, USER_PROFILE_CACHE_KEY)

        if chart_cache_key not in chart_svg_cache:
            profile_name = user_traffic_cache[USER_PROFILE_CACHE_KEY]
            traffic_results = user_traffic_cache[USER_TRAFFIC_CACHE_KEY]
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
            try:
                chart_svg = await asyncio.wait_for(
                    run_in_threadpool(generate_chart, **chart_params),
                    timeout=8
                )
                chart_svg_cache[chart_cache_key] = chart_svg
            except asyncio.TimeoutError:
                raise HTTPException(504, "Chart generation timeout")

        chart_svg = chart_svg_cache[chart_cache_key]

        # Set headers
        headers = {
            "Content-Type": "image/svg+xml; charset=utf-8",
            "Cache-Control": "public, max-age=7200, s-maxage=7200, stale-while-revalidate=86400"
        }

        return Response(
            content=chart_svg,
            media_type="image/svg+xml",
            headers=headers
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}\nStack trace: {traceback.format_exc()}"
        )

def _generate_cache_key(**params) -> str:
    default_values = {
        "theme": "default",
        "radius": 20,
        "height": 400,
        "width": 800,
        "ticks": 5,
        "bg_color": None,
        "clones_color": None,
        "views_color": None,
        "clones_point_color": None,
        "views_point_color": None,
        "exclude_repos": None
    }
    filtered_params = {k: v for k, v in params.items() if v != default_values.get(k)}
    return hashlib.md5(json.dumps(filtered_params, sort_keys=True).encode()).hexdigest()

# Function to generate new data
async def generate_new_data(USER_TRAFFIC_CACHE_KEY, USER_PROFILE_CACHE_KEY):
    print("Generating new data...")

    async with traffic_data_lock:
        # check again, avoid race condition
        if USER_TRAFFIC_CACHE_KEY not in user_traffic_cache:
            traffic_results, profile_name = await asyncio.gather(
                get_all_traffic_data(GITHUB_USERNAME),
                get_profile_name()
            )

            # Update cache
            user_traffic_cache[USER_TRAFFIC_CACHE_KEY] = traffic_results
            user_traffic_cache[USER_PROFILE_CACHE_KEY] = profile_name
