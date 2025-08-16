from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv, os, pathlib

app = FastAPI()

# --- Paths ---
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.csv"

# --- Static & Templates ---
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Ensure CSV exists with headers ---
DATA_DIR.mkdir(parents=True, exist_ok=True)
if not USERS_FILE.exists():
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "password", "first_name", "last_name"])

def get_user_by_email(email: str):
    if not USERS_FILE.exists():
        return None
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"].strip().lower() == email.strip().lower():
                return row
    return None

# ---------------- Routes ----------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)
    if user and user["password"] == password:
        resp = RedirectResponse(url="/feed", status_code=303)
        resp.set_cookie("session_email", email, httponly=True)
        return resp
    return RedirectResponse(url="/login?error=Invalid+email+or+password", status_code=303)

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("signup.html", {"request": request, "error": error})

@app.post("/signup")
def signup(first_name: str = Form(""),
           last_name: str = Form(""),
           email: str = Form(...),
           password: str = Form(...)):
    # prevent duplicates
    if get_user_by_email(email):
        return RedirectResponse(url="/login?error=Account+already+exists.+Please+log+in.", status_code=303)

    with open(USERS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([email, password, first_name, last_name])

    return RedirectResponse(url="/login?success=1", status_code=303)

@app.get("/feed", response_class=HTMLResponse)
def feed(request: Request):
    email = request.cookies.get("session_email")
    if not email:
        return RedirectResponse(url="/login", status_code=303)
    user = get_user_by_email(email) or {}
    name = user.get("first_name") or email.split("@")[0]
    return templates.TemplateResponse("feed.html", {"request": request, "name": name})

@app.get("/logout")
def logout():
    resp = RedirectResponse(url="/login", status_code=303)
    resp.delete_cookie("session_email")
    return resp

# JSON API for cards (feed)
@app.get("/api/feed", response_class=JSONResponse)
def api_feed(request: Request, page: int = 1, page_size: int = 8):
    # simple demo dataset (could come from DB later)
    all_items = [
        {
            "title": "Shop Deals",
            "text": "Always-great deals and seasonal promos.",
            "image": "https://picsum.photos/seed/deals/600/400",
            "cta": "Shop Deals",
            "url": "#"
        },
        {
            "title": "Shop Activewear",
            "text": "Stay warm & protected during outdoor activities.",
            "image": "https://picsum.photos/seed/active/600/400",
            "cta": "Shop Activewear",
            "url": "#"
        },
        {
            "title": "Shoulder Support",
            "text": "Stabilizers with compression and strap designs.",
            "image": "https://picsum.photos/seed/shoulder/600/400",
            "cta": "Shop Shoulder",
            "url": "#"
        },
        {
            "title": "Ski & Snowboarding",
            "text": "Gear for the coming season — find the best fit.",
            "image": "https://picsum.photos/seed/ski/600/400",
            "cta": "Shop Ski & Snow",
            "url": "#"
        },
        {
            "title": "Running Essentials",
            "text": "Shoes and wearables built for distance.",
            "image": "https://picsum.photos/seed/run/600/400",
            "cta": "Shop Running",
            "url": "#"
        },
        {
            "title": "Cycling Picks",
            "text": "Helmets, gloves, and performance kits.",
            "image": "https://picsum.photos/seed/cycle/600/400",
            "cta": "Shop Cycling",
            "url": "#"
        },
        {
            "title": "Yoga & Mobility",
            "text": "Mats, straps, and guided routines.",
            "image": "https://picsum.photos/seed/yoga/600/400",
            "cta": "Shop Yoga",
            "url": "#"
        },
        {
            "title": "Recovery Tools",
            "text": "Massage guns, foam rollers, and more.",
            "image": "https://picsum.photos/seed/recover/600/400",
            "cta": "Shop Recovery",
            "url": "#"
        },
        {
            "title": "Hiking Must-haves",
            "text": "Backpacks, hydration, and trail shoes.",
            "image": "https://picsum.photos/seed/hike/600/400",
            "cta": "Shop Hiking",
            "url": "#"
        },
        {
            "title": "Indoor Training",
            "text": "Home gym gear for every space.",
            "image": "https://picsum.photos/seed/home/600/400",
            "cta": "Shop Training",
            "url": "#"
        }
    ]
    start = (page - 1) * page_size
    end = start + page_size
    items = all_items[start:end]
    return {"items": items, "has_more": end < len(all_items)}
