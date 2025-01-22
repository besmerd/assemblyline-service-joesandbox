import json
import time

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT

import jbxapi


class JoeSandbox(ServiceBase):

    def __init__(self, config=None):
        super(JoeSandbox, self).__init__(config)

    def start(self):
        self.log.debug("Joesandbox service started")

    def execute(self, request):

        result = Result()

        joe = jbxapi.JoeSandbox(
            apiurl=self.config.get("api_url"),
            apikey=self.config.get("api_key"),
            accept_tac=True,
            user_agent="AssemblyLine",
        )

        with open(request.file_path, "rb") as fh:
            sample = (request.file_name, fh)
            result = joe.submit_sample(sample)
            submission_id = result["submission_id"]
            self.log.info("Submitted sample with id: %s", submission_id)

        self.log.debug("Start to polling for submission id: %", submission_id)

        elapsed_time = 0
        while elapsed_time <= self.config.get("timeout"):
            submission = joe.submission_info(submission_id)
            if submission["status"] == "finished":
                break

            time.sleep(self.config.get("poll_interval"))

        report_link = submission["most_relevant_analysis"]["webid"]

        result.add_section(
            ResultSection(
                "JoeSandbox full report is available here:",
                body_format=BODY_FORMAT.URL,
                body=json.dumps({"name": "JoeSandbox report", "url": report_link}),
            )
        )

        request.result
