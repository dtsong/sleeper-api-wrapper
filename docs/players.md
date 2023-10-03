# Players
`sleeper_wrapper.Players()`

Instantiating a `Players` object will allow interaction with Sleeper's [Players endpoint](https://docs.sleeper.com/#players) by pulling data on the players. Examples for how the data is structured for methods hitting the API directly may be found in their documentation for the endpoint.


## Methods
`get_all_players(sport)`: Gets all players from Sleeper. Retrieves data pertaining to each player in the Sleeper, including positions, biographical data, height / weight, team, and more.

> Please use this call sparingly, as it is intended only to be used once per day at most to keep your player IDs updated.
>
> Save the information to your own servers, if possible.

`get_trending_players(sport, add_drop, hours, limit)`: Gets trending players from Sleeper. Retrieves the player ID and number of adds / drops for that player during the specified lookback hours.

> If you use this trending data, please attribute Sleeper.
> Copy the code below to embed it in your app:
>
> \<iframe src="https://sleeper.app/embed/players/nfl/trending/add?lookback_hours=24&limit=25" width="350" height="500" allowtransparency="true" frameborder="0"></iframe>


## Examples
```
from sleeper_wrapper import Players

players = Players()

# gets all NFL players in the Sleeper system
all_players = players.get_all_players(sport="nfl")

# gets the top 10 added NFL players in the last 24 hours
trending_players = players.get_trending_players(sport="nfl", add_drop="add", hours=24, limit=10)
```