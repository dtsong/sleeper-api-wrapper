"""Trust store regression tests for the eMudhra intermediate CA compromise.

See https://emudhra.we-have-a-problem.com/. certifi 2026.10.19 removed the
affected root. The bundle tests below are the deterministic gate: they run
offline and fail on any certifi that still ships the root.

The chain tests are an end-to-end smoke check of the TLS stack that runs them.
They are marked `network`. On Python 3.13+ strict X.509 checks may reject the
test chain even with an old bundle, so the bundle tests carry the real signal.
"""
import certifi
import pytest
import requests

PATCHED_CERTIFI = (2026, 10, 19)
COMPROMISED_ROOT = "emSign ECC Root CA - G3"

COMPROMISED_CHAIN_HOSTS = [
	"https://dv-g3b-noct-emudhra.we-have-a-problem.com/",
	"https://dv-g3b-aaa-noct-emudhra.we-have-a-problem.com/",
]


def _version_tuple(version: str) -> tuple:
	return tuple(int(part) for part in version.split(".")[:3])


def test_certifi_is_patched() -> None:
	assert _version_tuple(certifi.__version__) >= PATCHED_CERTIFI, (
		f"certifi {certifi.__version__} predates the eMudhra distrust; upgrade to >= 2026.10.19"
	)


def test_certifi_bundle_excludes_compromised_root() -> None:
	with open(certifi.where(), encoding="ascii") as bundle:
		assert COMPROMISED_ROOT not in bundle.read(), (
			f"{certifi.where()} still trusts {COMPROMISED_ROOT}"
		)


@pytest.mark.network
@pytest.mark.parametrize("url", COMPROMISED_CHAIN_HOSTS)
def test_requests_rejects_compromised_chain(url: str) -> None:
	with pytest.raises(requests.exceptions.SSLError):
		requests.get(url, timeout=15)
