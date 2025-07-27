"""Module used to read the SQL requests"""


class SQL:
    """SQL class to access the sql requests"""

    def __init__(self):
        with open("../sql/user_login.sql", "r", encoding="utf-8") as f:
            self.user_login = f.read()

    def format(self, request: str, to_replace: dict):
        """Formats a request with the given arguments"""
        return request.format(**to_replace)
