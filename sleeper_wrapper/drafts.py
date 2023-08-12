from typing import Union

from .base_api import BaseApi

class Drafts(BaseApi):
	def __init__(self, draft_id: Union[str, int]) -> None:
		self.draft_id = draft_id
		self._base_url = "https://api.sleeper.app/v1/draft/{}".format(self.draft_id)

	def get_specific_draft(self) -> dict:
		"""gets the draft specified by the draft_id"""
		return self._call(self._base_url)

	def get_all_picks(self) -> list:
		"""gets all the picks in the draft specified by the draft_id"""
		return self._call("{}/{}".format(self._base_url,"picks"))

	def get_traded_picks(self) -> list:
		"""gets all traded picks in the draft specified by the draft_id"""
		return self._call("{}/{}".format(self._base_url,"traded_picks"))
