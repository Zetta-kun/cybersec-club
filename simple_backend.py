from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid
import json

app = FastAPI(title="CyberSec Club API", version="4.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

SECRET_KEY = "cybersec-secret-2024"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# Yaddaş bazası
users_db = {}
challenges_db = {}
submissions_db = []
contests_db = {}
contest_participants = {}
wishlist_db = []  # İstək qutusu

# Modeller
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class FlagSubmit(BaseModel):
    challenge_id: str
    flag: str

class ChallengeCreate(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    base_points: int = 100
    flag: str
    tags: List[str] = []

class ContestCreate(BaseModel):
    title: str
    description: str
    start_time: str  # ISO format
    end_time: str    # ISO format
    challenge_ids: List[str] = []

class WishlistItem(BaseModel):
    title: str
    description: str = ""
    category: str = "other"

# Default admin
users_db["admin"] = {
    "id": str(uuid.uuid4()),
    "username": "admin",
    "email": "admin@cybersec.az",
    "password_hash": pwd_context.hash("Admin123!@#"),
    "full_name": "System Admin",
    "rating": 2500,
    "max_rating": 2500,
    "total_solved": 0,
    "total_points": 0,
    "role": "super_admin",
    "rating_history": [{"date": datetime.utcnow().isoformat(), "rating": 2500}],
    "created_at": datetime.utcnow().isoformat()
}

# Default challenges
default_challenges = [
    {"title": "SQL Injection Basics", "description": "Find the SQL injection vulnerability. Try: admin' OR '1'='1' --", "category": "web_exploitation", "difficulty": "easy", "base_points": 100, "flag": "CTF{sql_injection_master}", "tags": ["web", "sql"]},
    {"title": "XSS Challenge", "description": "Find XSS vulnerability in the comment section. Use: <script>alert(1)</script>", "category": "web_exploitation", "difficulty": "easy", "base_points": 100, "flag": "CTF{xss_found}", "tags": ["web", "xss"]},
    {"title": "RSA Weak Key", "description": "Decrypt RSA with weak key. n=3233, e=17, c=855", "category": "cryptography", "difficulty": "medium", "base_points": 200, "flag": "CTF{rsa_crack_success}", "tags": ["crypto", "rsa"]},
    {"title": "Hash Cracking", "description": "Crack MD5 hash: 5d41402abc4b2a76b9719d911017c592", "category": "cryptography", "difficulty": "easy", "base_points": 50, "flag": "CTF{hello}", "tags": ["crypto", "hash"]},
    {"title": "Memory Dump", "description": "Analyze memory dump using Volatility. Find the hidden process.", "category": "forensics", "difficulty": "hard", "base_points": 300, "flag": "CTF{memory_analysis_pro}", "tags": ["forensics", "memory"]},
    {"title": "Buffer Overflow", "description": "Exploit buffer overflow. Offset is 40 bytes. Return address: 0xdeadbeef", "category": "binary_exploitation", "difficulty": "hard", "base_points": 350, "flag": "CTF{b0f_master}", "tags": ["pwn", "buffer"]},
    {"title": "OSINT Challenge", "description": "Find the flag from this Twitter profile: @cyberflag_hunter", "category": "osint", "difficulty": "medium", "base_points": 150, "flag": "CTF{osint_pro}", "tags": ["osint", "social"]},
    {"title": "Git Secrets", "description": "Find exposed credentials in this GitHub repo: github.com/test/secret-project", "category": "osint", "difficulty": "easy", "base_points": 75, "flag": "CTF{git_exposed}", "tags": ["osint", "git"]},
]

for i, ch in enumerate(default_challenges, 1):
    cid = str(i)
    challenges_db[cid] = {
        "id": cid,
        "title": ch["title"],
        "slug": ch["title"].lower().replace(" ", "-"),
        "description": ch["description"],
        "category": ch["category"],
        "difficulty": ch["difficulty"],
        "base_points": ch["base_points"],
        "current_points": ch["base_points"],
        "total_solves": 0,
        "total_attempts": 0,
        "tags": ch["tags"],
        "author_id": users_db["admin"]["id"],
        "created_at": datetime.utcnow().isoformat()
    }

# Flag yoxlama
def check_flag(challenge_id, flag):
    for ch in default_challenges:
        cid = str(default_challenges.index(ch) + 1)
        if cid == challenge_id and flag.strip() == ch["flag"]:
            return True
    if challenge_id in challenges_db:
        ch_title = challenges_db[challenge_id]["title"]
        for dch in default_challenges:
            if dch["title"] == ch_title and flag.strip() == dch["flag"]:
                return True
    return False

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username and username in users_db:
            return users_db[username]
    except JWTError:
        pass
    return None

def is_admin(user):
    return user and user.get("role") in ["admin", "super_admin"]

# ==================== AUTH ====================
@app.post("/api/v1/auth/register")
async def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(400, "Bu istifadeci adi artiq movcuddur")
    if len(user.password) < 8:
        raise HTTPException(400, "Shifre minimum 8 simvol olmalidir")
    
    users_db[user.username] = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "password_hash": pwd_context.hash(user.password),
        "full_name": user.full_name,
        "rating": 1000,
        "max_rating": 1000,
        "total_solved": 0,
        "total_points": 0,
        "role": "user",
        "rating_history": [{"date": datetime.utcnow().isoformat(), "rating": 1000}],
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {"id": users_db[user.username]["id"], "username": user.username, "email": user.email, "full_name": user.full_name, "rating": 1000, "max_rating": 1000, "total_solved": 0, "total_points": 0, "role": "user", "is_verified": True, "created_at": users_db[user.username]["created_at"]}

@app.post("/api/v1/auth/login")
async def login(login_data: UserLogin):
    user = users_db.get(login_data.username)
    if not user or not pwd_context.verify(login_data.password, user["password_hash"]):
        raise HTTPException(401, "Istifadeci adi ve ya shifre yanlishdir")
    
    access_token = jwt.encode({"sub": login_data.username, "exp": datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": access_token, "refresh_token": access_token, "token_type": "bearer", "expires_in": 604800, "user": {"id": user["id"], "username": user["username"], "email": user["email"], "full_name": user["full_name"], "rating": user["rating"], "max_rating": user["max_rating"], "total_solved": user["total_solved"], "total_points": user["total_points"], "role": user["role"], "is_verified": True, "created_at": user["created_at"]}}

# ==================== CHALLENGES ====================
@app.get("/api/v1/challenges/")
async def get_challenges(category: Optional[str] = Query(None), difficulty: Optional[str] = Query(None), search: Optional[str] = Query(None), current_user = Depends(get_current_user)):
    challenges = []
    for cid, challenge in challenges_db.items():
        if category and challenge.get("category") != category: continue
        if difficulty and challenge.get("difficulty") != difficulty: continue
        if search and search.lower() not in challenge.get("title", "").lower(): continue
        
        ch = challenge.copy()
        # Həll faizi
        total = ch["total_attempts"] if ch["total_attempts"] > 0 else 1
        ch["solve_rate"] = round((ch["total_solves"] / total) * 100, 1)
        
        if current_user:
            solved = any(s["username"] == current_user["username"] and s["challenge_id"] == cid for s in submissions_db)
            ch["is_solved"] = solved
        challenges.append(ch)
    
    return {"challenges": challenges, "total": len(challenges), "page": 1, "pages": 1}

@app.get("/api/v1/challenges/{challenge_id}")
async def get_challenge(challenge_id: str, current_user = Depends(get_current_user)):
    challenge = challenges_db.get(challenge_id)
    if not challenge: raise HTTPException(404, "Challenge tapilmadi")
    ch = challenge.copy()
    total = ch["total_attempts"] if ch["total_attempts"] > 0 else 1
    ch["solve_rate"] = round((ch["total_solves"] / total) * 100, 1)
    if current_user:
        solved = any(s["username"] == current_user["username"] and s["challenge_id"] == challenge_id for s in submissions_db)
        ch["is_solved"] = solved
    return ch

@app.post("/api/v1/challenges/solve")
async def submit_flag(submit: FlagSubmit, request: Request, current_user = Depends(get_current_user)):
    if not current_user: raise HTTPException(401, "Daxil olun")
    
    challenge = challenges_db.get(submit.challenge_id)
    if not challenge: raise HTTPException(404, "Challenge tapilmadi")
    
    already = any(s["username"] == current_user["username"] and s["challenge_id"] == submit.challenge_id for s in submissions_db)
    if already: raise HTTPException(400, "Bu suali artiq hell etmisiniz")
    
    if check_flag(submit.challenge_id, submit.flag):
        submissions_db.append({"username": current_user["username"], "challenge_id": submit.challenge_id, "timestamp": datetime.utcnow().isoformat()})
        challenge["total_solves"] += 1
        challenge["total_attempts"] += 1
        current_user["total_solved"] += 1
        points = challenge["current_points"]
        current_user["total_points"] += points
        
        # Rating artımı
        old_rating = current_user["rating"]
        rating_increase = int(points * 0.5)
        current_user["rating"] += rating_increase
        current_user["max_rating"] = max(current_user["max_rating"], current_user["rating"])
        current_user["rating_history"].append({"date": datetime.utcnow().isoformat(), "rating": current_user["rating"]})
        
        # Dinamik xal azalması
        if challenge["total_solves"] > 1:
            challenge["current_points"] = max(int(challenge["base_points"] * 0.3), challenge["current_points"] - 5)
        
        return {"status": "correct", "message": f"✅ Tebrikler! +{points} XP, +{rating_increase} Rating!", "points_earned": points, "is_first_blood": challenge["total_solves"] == 1, "attempts": 1}
    else:
        challenge["total_attempts"] += 1
        return {"status": "incorrect", "message": "❌ Yanlish flag! Yeniden cehd edin!", "attempts": 1}

# ==================== USER & LEADERBOARD ====================
@app.get("/api/v1/users/me")
async def get_profile(current_user = Depends(get_current_user)):
    if not current_user: raise HTTPException(401, "Daxil olun")
    user = current_user.copy()
    # Həll etdiyi sualları tap
    solved_challenges = []
    for s in submissions_db:
        if s["username"] == user["username"]:
            ch = challenges_db.get(s["challenge_id"], {})
            solved_challenges.append({"id": s["challenge_id"], "title": ch.get("title", ""), "points": ch.get("current_points", 0), "category": ch.get("category", "")})
    user["solved_challenges"] = solved_challenges
    return user

@app.get("/api/v1/leaderboard/")
async def get_leaderboard():
    users = sorted(users_db.values(), key=lambda u: u["rating"], reverse=True)
    leaderboard = []
    for idx, user in enumerate(users[:50], 1):
        r = user["rating"]
        if r >= 3000: rank_name, rank_color = "Legendary Grandmaster", "#AA0000"
        elif r >= 2400: rank_name, rank_color = "Grandmaster", "#FF7777"
        elif r >= 1900: rank_name, rank_color = "Candidate Master", "#FF88FF"
        elif r >= 1600: rank_name, rank_color = "Expert", "#AAAAFF"
        elif r >= 1400: rank_name, rank_color = "Specialist", "#77DDBB"
        elif r >= 1200: rank_name, rank_color = "Pupil", "#77FF77"
        else: rank_name, rank_color = "Newbie", "#CCCCCC"
        
        leaderboard.append({"rank": idx, "user_id": user["id"], "username": user["username"], "rating": user["rating"], "max_rating": user["max_rating"], "rank_name": rank_name, "rank_color": rank_color, "total_solved": user["total_solved"], "total_points": user["total_points"]})
    return {"leaderboard": leaderboard, "total": len(users), "page": 1, "pages": 1}

# ==================== CONTESTS ====================
@app.get("/api/v1/competitions/")
async def get_contests():
    contests = []
    for cid, contest in contests_db.items():
        contests.append(contest)
    # Tarixe gore sirala
    contests.sort(key=lambda c: c["start_time"], reverse=True)
    return {"competitions": contests, "total": len(contests)}

@app.post("/api/v1/admin/competitions")
async def create_contest(contest: ContestCreate, current_user = Depends(get_current_user)):
    if not is_admin(current_user): raise HTTPException(403, "Admin icazesi teleb olunur")
    
    cid = str(uuid.uuid4())[:8]
    now = datetime.utcnow()
    start = datetime.fromisoformat(contest.start_time) if contest.start_time else now + timedelta(hours=1)
    end = datetime.fromisoformat(contest.end_time) if contest.end_time else now + timedelta(hours=3)
    
    status = "active" if now >= start and now <= end else "upcoming" if now < start else "completed"
    
    contests_db[cid] = {
        "id": cid,
        "title": contest.title,
        "description": contest.description,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "status": status,
        "challenge_ids": contest.challenge_ids,
        "total_participants": 0,
        "created_at": now.isoformat()
    }
    
    return {"message": "Yarish yaradildi!", "competition_id": cid}

@app.post("/api/v1/competitions/{contest_id}/join")
async def join_contest(contest_id: str, current_user = Depends(get_current_user)):
    if not current_user: raise HTTPException(401, "Daxil olun")
    if contest_id not in contests_db: raise HTTPException(404, "Yarish tapilmadi")
    
    if contest_id not in contest_participants:
        contest_participants[contest_id] = []
    
    if current_user["username"] not in contest_participants[contest_id]:
        contest_participants[contest_id].append(current_user["username"])
        contests_db[contest_id]["total_participants"] += 1
    
    return {"message": "Yarishmaya qatildiniz!"}

# ==================== WISHLIST (İstək Qutusu) ====================
@app.post("/api/v1/wishlist/")
async def add_wishlist(item: WishlistItem, current_user = Depends(get_current_user)):
    if not current_user: raise HTTPException(401, "Daxil olun")
    
    wishlist_db.append({
        "id": str(uuid.uuid4())[:8],
        "title": item.title,
        "description": item.description,
        "category": item.category,
        "username": current_user["username"],
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending",
        "votes": 1
    })
    
    return {"message": "✅ Istek ugurla gonderildi!", "total": len(wishlist_db)}

@app.get("/api/v1/wishlist/")
async def get_wishlist():
    return {"wishlist": sorted(wishlist_db, key=lambda w: w["votes"], reverse=True), "total": len(wishlist_db)}

@app.post("/api/v1/wishlist/{item_id}/vote")
async def vote_wishlist(item_id: str, current_user = Depends(get_current_user)):
    if not current_user: raise HTTPException(401, "Daxil olun")
    
    for item in wishlist_db:
        if item["id"] == item_id:
            item["votes"] += 1
            return {"message": "Ses verildi!", "votes": item["votes"]}
    
    raise HTTPException(404, "Istek tapilmadi")

@app.put("/api/v1/admin/wishlist/{item_id}")
async def update_wishlist_status(item_id: str, status: str = "approved", current_user = Depends(get_current_user)):
    if not is_admin(current_user): raise HTTPException(403, "Admin icazesi teleb olunur")
    
    for item in wishlist_db:
        if item["id"] == item_id:
            item["status"] = status
            return {"message": f"Istek statusu: {status}"}
    
    raise HTTPException(404, "Istek tapilmadi")

# ==================== ADMIN ====================
@app.get("/api/v1/admin/dashboard")
async def admin_dashboard(current_user = Depends(get_current_user)):
    if not is_admin(current_user): raise HTTPException(403, "Admin icazesi teleb olunur")
    
    # Kateqoriya statistikası
    cat_stats = {}
    for ch in challenges_db.values():
        cat = ch["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "solves": 0}
        cat_stats[cat]["total"] += 1
        cat_stats[cat]["solves"] += ch["total_solves"]
    
    return {
        "total_users": len(users_db),
        "total_challenges": len(challenges_db),
        "total_submissions": len(submissions_db),
        "correct_submissions": len(submissions_db),
        "success_rate": 100 if submissions_db else 0,
        "weekly_solves": len([s for s in submissions_db if (datetime.utcnow() - datetime.fromisoformat(s["timestamp"])).days < 7]),
        "weekly_new_users": len([u for u in users_db.values() if (datetime.utcnow() - datetime.fromisoformat(u["created_at"])).days < 7]),
        "category_distribution": [{"category": cat, "total": data["total"], "solves": data["solves"]} for cat, data in cat_stats.items()],
        "top_users": [{"username": u["username"], "rating": u["rating"], "solved": u["total_solved"]} for u in sorted(users_db.values(), key=lambda x: x["rating"], reverse=True)[:10]],
        "recent_activities": [{"username": s["username"], "challenge": challenges_db.get(s["challenge_id"], {}).get("title", ""), "points": 0, "time": s["timestamp"]} for s in submissions_db[-10:]]
    }

@app.get("/api/v1/admin/users")
async def admin_get_users(search: Optional[str] = Query(None), page: int = Query(1), current_user = Depends(get_current_user)):
    if not is_admin(current_user): raise HTTPException(403, "Admin icazesi teleb olunur")
    users = list(users_db.values())
    if search: users = [u for u in users if search.lower() in u["username"].lower()]
    return {"users": users, "total": len(users), "page": page, "pages": 1}

@app.post("/api/v1/admin/challenges")
async def admin_create_challenge(challenge: ChallengeCreate, current_user = Depends(get_current_user)):
    if not is_admin(current_user): raise HTTPException(403, "Admin icazesi teleb olunur")
    
    cid = str(len(challenges_db) + 1)
    challenges_db[cid] = {
        "id": cid, "title": challenge.title,
        "slug": challenge.title.lower().replace(" ", "-"),
        "description": challenge.description,
        "category": challenge.category, "difficulty": challenge.difficulty,
        "base_points": challenge.base_points, "current_points": challenge.base_points,
        "total_solves": 0, "total_attempts": 0,
        "tags": challenge.tags, "author_id": current_user["id"],
        "created_at": datetime.utcnow().isoformat()
    }
    
    default_challenges.append({"title": challenge.title, "description": challenge.description, "category": challenge.category, "difficulty": challenge.difficulty, "base_points": challenge.base_points, "flag": challenge.flag, "tags": challenge.tags})
    
    return {"message": "✅ Challenge yaradildi!", "challenge_id": cid}

# ==================== HEALTH ====================
@app.get("/")
async def root():
    return {"name": "CyberSec Club API", "status": "operational", "version": "4.0.0", "features": ["Contests", "Wishlist", "Statistics", "Rating"]}

@app.get("/health")
async def health():
    return {"status": "healthy", "users": len(users_db), "challenges": len(challenges_db), "contests": len(contests_db), "wishlist": len(wishlist_db)}