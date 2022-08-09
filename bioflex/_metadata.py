import numpy as np
from typing import List
from ._study import _Study
from .constants import METADATA_TYPES
from ._base_object import _BaseObject

class _Metadata(_BaseObject):
	study: _Study
	id: int
	name: str
	type: int
	values: np.ndarray = None

	_cluster_names: List[str] = None
	_cluster_lengths: List[str] = None
	_clusters: np.ndarray = None


	def __init__(self, study: _Study, id: int, name: str, type: int):
		super().__init__(study)

		self.study = study
		self.id = id
		self.name = name
		self._type = type
		self.type = METADATA_TYPES[self._type]


	def __repr__(self):
		return 'Metadata(id={},name="{}",type="{}")'.format(
			self.id, self.name, self.type,
		)

	def _post_params(self, params: dict):
		return {
			'field_idx': self.id,
			**params,
		}
