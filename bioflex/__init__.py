from .constants import *
from .connection import Connection

def connect(token: str):
	""" Create a connection to BioTuring API server
	Parameters
	----------
	token : str
		Your access token registered from https://api.bioturing.com
	Returns
	-------
	conn : Connection
	Examples
	--------
	>>> import bioflex
	>>> conn = bioflex.connect('70d2acfda3a54ca6a4390699394****')
	"""
	return Connection(token)