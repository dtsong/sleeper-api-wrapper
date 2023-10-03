# User
`sleeper_wrapper.User()`

Instantiating a `User` object will allow interaction with Sleeper's [User endpoint](https://docs.sleeper.com/#user) by pulling data for the user specified by the `user_id`.


## Attributes
`initial_user_input` _(Union[str, int])_: The Sleeper user ID or username for the user. May be provided as a string or an int.


## Methods
`get_user()`: Returns the user's data.

`get_all_leagues(sport, season)`: Returns every league the user is in for that sport and season.

`get_all_drafts(sport, season)`: Returns every draft the user is in for that sport and season.

`get_username()`: Retrieves username.

`get_user_id()`: Retrieves user_id.

`get_display_name()`: Retrieves display name.


## Examples