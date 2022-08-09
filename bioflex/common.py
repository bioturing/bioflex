import base64
import numpy as np
from requests import Response
from requests import HTTPError


def decode_base64_array(base64_str: str, dtype: str, shape=(-1,)):
	decoded = base64.b64decode(base64_str)
	arr = np.frombuffer(decoded, dtype=dtype)
	return arr.reshape(shape)


def check_http_response(response: Response):
	if response.ok:
		return

	try:
		detail = response.json()['detail']
	except:
		response.raise_for_status()

	raise HTTPError(detail)
