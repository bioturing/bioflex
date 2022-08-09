import numpy as np
from ._metadata import _Metadata
from .common import decode_base64_array
from .constants import NUMBER, CATEGORY
from .constants import METADATA_TYPES

class Metadata(_Metadata):
	""" Metadata of a study"""

	def _parse_category_response(self, response: dict):
		self._cluster_names = np.array(response['cluster_names'])
		self._cluster_lengths = np.array(response['cluster_lengths'])
		self._clusters = decode_base64_array(response['metadata_values'], 'uint16')
		self.values = self._cluster_names[self._clusters]


	def _parse_numberic_response(self, response: dict):
		self._cluster_names = None
		self._cluster_lengths = None
		self._clusters = None
		self.values = decode_base64_array(response['metadata_values'], 'float32')


	def fetch(self):
		""" Fetch metadata from BioTuring server,
		self.values will be metadata values array after this function
		Examples
		--------
		>>> study = database.get_study('GSE96583_batch2')
		>>> study.metalist
		[Metadata(id=0,name="Number of mRNA transcripts",type="Numeric"),
 		 Metadata(id=1,name="Number of genes",type="Numeric"),
 		 Metadata(id=2,name="Batch id",type="Category"),
 		 Metadata(id=3,name="Stimulation",type="Category"),
 		 Metadata(id=4,name="Author's cell type",type="Category")]
		>>> metadata = study.metalist[4]
		>>> metadata
		Metadata(id=4,name="Author's cell type",type="Category")
		>>> metadata.fetch()
		>>> metadata.values
		array(['CD8 T cells', 'Dendritic cells', 'CD4 T cells', ...,
			   'CD8 T cells', 'B cells', 'CD4 T cells'], dtype='<U17')
 		"""

		response = self._post_request('/v1/study/fetch_metadata')
		self.name = response['name']
		self._type = response['type']
		self.type = METADATA_TYPES[self._type]

		if self._type == CATEGORY:
			self._parse_category_response(response)
		elif self._type == NUMBER:
			self._parse_numberic_response(response)
		else:
			raise ValueError('Metadata type unknown')