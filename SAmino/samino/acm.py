import json
import requests

from .lib import headers
from .lib.objects import *
from .lib.exception import CheckExceptions


class Acm:
    def __init__(self, comId: str):
        if comId is None: self.comId = None
        if comId is not None: self.comId = comId
        self.uid = headers.Headers().uid
        self.headers = headers.Headers().headers
        self.api = "https://service.narvii.com/api/v1"

    def promote(self, userId: str, rank: str):
        rank = rank.lower()
        if rank not in ["agent", "leader", "curator"]: raise TypeError(rank)
        rank = rank.replace("agent", "transfer-agent")
        req = requests.post(f"{self.api}/x{self.comId}/s/user-profile/{userId}/{rank}", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def accept_join_request(self, userId: str):
        req = requests.post(f"{self.api}/x{self.comId}/s/community/membership-request/{userId}/accept", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def reject_join_request(self, userId: str):
        req = requests.post(f"{self.api}/x{self.comId}/s/community/membership-request/{userId}/reject", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def change_welcome_message(self, message: str, enabled: bool = True):
        data = json.dumps({
            "path": "general.welcomeMessage",
            "value": {"enabled": enabled, "text": message}
        })
        req = requests.post(f"{self.api}/x{self.comId}/s/community/configuration", data=data, headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def change_guidelines(self, content: str):
        data = json.dumps({"content": content})
        req = requests.post(f"{self.api}/x{self.comId}/s/community/guideline", headers=self.headers, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def edit_community(self, name: str = None, description: str = None, aminoId: str = None, lang: str = None, themePackUrl: str = None):
        data = {}

        if name: data["name"] = name
        if description: data["content"] = description
        if aminoId: data["endpoint"] = aminoId
        if lang: data["primaryLanguage"] = lang
        if themePackUrl: data["themePackUrl"] = themePackUrl

        data = json.dumps(data)
        req = requests.post(f"{self.api}/x{self.comId}/s/community/settings", data=data, headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def get_community_stats(self):
        req = requests.get(f"{self.api}/x{self.comId}/s/community/stats", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return CommunityStats(req.json()["communityStats"])  # Still have no objects.. # Added Objects by Bovo -__-

    def get_admin_stats(self, type: str, start: int = 0, size: int = 25):
        type = type.lower()
        if type == "leader": pass
        elif type == "curator": pass
        else: raise TypeError(type)
        req = requests.get(f"{self.api}/x{self.comId}/s/community/stats/moderation?type={type}&start={start}&size={size}", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())  # Still have no objects..

    def get_join_requests(self, start: int = 0, size: int = 25):
        req = requests.get(f"{self.api}/x{self.comId}/s/community/membership-request?status=pending&start={start}&size={size}", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return JoinRequests(req.json())  # Still have no objects. # Added Objects by Bovo -______-

    def get_all_members(self, type: str, start: int = 0, size: int = 25):
        type = type.lower()
        req = requests.get(url=f"{self.api}/x{self.comId}/s/user-profile?type={type}&start={start}&size={size}", headers=self.headers)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return UserList(req.json()["userProfileList"])
