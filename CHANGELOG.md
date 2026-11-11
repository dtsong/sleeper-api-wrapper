# Changelog

 ## Version 1.0.1 and 1.0.2
- Created all objects for the wrapper
- Created all initial functions

## Version 1.0.3
- Added losses to standings
- Updated documentation

## Version 1.0.6
- Fixed scoreboards bug caused by sleeper api giving None as custom pts

## Version 1.0.7
- Fixed KeyError in the get_team_score() method.

## Version 1.2.0
- Added `get_sport_state` function to `league` module.

## Version 1.2.3
- Security: require `certifi>=2026.10.19`, which removes the roots behind the eMudhra intermediate CA compromise ([details](https://emudhra.we-have-a-problem.com/)).
- Widened `requests` to `>=2.32.4, <3` (2.32.4 fixes CVE-2024-47081).
- Added support for Python 3.15 (`>=3.11, <3.16`).
- Added offline tests for `BaseApi._call` and a TLS trust regression test. Live API tests are marked `network`.
