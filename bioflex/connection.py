from ._connection import _Connection
from .database import Database

class Connection(_Connection):
	""" Connection to BioTuring API server"""

	def databases(self):
		""" Get database instances from BioTuring API server
		Returns
		-------
		databases : list of Databases
		Examples
		--------
		>>> import bioturingclient
		>>> conn = bioturingclient.connect('70d2acfda3a54ca6a4390699394****')
		>>> conn.databases()
		[DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",name="BioTuring database",species="human",version=1),
 		 DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",name="BioTuring database",species="human",version=2),
 		 DataBase(id="5010c7d573ae4ff2b9691422b99aa2cd",name="BioTuring database",species="human",version=3)]
		"""
		response = self._post_request('/v1/database/list')
		return [
			Database(self, db['id'], db['name'], db['species'], db['version'])
			for db in response
		]

