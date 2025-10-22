"""Module used to read the SQL requests"""


class SQL:
    """SQL class to access the sql requests"""

    def __init__(self):
        # ========== USER ==========
        with open("app/sql/get_user.sql", "r", encoding="utf-8") as f:
            self.get_user = f.read()

        with open("app/sql/insert_user.sql", "r", encoding="utf-8") as f:
            self.insert_user = f.read()

        with open("app/sql/update_user.sql", "r", encoding="utf-8") as f:
            self.update_user = f.read()

        # ========== ACTIVITIES IMPORTS ==========
        with open("app/sql/get_activities_import.sql", "r", encoding="utf-8") as f:
            self.get_activities_import = f.read()

        with open("app/sql/insert_activities_import.sql", "r", encoding="utf-8") as f:
            self.insert_activities_import = f.read()

        with open("app/sql/update_activities_import.sql", "r", encoding="utf-8") as f:
            self.update_activities_import = f.read()
