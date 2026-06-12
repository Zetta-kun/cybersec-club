cd C:\Users\Nitro-2026\Desktop\club_db

$readme = @"
# 🛡️ CyberSec Club - Professional CTF Platform

A full-stack Capture The Flag (CTF) platform with Codeforces-style ELO rating system for cybersecurity enthusiasts.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![React](https://img.shields.io/badge/react-18-blue)
![FastAPI](https://img.shields.io/badge/fastapi-latest-teal)

## 🎯 Features

### 🏆 Rating System
- ELO-based dynamic rating (Codeforces/Glicko algorithm)
- 10 distinct ranks: Newbie → Legendary Grandmaster
- Rating history tracking
- First Blood bonus (+10% points)

### 🚩 CTF Challenges
- **10 Categories**: Web, Crypto, Forensics, Reverse, PWN, OSINT, Mobile, Cloud, Blockchain, Misc
- **5 Difficulty Levels**: Easy, Medium, Hard, Expert, Insane
- **Dynamic Scoring**: Points decrease as more users solve
- **Solve Rate**: Statistics for each challenge
- Flag validation (SHA-256)

### 🏁 Competition System
- Timed competitions
- Join/leave competitions
- Competition leaderboard

### 💡 Feature Request Box
- Users can submit new challenge/feature requests
- Voting system (upvote)
- Admin approval workflow

### ⚙️ Admin Dashboard
- 📊 Dashboard analytics
- 👥 User management
- 🏆 Challenge CRUD operations
- 📅 Competition management
- 💡 Request management

## 🛠 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python 3.12, FastAPI |
| Frontend | React 18, Vite, TailwindCSS |
| Database | In-memory (demo) / PostgreSQL (production) |
| Auth | JWT + bcrypt |
| Deployment | Docker, Nginx |

## 📸 Screenshots

### Home Page
![Home](screenshots/home.png)

### Challenges
![Challenges](screenshots/challenges.png)

### Leaderboard
![Leaderboard](screenshots/leaderboard.png)

### Admin Panel
![Admin](screenshots/admin.png)

## 📦 Installation

### Quick Start (Demo)

```bash
# Clone the repository
git clone https://github.com/your-username/cybersec-club.git
cd cybersec-club

# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]
uvicorn simple_backend:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev


🌐 Access Points
Service	URL
Frontend	http://localhost:3000
Backend API	http://localhost:8000
API Documentation	http://localhost:8000/docs

👤 Default Credentials
Username	Password	Role
admin	Admin123!@#	Super Admin


📁 Project Structure

club_db/
├── backend/                    # Python FastAPI backend
│   ├── api/v1/endpoints/      # REST API endpoints
│   ├── core/                  # Core modules (config, security, database)
│   ├── models/                # SQLAlchemy database models
│   ├── schemas/               # Pydantic validation schemas
│   └── services/              # Business logic layer
├── frontend/                  # React frontend
│   └── src/
│       ├── components/        # Reusable UI components
│       ├── pages/             # Page components
│       ├── services/          # API service layer
│       └── hooks/             # Custom React hooks
├── database/                  # SQL migration files
├── nginx/                     # Nginx configuration
├── scripts/                   # Setup and deployment scripts
├── simple_backend.py          # Standalone demo backend
├── docker-compose.yml         # Docker configuration
└── Dockerfile                 # Docker image



📝 License

MIT License - Free to use, modify, and distribute


👨‍💻 Author

Zetta-kun