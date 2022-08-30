"""
This is the Gumshoe add-on for DocumentCloud.

It runs the Gumshoe machine learning model on a collection of DocumentCloud
documents
"""

import requests
from documentcloud.addon import AddOn

URL = "https://us-central1-gumshoe-muckrock-0ce3.cloudfunctions.net/gumshoe3"


class Gumshoe(AddOn):
    def main(self):
        # fetch your add-on specific data
        relevant = self.data.get("relevant", "")
        irrelevant = self.data.get("irrelevant", "")
        email = self.data.get("email", "")

        document_ids = [d.id for d in self.get_documents()]

        resp = requests.post(
            URL,
            json={
                "doc_cloud_ids": document_ids,
                "doc_cloud_token": self.client.refresh_token,
                "relevant_keywords": relevant,
                "irrelevant_keywrods": irrelevant,
                "email": email,
            },
        )

        if resp.status_code != 200:
            self.set_message("Error submitting request")

        self.set_message("Request submitted, please wait for the request to process")


if __name__ == "__main__":
    Gumshoe().main()
