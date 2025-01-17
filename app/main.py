from fastapi import FastAPI, Query, Response, HTTPException
from cachetools import TTLCache
from app.services.github_api import get_all_traffic_data, get_profile_name
from app.services.chart_generator import generate_chart
import hashlib

app = FastAPI()

# Create a TTL (time-to-live) cache with a max size of 1 and expiration time of 86400 seconds (24 hours)
cache = TTLCache(maxsize=10, ttl=86400)  # Cache for 24 hours, increase maxsize to allow more cached items

@app.get("/")
def root():
    return {"message": "Welcome to GitHub Traffic Stats API"}

@app.get("/api")
def get_traffic_chart(
    username: str = Query(..., description="GitHub username"),
    theme: str = Query("default", description="Chart theme (e.g., 'tokyo-night')"),
    bg_color: str = Query(None, description="Background color (e.g., '00000000' for transparent black, 'FFFFFF' for white without '#')"),
    height: int = Query(400, ge=400, description="Chart height in pixels"),
    width: int = Query(800, ge=800, description="Chart width in pixels")
):
    """
    Endpoint to get the traffic chart for a GitHub user's repository.
    It fetches traffic data from the GitHub API and generates a chart in SVG format.
    
    Args:
    - username: GitHub username whose traffic data is to be fetched.
    - theme: The theme to be applied to the chart.
    - bg_color: Optional background color for the chart.
    - height: Height of the chart.
    - width: Width of the chart.

    Returns:
    - A response containing the chart in SVG format.
    """
    try:
        # Generate a unique cache key based on the request parameters
        cache_key = generate_cache_key(username, theme, height, width, bg_color)

        # Check if the traffic data is cached for this unique combination
        if cache_key in cache:
            chart_svg = cache[cache_key]  # Retrieve the cached chart
        else:
            # Fetch new traffic data
            traffic_data = get_all_traffic_data(username)
            profile_name = get_profile_name()  # Get the profile name
            
            # Generate the chart
            chart_svg = generate_chart(profile_name, traffic_data, theme, height, width, bg_color)

            # Store the generated chart in the cache
            cache[cache_key] = chart_svg

        # Return the chart as an SVG response
        return Response(content=chart_svg, media_type="image/svg+xml", headers={"Content-Disposition": "inline; filename=chart.svg"})

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))  # Raise 404 if theme file is not found
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")  # Raise 500 for other errors

def generate_cache_key(username, theme, height, width, bg_color):
    """
    Generate a unique cache key based on the request parameters.
    """
    # Concatenate the parameters to form a string, and then hash it to generate a unique key
    key_string = f"{username}-{theme}-{height}-{width}-{bg_color}"
    return hashlib.md5(key_string.encode()).hexdigest()  # Use MD5 to generate a short, unique key