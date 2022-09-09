"""
This is the Gumshoe add-on for DocumentCloud.

It runs the Gumshoe machine learning model on a collection of DocumentCloud
documents
"""

import time

import requests
from documentcloud.addon import AddOn

URL = "https://us-central1-gumshoe-muckrock-0ce3.cloudfunctions.net/gumshoe3"
POLL_INTERVAL = 120


class Gumshoe(AddOn):

    def get_progress(self):
        """Get the progress for the current run."""
        if not self.id:
            return None
        resp = self.client.get(f"addon_runs/{self.id}/")
        if resp.status_code == 200:
            return resp.json()["progress"]

        return None


    def main(self):
        # fetch your add-on specific data
        relevant = self.data.get("relevant", "")
        irrelevant = self.data.get("irrelevant", "")
        email = self.data.get("email", "")
        run_id = self.id

        document_ids = [d.id for d in self.get_documents()]

        resp = requests.post(
            URL,
            json={
                "doc_cloud_ids": document_ids,
                "doc_cloud_token": self.client.refresh_token,
                "relevant_keywords": relevant,
                "irrelevant_keywords": irrelevant,
                "email": email,
                "run_id": run_id,
            },
        )

        if resp.status_code != 200:
            self.set_message("Error submitting request")

        self.set_message("Request submitted, please wait for the request to process")
        progress = 0
        while progress != 100:
            progress = self.get_progress()
            print(progress)
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    Gumshoe().main()
