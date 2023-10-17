# Stats
`sleeper_wrapper.Stats()`

Instantiating a `Stats` object will allow interaction with Sleeper's Stats endpoint and retrieve stats and projections for Sleeper, though it is no longer officially documented and supported. Both stats and projections include box score and detailed stats as well as rollups to fantasy scores in standard scoring formats (standard, ppr, half ppr).


## Methods
`get_all_stats(season_type, season)`: Retrieves all statistics for the given season. It supports detailed data going back until 2010 before only providing ranks for the various scoring formats. The detailed data contains information such as passing yards per attempt, field goal makes and misses by 10 yard buckets, snaps played, red zone statistics, and more.

`get_week_stats(season_type, season, week)`: Retrieves all statistics for the given season and week. It supports detailed data going back until 2010 before only providing ranks for the various scoring formats. The detailed data contains information such as passing yards per attempt, field goal makes and misses by 10 yard buckets, snaps played, red zone statistics, and more.

`get_all_projections(season_type, season)`: Retrieves all projections for the given season. It supports data going back until 2018 and contains information such as passing yards per attempt, field goal makes and misses by 10 yard buckets, ADP, games played, and more.

`get_week_projections(season_type, season, week)`: Retrieves all projections for the given season and week. It supports data going back until 2018 and contains information such as passing yards per attempt, field goal makes and misses by 10 yard buckets, ADP, games played, and more.

`get_player_week_stats(stats, player_id)`: Gets a player's stats or projections from the given dictionary.

`get_player_week_score(stats, player_id)`: Retrieves a player's points scored for the primary scoring formats (standard, PPR, half PPR).


## Examples
```
from sleeper_wrapper import Stats

stats = Stats()

# pulls all of the stats for week 1 of the 2023 regular season
week_stats = stats.get_week_stats("regular", 2023, 1)

# retrieves stats for the Detroit defense for the provided week
score = stats.get_player_week_score(week_stats, "DET")
```