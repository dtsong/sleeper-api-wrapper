from typing import Union

from .base_api import BaseApi

class Drafts(BaseApi):
	"""The data associated with a given Sleeper draft.

	Attributes:
	  draft_id: Union[str, int]
	    The Sleeper ID for the draft. May be provided as a string or int.
	"""

	def __init__(self, draft_id: Union[str, int]) -> None:
		"""Initializes the instance based on draft ID.

		Args:
		  draft_id: Union[str, int]
	        The Sleeper ID for the draft. May be provided as a string or int.
		"""
		self.draft_id = draft_id
		self._base_url = "https://api.sleeper.app/v1/draft/{}".format(self.draft_id)

	def get_specific_draft(self) -> dict:
		"""Returns the draft's data."""
		return self._call(self._base_url)

	def get_all_picks(self) -> list:
		"""Returns all the picks in the specified draft."""
		return self._call("{}/{}".format(self._base_url,"picks"))

	def get_traded_picks(self) -> list:
		"""Returns all the traded picks in the specified draft."""
		return self._call("{}/{}".format(self._base_url,"traded_picks"))
