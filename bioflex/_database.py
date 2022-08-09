from ._connection import _Connection
from ._base_object import _BaseObject

class _Database(_BaseObject):
	connection: _Connection

	id: str
	name: str
	species: str
	version: int

	def __init__(self,
			connection: _Connection,
			id: str,
			name: str,
			species: str,
			version: int,
		):
		super().__init__(connection)

		self.connection = connection
		self.id = id
		self.name = name
		self.species = species
		self.version = version


	def __repr__(self):
		return 'DataBase(id="{}",name="{}",species="{}",version={})'.format(
			self.id, self.name, self.species, self.version,
		)


	def _post_params(self, params: dict):
		return {
			'database': self.id,
			'species': self.species,
			'version': self.version,
			**params,
		}
