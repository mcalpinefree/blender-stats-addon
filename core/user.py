
import requests
import json

class User:
    def __init__(self, id, name, projectsJson):
        self.id = id
        self.name = name
        self.projects = json.loads(projectsJson)

    def save_as_current_user(self, addon_prefs):
        addon_prefs.user_id = self.id
        addon_prefs.user_name = self.name
        addon_prefs.projects = json.dumps(self.projects)

    def get_user_online(id):
        r = requests.get("https://api.blender-stats.staging.mcalpinefree.io/user",
                        headers={"Authorization": "Bearer " + id})
        response = json.loads(r.content)
        name = "Unknown"
        if "name" in response:
            name = response["name"]
        r = requests.get("https://api.blender-stats.staging.mcalpinefree.io/user/{}/projects".format(id),
                        headers={"Authorization": "Bearer " + id})

        return User(response["id"], name, r.content)

    def get_local_user(addon_prefs):
        return User(addon_prefs.user_id, addon_prefs.user_name, addon_prefs.projects)



        

    
