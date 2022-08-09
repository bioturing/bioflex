import io
import requests
from tqdm import tqdm
from .constants import CHUNK_SIZE
from .common import check_http_response

BIOTURING_ADDRESS = 'https://api.bioturing.com'

class _Connection():
	_token: str = None

	def __init__(self, token: str):
		self._token = token


	def _http_headers(self):
		return {'btr-api-token': self._token}


	def _post_download(self,
			path: str,
			params: dict = dict(),
			dst_file: io.IOBase = None,
		):

		if dst_file is None:
			dst_f = io.BytesIO()
		else:
			dst_f = dst_file

		response = requests.post(
			'{}{}'.format(BIOTURING_ADDRESS, path),
			stream=True, json=params, headers=self._http_headers(),
		)

		check_http_response(response)

		total_size = response.headers.get('Content-Length', None)
		if total_size is not None:
			total_size = int(total_size)

		with tqdm(total=total_size, desc='Downloading', unit='bytes', unit_scale=True) as p:
			for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
				dst_f.write(chunk)
				p.update(len(chunk))

		dst_f.flush()
		dst_f.seek(0)

		return dst_f


	def _post_request(self,
			path: str,
			params: dict = dict(),
		):
		response = requests.post(
			'{}{}'.format(BIOTURING_ADDRESS, path),
			json=params, headers=self._http_headers(),
		)

		check_http_response(response)

		return response.json()
