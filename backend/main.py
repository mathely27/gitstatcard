from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pathlib import Path
import requests
app = FastAPI()
@app.get("/")
def home():
    return {
        "message": "GitStatCard backend is running"
    }
@app.get("/api/user/{username}")
def get_user(username: str):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="GitHub user not found"
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch data from GitHub"
        )
    data = response.json()
    return {
    "name": data.get("name") or data["login"],
    "username": data["login"],
    "profile_picture": data["avatar_url"],
    "total_repos": data["public_repos"],
    "followers": data["followers"],
    "following": data["following"]
}
@app.get("/api/card/{username}")
def get_card(username: str):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="GitHub user not found"
        )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch data from GitHub"
        )
    data = response.json()
    svg_path = Path(__file__).parent.parent / "cards" / "github-dark.svg"
    svg = svg_path.read_text(encoding="utf-8")
    svg = svg.replace("{{NAME}}", data.get("name") or data["login"])
    svg = svg.replace("{{USERNAME}}", data["login"])
    svg = svg.replace("{{PROFILE_PICTURE}}", data["avatar_url"])
    svg = svg.replace("{{TOTAL_REPOS}}", str(data["public_repos"]))
    svg = svg.replace("{{FOLLOWERS}}", str(data["followers"]))
    svg = svg.replace("{{COMMITS}}", "Coming soon")
    svg = svg.replace("{{STARS}}", "Coming soon")
    svg = svg.replace("{{CURRENT_STREAK}}", "0")
    svg = svg.replace("{{MAX_STREAK}}", "0")

    return Response(
        content=svg,
        media_type="image/svg+xml"
    )