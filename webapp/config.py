from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	"""Configuration for the FastAPI proof of concept."""

	league_id: str = "1257507151190958081"
	sport: str = "nfl"
	score_type: str = "pts_ppr"
	league_cache_ttl_seconds: int = 300
	players_cache_ttl_seconds: int = 21600
	stats_cache_ttl_seconds: int = 900

	class Config:
		env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	"""Returns cached settings instance."""
	return Settings()
