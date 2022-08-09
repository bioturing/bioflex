from typing import List
from ._database import _Database
from ._base_object import _BaseObject


class _Study(_BaseObject):
	database: _Database

	id: int
	hash_id: str
	title: str
	authors: List[str]
	reference: str

	def __init__(self,
			database: _Database,
			response: dict,
		):
		super().__init__(database)

		self.database = database
		self.id = response['id']
		self.hash_id = response['hash_id']
		self.title = response['title']
		self.authors = response['authors']
		self.reference = response['reference']


	def __repr__(self):
		return 'Study(id="{}",hash_id="{}",title="{}",reference="{}")'.format(
			self.id, self.hash_id, self.title, self.reference
		)


	def _post_params(self, params: dict):
		return {
			'study_idx': self.id,
			**params,
		}
