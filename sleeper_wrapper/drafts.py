from .base_api import BaseApi

class Drafts(BaseApi):
	def __init__(self, draft_id):
		self.draft_id = draft_id
		self._base_url = "https://api.sleeper.app/v1/draft/{}".format(self.draft_id)

	def get_specific_draft(self):
		"""gets the draft specified by the draft_id"""
		return self._call(self._base_url)

	def get_all_picks(self):
		"""gets all the picks in the draft specified by the draft_id"""
		return self._call("{}/{}".format(self._base_url,"picks"))

	def get_traded_picks(self):
		"""gets all traded picks in the draft specified by the draft_id"""
		return self._call("{}/{}".format(self._base_url,"traded_picks"))
