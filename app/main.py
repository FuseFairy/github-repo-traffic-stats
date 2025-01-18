from contextlib import asynccontextmanager
import traceback
from fastapi import FastAPI, Query, Response, HTTPException, Request
from fastapi.responses import RedirectResponse
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
from dotenv import load_dotenv, find_dotenv
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv(find_dotenv())

cache = TTLCache(maxsize=10, ttl=float('inf'))

# Background Scheduler setup
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    print("Scheduler started.")
    try:
        yield
    finally:
        print("Shutting down scheduler...")
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

def schedule_update_data(username, exclude_repos, traffic_data_key, profile_name_key):
    print("Scheduling periodic data update...")
    if exclude_repos:
        exclude_repos_list = exclude_repos.split(",")
    else:
        exclude_repos_list = None

    scheduler.add_job(generate_new_data, 'interval', minutes=29, id=username,
                      args=[username, exclude_repos_list, traffic_data_key, profile_name_key], replace_existing=True)

@app.get("/")
def root():
    return RedirectResponse(url="https://github.com/FuseFairy/github-repo-traffic")

@app.get("/api")
def get_traffic_chart(
    request: Request,
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., '00000000' for transparent black, 'FFFFFF' for white without '#')"),
    clones_color: str = Query(None, description="Color for clones line (e.g., 'FF5733' for orange-red without '#')"),
    views_color: str = Query(None, description="Color for views line (e.g., '33FF57' for green without '#')"),
    height: int = Query(400, ge=400, description="Chart height in pixels"),
    width: int = Query(800, ge=800, description="Chart width in pixels"),
    exclude_repos: str = Query(None, description="Comma-separated list of repository names to exclude from the chart"),
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
        - height: Height of the chart.
        - width: Width of the chart.
        - exclude_repos: Comma-separated list of repository names to exclude from the chart.

    Returns:
        A response containing the chart in SVG format.
    """
    try:
        # Get If-None-Match header (client's ETag)
        if_none_match = request.headers.get("If-None-Match")

        cache_key_parts = [username]
        if exclude_repos:
            cache_key_parts.append(exclude_repos)
        cache_key = '_'.join(cache_key_parts)
        
        # Check if traffic data is already cached
        traffic_data_key = f"traffic_data_{cache_key}"
        profile_name_key = f"profile_name_{cache_key}"

        # Get or generate data
        if traffic_data_key not in cache and profile_name_key not in cache:
            generate_new_data(username, exclude_repos, traffic_data_key, profile_name_key)
            schedule_update_data(username, exclude_repos, traffic_data_key, profile_name_key)

        traffic_data = cache[traffic_data_key]
        profile_name = cache[profile_name_key]

        # Generate chart
        chart_svg = generate_chart(profile_name, traffic_data, theme, height, width, bg_color, clones_color, views_color)
        
        # Generate ETag
        chart_hash = hashlib.md5(chart_svg).hexdigest()
        
        # If ETag matches, return 304 Not Modified
        if if_none_match and if_none_match == chart_hash:
            return Response(status_code=304)

        # Set headers
        headers = {
            "Content-Type": "image/svg+xml; charset=utf-8",
            "Cache-Control": "public, max-age=1800, must-revalidate",
            "ETag": chart_hash
        }

        return Response(
            content=chart_svg,
            media_type="image/svg+xml",
            headers=headers
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Detailed Stack Trace:")
        print(traceback.format_exc())
        
        raise HTTPException(status_code=500, detail="Internal server error")

# Function to generate new data
def generate_new_data(username, exclude_repos, traffic_data_key, profile_name_key):
    print("Generating new data...")
    if exclude_repos:
        exclude_repos_list = exclude_repos.split(",")
    else:
        exclude_repos_list = None
        
    traffic_data = get_all_traffic_data(username, exclude_repos_list)
    profile_name = get_profile_name()
    
    # Update cache
    cache[traffic_data_key] = traffic_data
    cache[profile_name_key] = profile_name
