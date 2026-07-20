import requests


class HttpClient:
    def __init__(self, timeout=10):
        self.session = requests.Session()
        self.timeout = timeout

    def get(self, url, **kwargs):
        response = self.session.get(
            url,
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()