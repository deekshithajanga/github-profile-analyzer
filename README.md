# 🔍 GitHub Profile Analyzer

A full-stack web application that analyzes any GitHub profile and generates insights including language breakdown, top repositories, and a custom developer score.

## 🚀 Live Demo
> Search any GitHub username and get instant analytics

## ✨ Features

- **Developer Score** — Custom scoring algorithm based on followers, repos, stars, and profile completeness
- **Language Breakdown** — Interactive doughnut chart showing top programming languages
- **Top Repositories** — Ranked by stars with metadata
- **Search History** — Tracks recent searches using SQLite
- **Real-time Data** — Fetches live data directly from GitHub REST API

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | SQLite |
| Frontend | HTML5, Bootstrap 5, Chart.js |
| API | GitHub REST API v3 |
| Server | Uvicorn (ASGI) |

## 📁 Project Structure

```
github-profile-analyzer/
├── app/
│   ├── main.py          # FastAPI routes and business logic
│   ├── templates/
│   │   ├── index.html   # Search page
│   │   └── result.html  # Results dashboard
│   └── static/          # Static assets
├── run.py               # Application entry point
└── requirements.txt     # Python dependencies
```

## ⚙️ Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/deekshithajanga/github-profile-analyzer.git
cd github-profile-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py

# Visit http://localhost:8000
```

## 📊 How the Developer Score Works

The score (0–100) is calculated based on:
- **Followers** — Up to 30 points
- **Public Repositories** — Up to 20 points  
- **Total Stars** — Up to 30 points
- **Profile Completeness** — Up to 20 points (bio, website, location, email)

## 🔮 Future Improvements

- [ ] Compare two GitHub profiles side by side
- [ ] AI-powered profile roast & feedback
- [ ] Contribution streak analysis
- [ ] Deploy on Render/Railway

## 👩‍💻 Author

**Deekshitha Reddy Janga**  
[GitHub](https://github.com/deekshithajanga) • [LinkedIn](https://www.linkedin.com/in/deekshithajanga/)