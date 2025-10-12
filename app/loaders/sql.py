"""Module used to read the SQL requests"""


class SQL:
    """SQL class to access the sql requests"""

    def __init__(self):
        with open("app/sql/save_user.sql", "r", encoding="utf-8") as f:
            self.save_user = f.read()

        with open("app/sql/get_user.sql", "r", encoding="utf-8") as f:
            self.get_user = f.read()

    def format_request(self, request: str, to_replace: dict):
        """Formats a request with the given arguments"""
        return request.format(**to_replace)
