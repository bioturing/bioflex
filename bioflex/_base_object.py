import io
from abc import ABC, abstractmethod

class _BaseObject(ABC):
	_parent: any

	def __init__(self, parent: any):
		self._parent = parent

	@abstractmethod
	def _post_params(self, params: dict) -> dict:
		pass


	def _post_download(self,
			path: str,
			params: dict = dict(),
			dst_file: io.IOBase = None,
		):
		return self._parent._post_download(
			path,
			params=self._post_params(params),
			dst_file=dst_file,
		)


	def _post_request(self,
			path: str,
			params: dict = dict(),
		):
		return self._parent._post_request(
			path, params=self._post_params(params),
		)
