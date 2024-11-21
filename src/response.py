from curl_cffi.requests import Response
from src.exceptions import HTTPError


def check_response(response: Response) -> None:
    if response.status_code not in (200, 204):
        raise HTTPError(
            f"Failed to get response ({response.url}): {response.status_code} -- {response.text}"
        )
