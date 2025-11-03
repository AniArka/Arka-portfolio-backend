from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "AniArka")
GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

async def fetch_repos():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(GITHUB_API, headers=headers)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch GitHub repos")
        return r.json()

@router.get("/")
async def list_repos():
    repos = await fetch_repos()
    out = []
    for repo in repos:
        out.append({
            "name": repo.get("name"),
            "html_url": repo.get("html_url"),
            "description": repo.get("description") or "",
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count", 0),
        })
    # sort by stargazers desc, then name (optional)
    out.sort(key=lambda x: (-x["stargazers_count"], x["name"].lower()))
    return out
