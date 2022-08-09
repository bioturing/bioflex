from typing import List
from .study import Study
from ._database import _Database


class ExpressionSummary():
	"""Expression summary"""
	"""Name of cluster"""
	name: str
	"""Sum of expressed values in cluster"""
	sum: float
	"""Mean of expressed values in cluster"""
	mean: float
	"""Clutser expression rate (count / total_cells)"""
	rate: float
	"""Number of expressed cells in cluster"""
	count: int
	"""Number of cells in cluster"""
	total: int

	def __init__(self, response: dict):
		self.name = response['name']
		self.sum = response['sum']
		self.mean = response['mean']
		self.rate = response['rate']
		self.count = response['count']
		self.total = response['total']

	def __repr__(self):
		return 'Summary(name="{}",sum={},mean={},rate={},count={},total={})'.format(
			self.name, self.sum, self.mean, self.rate, self.count, self.total,
		)


class Database(_Database):
	""" BioTuring Database instance """

	def get_study(self, study_hash_id: str):
		""" Get study instance using study index
		Parameters
		----------
		study_hash_id : str
			Study hash ID from https://talk2data.bioturing.com/studies/
		Returns
		-------
		study : Study
		Examples
		--------
		>>> database.get_study('GSE96583_batch2')
		Study(id="1557",hash_id="GSE96583_batch2",title="Multiplexed droplet
		single-cell RNA-sequencing using natural genetic variation (Batch 2)",
		reference="https://www.nature.com/articles/nbt.4042")
		"""
		response = self._post_request('/v1/study/get', {
			'hash_id': study_hash_id,
		})
		return Study(self, response)


	def get_celltypes_expression_summary(self, gene_names: List[str]):
		""" Get cell types gene expression summary
		Parameters
		----------
		gene_names : list of str
			List of gene names to summerize
		Returns
		-------
		expressions : list of ExpressionSummary
		Examples
		--------
		>>> database.get_celltypes_expression_summary(['CD3D', 'CD3E'])
		{'CD3D': [Summary(name="B cell",sum=707108874.0,mean=4192.709686217774,rate=0.03504117106973723,count=168652.0,total=4812967),
		  Summary(name="CD4-positive, alpha-beta T cell",sum=9489987442.0,mean=4657.561967741555,rate=0.5283278751435854,count=2037544.0,total=3856590),
		  ...
		  Summary(name="corneal progenitor",sum=0.0,mean=0.0,rate=0.0,count=0.0,total=3973),
		  Summary(name="nucleus pulposus progenitor cell",sum=0.0,mean=0.0,rate=0.0,count=0.0,total=2310)]}
		"""
		response = self._post_request('/v1/expression/celltypes', {
			'gene_names': gene_names,
		})
		results = dict()
		for gene_name in gene_names:
			gene_summary = []
			for summary in response[gene_name]:
				gene_summary.append(ExpressionSummary(summary))

			results[gene_name] = gene_summary
		return results
