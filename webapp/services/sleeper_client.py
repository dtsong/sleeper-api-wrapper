import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from sleeper_wrapper import Drafts, League, Players, Stats, get_sport_state

from webapp.config import Settings


@dataclass
class TTLCache:
	"""Lightweight TTL cache to avoid hammering the Sleeper API."""

	ttl_seconds: int
	value: Any = None
	expires_at: float = 0

	def get(self) -> Any:
		if self.value is not None and time.time() < self.expires_at:
			return self.value
		return None

	def set(self, value: Any) -> None:
		self.value = value
		self.expires_at = time.time() + self.ttl_seconds


class SleeperClient:
	"""Fetches and shapes data for the FastAPI views."""

	def __init__(self, settings: Settings):
		self.settings = settings
		self._league_cache = TTLCache(settings.league_cache_ttl_seconds)
		self._players_cache = TTLCache(settings.players_cache_ttl_seconds)
		self._stats_cache: Dict[str, TTLCache] = {}

	def _fetch_league_bundle(self) -> Dict[str, Any]:
		"""Returns cached league info, rosters, users, and sport state."""
		cached = self._league_cache.get()
		if cached:
			return cached

		league = League(self.settings.league_id)
		info = league.get_league()
		rosters = league.get_rosters()
		users = league.get_users()
		state = get_sport_state(self.settings.sport)

		bundle = {
			"league": league,
			"info": info,
			"rosters": rosters,
			"users": users,
			"state": state,
		}
		self._league_cache.set(bundle)
		return bundle

	def _user_lookup(self, users: List[Dict[str, Any]]) -> Dict[str, str]:
		result = {}
		for user in users:
			team_name = user.get("metadata", {}).get("team_name")
			name = team_name or user.get("display_name") or user.get("username")
			if user.get("user_id"):
				result[user["user_id"]] = name
		return result

	def _roster_lookup(self, rosters: List[Dict[str, Any]]) -> Dict[int, str]:
		return {roster["roster_id"]: roster.get("owner_id") for roster in rosters}

	def _players(self) -> Dict[str, Dict[str, Any]]:
		"""Returns cached player directory keyed by player_id."""
		cached = self._players_cache.get()
		if cached:
			return cached
		players = Players().get_all_players(self.settings.sport)
		if not isinstance(players, dict):
			players = {}
		self._players_cache.set(players)
		return players

	def _season_stats(self, season: str) -> Dict[str, Any]:
		"""Returns cached season stats."""
		cache = self._stats_cache.get(season)
		if cache and cache.get() is not None:
			return cache.get()

		cache = TTLCache(self.settings.stats_cache_ttl_seconds)
		self._stats_cache[season] = cache

		stats = Stats().get_all_stats("regular", season)
		if not isinstance(stats, dict):
			stats = {}
		cache.set(stats)
		return stats

	def league_dashboard(self, week: Optional[int] = None) -> Dict[str, Any]:
		bundle = self._fetch_league_bundle()
		league = bundle["league"]
		info = bundle["info"]
		rosters = bundle["rosters"]
		users = bundle["users"]
		state = bundle["state"]

		target_week = week or state.get("week") or info.get("week") or 1
		matchups = league.get_matchups(target_week)
		if not isinstance(matchups, list):
			matchups = []
		scoreboard = self._build_scoreboard(matchups, rosters, users, target_week)

		standings = league.get_standings(rosters=rosters, users=users)
		transactions = league.get_transactions(target_week)
		if not isinstance(transactions, list):
			transactions = []

		return {
			"info": info,
			"state": state,
			"settings": info.get("settings", {}),
			"standings": standings,
			"managers": users,
			"scoreboard": scoreboard,
			"transactions": transactions or [],
			"week": target_week,
		}

	def _build_scoreboard(
		self,
		matchups: List[Dict[str, Any]],
		rosters: List[Dict[str, Any]],
		users: List[Dict[str, Any]],
		week: int,
	) -> List[Dict[str, Any]]:
		if not matchups:
			return []
		user_lookup = self._user_lookup(users)
		roster_lookup = self._roster_lookup(rosters)

		matchup_groups: Dict[int, List[Dict[str, Any]]] = {}
		for matchup in matchups:
			matchup_id = matchup.get("matchup_id", 0)
			matchup_groups.setdefault(matchup_id, []).append(matchup)

		scoreboard = []
		for matchup_id, teams in sorted(matchup_groups.items()):
			entries = []
			for team in teams:
				roster_id = team.get("roster_id")
				owner_id = roster_lookup.get(roster_id)
				team_name = user_lookup.get(owner_id, f"Roster {roster_id}")
				points_raw = team.get("points", 0)
				projected_raw = team.get("projected_points")
				points = round(points_raw, 2) if isinstance(points_raw, (int, float)) else 0
				projected = round(projected_raw, 2) if isinstance(projected_raw, (int, float)) else None
				entries.append(
					{
						"team_name": team_name,
						"points": points,
						"projected": projected,
					}
				)
			scoreboard.append({"matchup_id": matchup_id, "week": week, "teams": entries})
		return scoreboard

	def roster_view(self) -> Dict[str, Any]:
		bundle = self._fetch_league_bundle()
		info = bundle["info"]
		rosters = bundle["rosters"]
		users = bundle["users"]
		user_lookup = self._user_lookup(users)
		players = self._players()

		def hydrate_player(player_id: str) -> Dict[str, Any]:
			player = players.get(player_id, {})
			full_name = player.get("full_name") or f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
			return {
				"id": player_id,
				"name": full_name or player_id,
				"position": player.get("position"),
				"team": player.get("team"),
			}

		hydrated = []
		for roster in rosters:
			owner_id = roster.get("owner_id")
			starters_set = set(roster.get("starters", []))
			all_players = [hydrate_player(pid) for pid in roster.get("players", [])]
			starters_full = [hydrate_player(pid) for pid in roster.get("starters", [])]
			bench = [p for p in all_players if p["id"] not in starters_set]
			hydrated.append(
				{
					"roster_id": roster.get("roster_id"),
					"owner_id": owner_id,
					"owner_name": user_lookup.get(owner_id, "Unassigned"),
					"players": all_players,
					"starters": starters_full,
					"bench": bench,
				}
			)

		return {"info": info, "rosters": hydrated, "users": users}

	def draft_results(self) -> Dict[str, Any]:
		bundle = self._fetch_league_bundle()
		info = bundle["info"]
		league = bundle["league"]
		users = bundle["users"]
		user_lookup = self._user_lookup(users)
		players = self._players()

		drafts = league.get_all_drafts()
		if not drafts:
			return {"draft": None, "picks": []}
		active_draft = drafts[0]
		draft = Drafts(active_draft["draft_id"])
		picks = draft.get_all_picks() or []

		def player_name(player_id: str) -> str:
			player = players.get(player_id, {})
			return player.get("full_name") or f"{player.get('first_name', '')} {player.get('last_name', '')}".strip() or player_id

		decorated = []
		for pick in sorted(picks, key=lambda p: (p.get("round", 0), p.get("pick_no", 0))):
			player_id = pick.get("player_id")
			decorated.append(
				{
					"round": pick.get("round"),
					"pick_no": pick.get("pick_no"),
					"roster_id": pick.get("roster_id"),
					"picked_by": user_lookup.get(pick.get("picked_by")),
					"player": player_name(player_id),
					"player_id": player_id,
					"metadata": pick.get("metadata", {}),
				}
			)

		return {"info": info, "draft": active_draft, "picks": decorated}

	def player_stats(
		self, query: Optional[str] = None, season: Optional[str] = None, add_drop: str = "add"
	) -> Dict[str, Any]:
		bundle = self._fetch_league_bundle()
		info = bundle["info"]
		default_season = info.get("season")
		season_to_use = str(season or default_season)
		players = self._players()
		stats = self._season_stats(season_to_use) if season_to_use else {}

		def enrich(player_id: str) -> Dict[str, Any]:
			player = players.get(player_id, {})
			stat_line = stats.get(player_id, {})
			full_name = player.get("full_name") or f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
			return {
				"id": player_id,
				"name": full_name or player_id,
				"position": player.get("position"),
				"team": player.get("team"),
				"pts_ppr": stat_line.get("pts_ppr"),
				"pts_std": stat_line.get("pts_std"),
				"pts_half_ppr": stat_line.get("pts_half_ppr"),
				"games": stat_line.get("gp"),
			}

		results: List[Dict[str, Any]] = []
		source: str
		if query:
			query_lower = query.lower()
			for player_id, player in players.items():
				name = player.get("full_name") or f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
				if name and query_lower in name.lower():
					results.append(enrich(player_id))
				if len(results) >= 25:
					break
			source = "search"
		else:
			trending = Players().get_trending_players(self.settings.sport, add_drop=add_drop, hours=168, limit=25)
			for entry in trending:
				player_id = entry.get("player_id")
				annotated = enrich(player_id)
				annotated["count"] = entry.get("count")
				annotated["direction"] = add_drop
				results.append(annotated)
			source = "trending"

		return {"info": info, "season": season_to_use, "results": results, "source": source}


_client_instance: Optional[SleeperClient] = None


def get_client(settings: Settings) -> SleeperClient:
	"""Factory for dependency injection."""
	global _client_instance
	if _client_instance is None:
		_client_instance = SleeperClient(settings)
	return _client_instance
