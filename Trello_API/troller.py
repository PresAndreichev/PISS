import requests

class TrelloAPI:
    BASE_URL = "https://api.trello.com/1"

    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token

    def _make_request(self, method: str, endpoint: str, params: dict = None):
        if params is None:
            params = {}
        params.update({"key": self.api_key, "token": self.token})

        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.request(method, url, params=params)

        if not response.ok:
            response.raise_for_status()

        return response.json()

    def get_boards(self):
        """Get all boards for the authenticated user."""
        return self._make_request("GET", "members/me/boards")

    def create_board(self, name: str, desc: str = "", prefs: dict = None):
        """Create a new Trello board."""
        params = {"name": name, "desc": desc}
        if prefs:
            params.update(prefs)
        return self._make_request("POST", "boards", params)

    def get_cards(self, board_id: str):
        """Get all cards on a specific board."""
        return self._make_request("GET", f"boards/{board_id}/cards")

    def create_card(self, list_id: str, name: str, desc: str = ""):
        """Create a new card in a specific list."""
        params = {"idList": list_id, "name": name, "desc": desc}
        return self._make_request("POST", "cards", params)

    def update_card(self, card_id: str, fields: dict):
        """Update a card's details."""
        return self._make_request("PUT", f"cards/{card_id}", fields)

    def delete_card(self, card_id: str):
        """Delete a specific card."""
        return self._make_request("DELETE", f"cards/{card_id}")