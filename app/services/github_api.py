import asyncio
import os
from fastapi import HTTPException
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Fetch all traffic data for a user's repositories
async def get_all_traffic_data(username: str):
    """
    Retrieves traffic data (clones and views) for all repositories of a GitHub user.

    Args:
        - username: The GitHub username whose repository traffic data is to be fetched.

    Returns:
       A dictionary containing traffic data for each day, including the number of clones and views.

    Raises:
        HTTPException: If any error occurs while fetching the data.
    """
    repos = await get_user_repos(username)  # Get the list of repositories for the user

    tasks = [get_repo_traffic(username, repo_name) for repo_name in repos]
    results = await asyncio.gather(*tasks)
    traffic_results = [{repo_name: result} for repo_name, result in zip(repos, results)]

    return traffic_results

# Fetch all repositories of a user
async def get_user_repos(username: str):
    """
    Retrieves all repository names for a specified GitHub user.

    Args:
        username: The GitHub username whose repositories are to be fetched.

    Returns:
        A list of repository names owned by the user.

    Raises:
        HTTPException: If any error occurs while fetching the repositories.
    """
    url = f"{BASE_URL}/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    repos = response.json()
    list_repos = [repo["name"] for repo in repos]

    return list_repos

# Fetch traffic data for a specific repository
async def get_repo_traffic(repo_owner, repo_name):
    """
    Retrieves traffic data (clones and views) for a specific repository.

    Args:
        - repo_owner: The owner of the repository.
        - repo_name: The name of the repository.

    Returns:
        A dictionary containing clones and views data for the repository.

    Raises:
        HTTPException: If any error occurs while fetching the traffic data.
    """
    clones_url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/traffic/clones"
    views_url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/traffic/views"

    try:
        clones_response = requests.get(clones_url, headers=HEADERS)
        views_response = requests.get(views_url, headers=HEADERS)

        clones_response.raise_for_status()
        views_response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code
        raise HTTPException(
            status_code=status_code,
            detail=f"HTTP error while fetching traffic data: {http_err.response.text}"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Network error while fetching traffic data: {str(e)}"
        )
    
    clones_data = clones_response.json()
    views_data = views_response.json()

    return {
        "clones": clones_data.get("clones", []),
        "views": views_data.get("views", []),
    }

# Fetch the profile name of the authenticated GitHub user
async def get_profile_name():
    """
    Retrieves the name of the authenticated GitHub user.

    Returns:
        The name of the authenticated GitHub user.

    Raises:
        HTTPException: If any error occurs while fetching the profile name.
    """
    url = f"{BASE_URL}/user"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    response_json = response.json()

    return response_json["name"]
