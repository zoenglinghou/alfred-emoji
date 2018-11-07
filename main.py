import json
import os
import re
import uuid
from glob import glob
from shutil import make_archive
from urllib import request


class alfred_emoji(object):
    def __init__(self):
        self.URL = "https://github.com/iamcal/emoji-data/raw/master/emoji.json"
        self.products_path = "./products"

    def remove_old(self):
        for old_snippet in glob(os.path.join(self.products_path, '*.json')):
            os.remove(old_snippet)

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
                    re.split("-|_", emoji["short_name"]))
            snippet["alfredsnippet"]["keyword"] = emoji["short_name"]

            filename = os.path.join(
                self.products_path, snippet["alfredsnippet"]["name"] + " [" +
                snippet["alfredsnippet"]["uid"] + "].json")

            with open(filename, "w") as fp:
                json.dump(snippet, fp)

    def prepare_file(self):
        make_archive("./alfred-emoji", "zip", self.products_path)
        os.rename("./alfred-emoji.zip", "./alfred-emoji.alfredsnippets")

    def main(self):
        self.remove_old()
        emoji_data = self.get_data()
        self.translate(emoji_data)
        self.prepare_file()


if __name__ == "__main__":
    afemj = alfred_emoji()
    afemj.main()
