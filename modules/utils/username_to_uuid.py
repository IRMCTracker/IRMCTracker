""" Username to UUID
 Converts a Minecraft username to it's UUID equivalent.

Uses the official Mojang API to fetch player data.

credit: https://github.com/EthanJoyce/MinecraftUsernameToUUID tnx buddy <3
"""
import http.client
import json


class UsernameToUUID:
    def __init__(self, username):
        self.username = username

    def get_uuid(self, timestamp=None):
        """
          Get the UUID of the player.

          Parameters
          ----------
          timestamp : long integer
              The time at which the player used this name, expressed as a Unix timestamp.
        """
        get_args = "" if timestamp is None else "?at=" + str(timestamp)

        http_conn = http.client.HTTPSConnection("api.mojang.com");
        http_conn.request("GET", "/users/profiles/minecraft/" + self.username + get_args,
            headers={'User-Agent':'Minecraft Username -> UUID', 'Content-Type':'application/json'});
        response = http_conn.getresponse().read().decode("utf-8")

        if (not response and timestamp is None): # No response & no timestamp
            return self.get_uuid(0) # Let's retry with the Unix timestamp 0.
        if (not response): # No response (player probably doesn't exist)
            return ""

        json_data = json.loads(response)
        try:
            uuid = json_data['id']
        except KeyError as e:
            print("KeyError raised:", e);

        return uuid