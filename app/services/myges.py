import requests
from urllib.parse import urlparse, parse_qs

CLIENT_ID = "skolae-app"
USER_AGENT = "skolae-app-ios/3.5.0 (com.reseauges.skolae.app; build:26; iOS 15.0.1) Alamofire/4.9.1"
OAUTH_AUTHORIZE_URL = f"https://authentication.kordis.fr/oauth/authorize?client_id={CLIENT_ID}&response_type=token"
AGENDA_ENDPOINT_URL = "https://api.kordis.fr/me/agenda"

class myges:
    def __init__(self,LOGIN,PASSWORD) -> None:
        self.LOGIN = LOGIN
        self.PASSWORD = PASSWORD

    def get_access_token(self) -> str:
        response = requests.get(
            url=OAUTH_AUTHORIZE_URL,
            auth=(self.LOGIN, self.PASSWORD),
            allow_redirects=False,
        )

        if response.status_code == 401:
            raise Exception("Wrong credentials")

        access_token = self.extract_access_token(response.headers)

        return access_token
    
    def extract_access_token(self, headers) -> str:
        location = headers.get("Location")

        if not location:
            raise Exception("Location header not found")

        location_url = urlparse(location)

        if not location_url.fragment:
            raise Exception("Impossible to extract fragment")

        query_params = parse_qs(location_url.fragment)
        access_token = query_params.get("access_token")

        if not access_token:
            raise Exception("Impossible to extract access token")

        return access_token[0]

    def get_agenda(self, start, end) -> dict:
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
        }
        params = {
            "start": int(start) * 1000,
            "end": int(end) * 1000,
        }

        response = requests.get(url=AGENDA_ENDPOINT_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Unable to get the agenda, error {response.status_code}")

        response_data = response.json()

        if not response_data:
            raise Exception("No data in the agenda for date {start} to {end}")

        return response_data.get("result")