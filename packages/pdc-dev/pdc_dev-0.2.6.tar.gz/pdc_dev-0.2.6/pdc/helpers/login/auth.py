import requests
from pdc import settings
from pdc.helpers.login.Tuser import Tuser

class Api():

    def pdcLoginCheck(token):
        loginCheck = False
        try:
            response = requests.get(settings.PDC_SWARM_AUTHORIZATOR_API + "isauthenticated/?token=" + token)
            if response.json()["authenticated"] == "true":
                loginCheck = True
        except:
            loginCheck = False
        return loginCheck

    def pdcGetUser(token):
        response = requests.get(settings.PDC_SWARM_AUTHORIZATOR_API + "getuser/?token=" + token)
        user = Tuser(response.json()["username"], response.json()["email"], response.json()["admin"])
        return user
