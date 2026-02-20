from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
import sqlite3
from datetime import datetime
import json

app = FastAPI(title="GitHub Profile Analyzer")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("search_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            searched_at TEXT NOT NULL,
            followers INTEGER,
            public_repos INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_search(username, followers, public_repos):
    conn = sqlite3.connect("search_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO searches (username, searched_at, followers, public_repos) VALUES (?, ?, ?, ?)",
        (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), followers, public_repos)
    )
    conn.commit()
    conn.close()

def get_recent_searches():
    conn = sqlite3.connect("search_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, searched_at FROM searches ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

# ---------- GitHub API Helpers ----------
async def fetch_github_user(username: str):
    async with httpx.AsyncClient() as client:
        headers = {"Accept": "application/vnd.github+json"}
        user_res = await client.get(f"https://api.github.com/users/{username}", headers=headers)
        if user_res.status_code == 404:
            return None, None, None
        user = user_res.json()

        repos_res = await client.get(
            f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated",
            headers=headers
        )
        repos = repos_res.json()

        return user, repos, None

def calculate_score(user, repos):
    score = 0
    score += min(user.get("followers", 0) * 2, 30)
    score += min(user.get("public_repos", 0), 20)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    score += min(total_stars * 3, 30)
    if user.get("bio"):
        score += 5
    if user.get("blog"):
        score += 5
    if user.get("location"):
        score += 5
    if user.get("email"):
        score += 5
    return min(score, 100)

def get_language_stats(repos):
    lang_count = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_count[lang] = lang_count.get(lang, 0) + 1
    sorted_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs[:6]

def get_top_repos(repos):
    sorted_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)
    return sorted_repos[:5]

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    recent = get_recent_searches()
    return templates.TemplateResponse("index.html", {"request": request, "recent": recent})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, username: str = Form(...)):
    user, repos, error = await fetch_github_user(username.strip())

    if user is None:
        recent = get_recent_searches()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"GitHub user '{username}' not found!",
            "recent": recent
        })

    score = calculate_score(user, repos)
    languages = get_language_stats(repos)
    top_repos = get_top_repos(repos)
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)

    save_search(username, user.get("followers", 0), user.get("public_repos", 0))

    lang_labels = json.dumps([l[0] for l in languages])
    lang_values = json.dumps([l[1] for l in languages])

    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": user,
        "score": score,
        "languages": languages,
        "top_repos": top_repos,
        "total_stars": total_stars,
        "lang_labels": lang_labels,
        "lang_values": lang_values,
    })