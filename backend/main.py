from fastapi import FastAPI, HTTPException
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