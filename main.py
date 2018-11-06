import glob
import json
import os
import uuid
from shutil import make_archive
from urllib import request


class alfred_emoji(object):
    def __init__(self):
        self.URL = "https://github.com/iamcal/emoji-data/raw/master/emoji.json"

    def get_data(self):

        with request.urlopen(self.URL) as response:
            emoji_data = json.loads(response.read())

        return emoji_data

    def translate(self, emoji_data):

        # Initialize snippet json
        snippet = {
            "alfredsnippet": {
                "snippet": "",
                "dontautoexpand": False,
                "uid": "",
                "name": "",
                "keyword": ""
            }
        }

        # Translation
        for emoji in emoji_data:

            # Assign file values
            snippet["alfredsnippet"]["snippet"] = chr(
                int(emoji["unified"].split("-")[0], 16))
            snippet["alfredsnippet"]["uid"] = str(uuid.uuid4())
            try:
                snippet["alfredsnippet"]["name"] = emoji["name"].lower()
            except AttributeError:
                snippet["alfredsnippet"]["name"] = " ".join(
                    emoji["short_name"].split("-"))
            snippet["alfredsnippet"]["keyword"] = emoji["short_name"]

            filename = "./product/" + snippet["alfredsnippet"][
                "name"] + " [" + snippet["alfredsnippet"]["uid"] + "].json"

            with open(filename, "w") as fp:
                json.dump(snippet, fp)

    def prepare_file(self):
        make_archive("./alfred-emoji", "zip", "./product")
        os.rename("./alfred-emoji.zip", "./alfred-emoji.alfredsnippets")

    def main(self):
        emoji_data = self.get_data()
        self.translate(emoji_data)
        self.prepare_file()


if __name__ == "__main__":
    afemj = alfred_emoji()
    afemj.main()
