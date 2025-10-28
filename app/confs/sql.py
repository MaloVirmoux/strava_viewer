"""Module used to read the SQL requests"""


class SQL:
    """SQL class to access the sql requests"""

    def __init__(self):
        # ========== USER ==========
        folder = "app/sql/users"
        with open(f"{folder}/get_user.sql", "r", encoding="utf-8") as f:
            self.get_user = f.read()

        with open(f"{folder}/insert_user.sql", "r", encoding="utf-8") as f:
            self.insert_user = f.read()

        with open(f"{folder}/update_user.sql", "r", encoding="utf-8") as f:
            self.update_user = f.read()

        # ========== ACTIVITIES ==========
        folder = "app/sql/activities"
        with open(f"{folder}/get_activities.sql", "r", encoding="utf-8") as f:
            self.get_activities = f.read()

        with open(f"{folder}/insert_activity.sql", "r", encoding="utf-8") as f:
            self.insert_activity = f.read()

        with open(f"{folder}/delete_activities.sql", "r", encoding="utf-8") as f:
            self.delete_activities = f.read()

        # ========== ACTIVITIES IMPORTS ==========
        folder = "app/sql/activities_imports"
        with open(f"{folder}/get_activities_import.sql", "r", encoding="utf-8") as f:
            self.get_activities_import = f.read()

        with open(f"{folder}/insert_activities_import.sql", "r", encoding="utf-8") as f:
            self.insert_activities_import = f.read()

        with open(f"{folder}/update_activities_import.sql", "r", encoding="utf-8") as f:
            self.update_activities_import = f.read()
