from fastapi import FastAPI, Query, Response, HTTPException, Request
from fastapi.responses import RedirectResponse
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timezone
import hashlib

load_dotenv(find_dotenv())

app = FastAPI()

cache = TTLCache(maxsize=10, ttl=1800)

@app.get("/")
def root():
    return RedirectResponse(url="https://github.com/FuseFairy/github-repo-traffic")

@app.get("/api")
async def get_traffic_chart(
    request: Request,
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., '00000000' for transparent black, 'FFFFFF' for white without '#')"),
    clones_color: str = Query(None, description="Color for clones line (e.g., 'FF5733' for orange-red without '#')"),
    views_color: str = Query(None, description="Color for views line (e.g., '33FF57' for green without '#')"),
    height: int = Query(400, ge=400, description="Chart height in pixels"),
    width: int = Query(800, ge=800, description="Chart width in pixels"),
    exclude_repos: str = Query(None, description="Comma-separated list of repository names to exclude from the chart")
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
        
        # Check if traffic data is already cached
        traffic_data_key = f"traffic_data_{username}"
        profile_name_key = f"profile_name_{username}"
        
        # Function to generate new data
        async def generate_new_data():
            if exclude_repos:
                exclude_repos_list = exclude_repos.split(",")
            else:
                exclude_repos_list = None
                
            traffic_data = await get_all_traffic_data(username, exclude_repos_list)
            profile_name = await get_profile_name()
            
            # Update cache
            cache[traffic_data_key] = traffic_data
            cache[profile_name_key] = profile_name
            
            return traffic_data, profile_name

        # Get or generate data
        if traffic_data_key in cache and profile_name_key in cache:
            traffic_data = cache[traffic_data_key]
            profile_name = cache[profile_name_key]
        else:
            traffic_data, profile_name = await generate_new_data()

        # Generate chart
        chart_svg = generate_chart(profile_name, traffic_data, theme, height, width, 
                                 bg_color, clones_color, views_color)
        
        # Generate ETag
        chart_hash = hashlib.md5(chart_svg).hexdigest()
        
        # If ETag matches, return 304 Not Modified
        if if_none_match and if_none_match == chart_hash:
            return Response(status_code=304)

        # Set headers
        headers = {
            "Cache-Control": "public, max-age=1800, must-revalidate",
            "Content-Disposition": "inline; filename=chart.svg",
            "ETag": chart_hash,
            "Last-Modified": datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        }

        return Response(
            content=chart_svg,
            media_type="image/svg+xml",
            headers=headers
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
