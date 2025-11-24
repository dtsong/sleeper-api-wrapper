from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webapp.config import Settings, get_settings
from webapp.services.sleeper_client import SleeperClient, get_client

app = FastAPI(title="Sleeper League Dashboard", version="0.1.0")

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")


def client_dependency(settings: Settings = Depends(get_settings)) -> SleeperClient:
	return get_client(settings)


@app.get("/", response_class=HTMLResponse)
def league_dashboard(
	request: Request,
	week: int | None = Query(default=None, description="Override week to view"),
	client: SleeperClient = Depends(client_dependency),
):
	data = client.league_dashboard(week=week)
	return templates.TemplateResponse(
		"dashboard.html", {"request": request, "title": "League Dashboard", **data}
	)


@app.get("/rosters", response_class=HTMLResponse)
def rosters(
	request: Request,
	client: SleeperClient = Depends(client_dependency),
):
	data = client.roster_view()
	return templates.TemplateResponse(
		"rosters.html", {"request": request, "title": "Rosters", **data}
	)


@app.get("/draft", response_class=HTMLResponse)
def draft(
	request: Request,
	client: SleeperClient = Depends(client_dependency),
):
	data = client.draft_results()
	return templates.TemplateResponse(
		"draft.html", {"request": request, "title": "Draft Results", **data}
	)


@app.get("/players", response_class=HTMLResponse)
def players(
	request: Request,
	q: str | None = Query(default=None, description="Player name search"),
	season: str | None = Query(default=None, description="Season year for stats"),
	add_drop: str = Query(default="add", description="Trending add or drop feed"),
	client: SleeperClient = Depends(client_dependency),
):
	data = client.player_stats(query=q, season=season, add_drop=add_drop)
	return templates.TemplateResponse(
		"players.html",
		{"request": request, "title": "Player Stats", "query": q, "add_drop": add_drop, **data},
	)


@app.get("/health")
def health() -> dict:
	return {"status": "ok"}
