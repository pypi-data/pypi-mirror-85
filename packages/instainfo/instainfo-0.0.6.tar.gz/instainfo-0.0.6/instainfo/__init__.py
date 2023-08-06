import requests
import json


class UserProfile:
    USER_API_URL = None
    USER_DATA = None

    def __init__(self, username):
        self.USER_API_URL = "https://www.instagram.com/{}/?__a=1".format(
            username)
        self.USER_DATA = requests.get(self.USER_API_URL).json()

    def GetProfilePicURL(self):
        return(self.USER_DATA['graphql']['user']['profile_pic_url_hd'])

    def IsPrivate(self):
        return(bool(self.USER_DATA['graphql']['user']['is_private']))

    def IsBusinessAccount(self):
        return(bool(self.USER_DATA['graphql']['user']['is_business_account']))

    def IsJoinedRecently(self):
        return(bool(self.USER_DATA['graphql']['user']['is_joined_recently']))

    def FollowersCount(self):
        return(self.USER_DATA['graphql']['user']['edge_follow']['count'])

    def FollowedByCount(self):
        return(self.USER_DATA['graphql']['user']['edge_followed_by']['count'])
