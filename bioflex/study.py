import h5py
from typing import List
from scipy import sparse

from ._database import _Database
from ._study import _Study
from .common import decode_base64_array
from .metadata import Metadata

class Study(_Study):
	"""Study instance"""

	metalist: List[Metadata] = None

	def __init__(self,
			db: _Database,
			response: dict,
		):
		super().__init__(db, response)
		self.metalist = [
			Metadata(self, field['id'], field['name'], field['type'])
			for field in response['metalist']
		]


	def query_genes(self, gene_names: List[str], unit: str):
		""" Get study instance using study index
		Parameters
		----------
		gene_names : list of str
			Querying gene names
		unit: str
			Expression unit, bioflex.UNIT_LOGNORM or bioflex.UNIT_RAW
		Returns
		-------
		expression_matrix : csc_matrix
			Expression matrix, shape=(n_cells, n_genes)
		Examples
		--------
		>>> exp_mtx = study.query_genes(['CD3D', 'CD3E'], bioflex.UNIT_LOGNORM)
		>>> exp_mtx
		<29065x2 sparse matrix of type '<class 'numpy.float32'>'
			with 15492 stored elements in Compressed Sparse Column format>
		"""

		response = self._post_request('/v1/study/query_genes', {
			'gene_names': gene_names,
			'unit': unit,
		})


		shape = response['shape']
		data = decode_base64_array(response['data'], 'float32')
		indices = decode_base64_array(response['indices'], 'uint32')
		indptr = decode_base64_array(response['indptr'], 'uint64')

		csc_mtx = sparse.csc_matrix((data, indices, indptr), shape=shape)

		return csc_mtx


	def matrix(self, unit: str):
		""" Get study matrix
		Parameters
		----------
		unit: str
			Expression unit, bioflex.UNIT_LOGNORM or bioflex.UNIT_RAW
		Returns
		-------
		expression_matrix : csc_matrix
			Expression matrix, shape=(n_cells, n_genes)
		Examples
		--------
		>>> study.matrix(bioflex.UNIT_LOGNORM)
		<29065x64642 sparse matrix of type '<class 'numpy.float32'>'
			with 17570739 stored elements in Compressed Sparse Column format>
		"""

		buffer = self._post_download('/v1/study/get_matrix', {'unit': unit})
		with h5py.File(buffer, 'r') as f:
			data = f['data'][()]
			indices = f['indices'][()]
			indptr = f['indptr'][()]
			shape = f['shape'][()]
		buffer.close()

		return sparse.csc_matrix((data, indices, indptr), shape=shape)


	def features(self):
		""" Get study features
		Returns
		-------
		features : list of str
			Study features, length = number of genes
		Examples
		--------
		>>> study.features()
		['5S_RRNA',
 		 '5_8S_RRNA',
 		 ...
 		 'AC006273',
 		 'AC006277',
 		 ...]
		"""

		return self._post_request('/v1/study/get_features')


	def barcodes(self):
		""" Get study barcodes
		Returns
		-------
		barcodes : list of str
			Study barcodes, length = number of cells
		Examples
		--------
		>>> study.barcodes()
		['GSM2560249_AAACATACCAAGCT-1',
		 'GSM2560249_AAACATACCCCTAC-1',
		 ...
		 'GSM2560249_AATTGTGATTCACT-1',
		 'GSM2560249_AATTGTGATTTCGT-1',
		 ...]
		 """

		return self._post_request('/v1/study/get_barcodes')
