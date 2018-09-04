import json
import upwork
import csv


class UpworkClient(object):
    def __init__(self):
        self.public_key = ""
        self.secret_key = ""
        self.client = upwork.Client(self.public_key, self.secret_key)

    def write_usernames_to_csv(self, room):
        output = csv.StringIO()
        writer = csv.writer(output)
        for userId in room.users:
            user = self.client.hr.get_user(userId)
            writer.writerow(user.username)
        output.seek(0)
        return output.readlines()

    def run(self):
        print("Please to this URL (authorize the app if necessary):")
        print(self.client.auth.get_authorize_url())
        print("After that you should be redirected back to your app URL with " +
              "additional ?oauth_verifier= parameter")

        verifier = input('Enter oauth_verifier: ')

        oauth_access_token, oauth_access_token_secret = self.client.auth.get_access_token(verifier)

        self.client.oauth_access_token = oauth_access_token
        self.client.oauth_access_token_secret = oauth_access_token_secret

        response = json.loads(self.client.messages.get_rooms('StarNavi'))
        room = json.loads(self.client.messages.get_room_details('StarNavi', response.rooms[0].roomId))
        print(room)
        self.write_usernames_to_csv(room)


if __name__ == "__main__":
    client = UpworkClient()
    client.run()
