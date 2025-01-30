import asyncio
import os
import httpx

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
    repos = await get_user_repos(username)

    async with httpx.AsyncClient(http2=True) as client:
        semaphore = asyncio.Semaphore(10)

        async def bounded_task(repo_name):
            async with semaphore:
                return await get_repo_traffic(username, repo_name, client)

        tasks = [bounded_task(repo) for repo in repos]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    valid_results = [
        {repo: result} 
        for repo, result in zip(repos, results) 
        if not isinstance(result, Exception)
    ]

    return valid_results

# Fetch all repositories of a user
async def get_user_repos(username: str):
    """
    Retrieves all public repository names for a specified GitHub user.

    Args:
        username: The GitHub username whose repositories are to be fetched.

    Returns:
        A list of repository names owned by the user.

    Raises:
        dict: A dictionary containing error message if any error occurs while fetching the repositories.
    """
    url = f"{BASE_URL}/users/{username}/repos"
    repos = []
    page = 1

    async with httpx.AsyncClient(http2=True) as client:
        while True:
            try:
                response = await client.get(
                    url,
                    headers=HEADERS,
                    params={"page": page, "per_page": 100, "type": "public"}
                )
                response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses

                current_repos = response.json()
                if not current_repos:
                    break

                repos.extend([repo["name"] for repo in current_repos])

                if "next" not in response.links:
                    break

                page += 1

            except httpx.HTTPStatusError as http_err:
                raise Exception(f"HTTP error: {http_err.response.status_code} - {http_err.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Network error: {str(e)}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")

    return repos

# Fetch traffic data for a specific repository
async def get_repo_traffic(repo_owner, repo_name, client: httpx.AsyncClient):
    """
    Retrieves traffic data (clones and views) for a specific repository.

    Args:
        - repo_owner: The owner of the repository.
        - repo_name: The name of the repository.

    Returns:
        A dictionary containing clones and views data for the repository.

    Raises:
        Exception: If any error occurs while fetching the traffic data.
    """
    clones_url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/traffic/clones"
    views_url = f"{BASE_URL}/repos/{repo_owner}/{repo_name}/traffic/views"

    try:
        clones_res, views_res = await asyncio.gather(
            client.get(clones_url, headers=HEADERS),
            client.get(views_url, headers=HEADERS)
        )
        clones_res.raise_for_status()
        views_res.raise_for_status()

    except httpx.HTTPStatusError as e:
        raise Exception(f"Error for {repo_name}: HTTP {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise Exception(f"Unexpected error for {repo_name}: {str(e)}")

    try:
        clones_data = clones_res.json().get("clones", [])
        views_data = views_res.json().get("views", [])
    except ValueError as e:
        raise Exception(f"JSON decode error for {repo_name}: {str(e)}")

    return {"clones": clones_data, "views": views_data}

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
    
    try:
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.get(url, headers=HEADERS)
        
        response.raise_for_status()
        
        response_json = response.json()
    
    except httpx.HTTPStatusError as http_err:
        raise Exception(f"HTTP error: {http_err.response.status_code} - {http_err.response.text}")
    except httpx.RequestError as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

    return response_json["name"]
