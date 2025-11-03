from fastapi import APIRouter, HTTPException
import httpx
import os
import asyncio

router = APIRouter()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "AniArka")
GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

async def fetch_repos():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"  # use token if available

    retries = 3  # retry a few times in case of transient Render network issues
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.get(GITHUB_API, headers=headers)
                if r.status_code == 200:
                    return r.json()
                else:
                    # log the exact response for debugging
                    print(f"[Attempt {attempt+1}] GitHub error {r.status_code}: {r.text}")
        except httpx.RequestError as e:
            print(f"[Attempt {attempt+1}] Request error: {e}")
        await asyncio.sleep(2 * (attempt + 1))  # exponential backoff

    # if all retries fail
    raise HTTPException(status_code=502, detail="Failed to fetch GitHub repos after retries")

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
    out.sort(key=lambda x: (-x["stargazers_count"], x["name"].lower()))
    return out
