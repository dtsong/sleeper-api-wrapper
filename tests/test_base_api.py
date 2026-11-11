"""Offline tests for BaseApi._call.

These tests mock requests.get, so they pin the wrapper's HTTP contract
without the network. They guard against regressions when requests is bumped.
"""
import json

import pytest
import requests

from sleeper_wrapper.base_api import BaseApi

URL = "https://api.sleeper.app/v1/state/nfl"


def _response(status_code: int, payload=None) -> requests.Response:
	response = requests.Response()
	response.status_code = status_code
	response.url = URL
	response._content = b"" if payload is None else json.dumps(payload).encode()
	return response


def test_call_returns_parsed_json(mocker) -> None:
	payload = {"week": 9, "season_type": "regular"}
	mocker.patch("sleeper_wrapper.base_api.requests.get", return_value=_response(200, payload))

	assert BaseApi()._call(URL) == payload


def test_call_returns_list_payloads(mocker) -> None:
	payload = [{"roster_id": 1}, {"roster_id": 2}]
	mocker.patch("sleeper_wrapper.base_api.requests.get", return_value=_response(200, payload))

	assert BaseApi()._call(URL) == payload


def test_call_passes_url_through_unchanged(mocker) -> None:
	mock_get = mocker.patch("sleeper_wrapper.base_api.requests.get", return_value=_response(200, {}))
	url = "https://api.sleeper.app/v1/players/nfl/trending/add?lookback_hours=24&limit=25"

	BaseApi()._call(url)

	mock_get.assert_called_once_with(url)


@pytest.mark.parametrize("status_code", [400, 404, 429, 500])
def test_call_returns_http_error_instead_of_raising(mocker, status_code: int) -> None:
	# Current public behavior: _call returns the HTTPError object, it does not raise.
	# This test locks that contract. Change it only in a deliberate, versioned release.
	mocker.patch("sleeper_wrapper.base_api.requests.get", return_value=_response(status_code))

	result = BaseApi()._call(URL)

	assert isinstance(result, requests.exceptions.HTTPError)
	assert result.response.status_code == status_code


def test_call_does_not_disable_tls_verification(mocker) -> None:
	# The wrapper must never pass verify=False. A default call uses certifi's bundle.
	mock_get = mocker.patch("sleeper_wrapper.base_api.requests.get", return_value=_response(200, {}))

	BaseApi()._call(URL)

	assert "verify" not in mock_get.call_args.kwargs
