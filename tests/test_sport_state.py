"""Offline test for get_sport_state (mocked, no network)."""
from sleeper_wrapper import get_sport_state


def test_get_sport_state(mocker) -> None:
	mock_data = {
		"week": 1,
		"season_type": "regular"
		}
	mock_base_api_call = mocker.patch(
		"sleeper_wrapper.league.BaseApi._call", return_value=mock_data
		)
	response = get_sport_state("nfl")
	assert response == mock_data
	mock_base_api_call.assert_called_once_with(
		"https://api.sleeper.app/v1/state/nfl"
		)
