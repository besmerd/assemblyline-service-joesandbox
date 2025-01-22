import json
import time

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.request import ServiceRequest
from assemblyline_v4_service.common.result import BODY_FORMAT, Result, ResultSection

import jbxapi


class JoeSandbox(ServiceBase):

    def __init__(self, config=None):
        super(JoeSandbox, self).__init__(config)

    def start(self):
        self.log.debug("Joesandbox service started")

    def execute(self, request):


        joe = jbxapi.JoeSandbox(
            apiurl=self.config.get("api_url") or None,
            apikey=request.get_param("api_key") or self.config.get("api_key"),
            accept_tac=True,
            user_agent="AssemblyLine JoeSandbox Service",
        )


        with open(request.file_path, "rb") as fh:
            sample = (request.file_name, fh)
            submission_id = joe.submit_sample(sample).get('submission_id')
            self.log.info("Submitted sample with id: %s", submission_id)

        self.log.debug("Start to polling for submission id: %", submission_id)

        elapsed_time = 0
        while elapsed_time <= self.config.get("timeout"):
            submission = joe.submission_info(submission_id)
            if submission["status"] == "finished":
                break

            time.sleep(self.config.get("poll_interval"))

        report_link = submission["most_relevant_analysis"]["webid"]

        result = Result()

        result.add_section(
            ResultSection(
                "JoeSandbox full report is available here:",
                body_format=BODY_FORMAT.URL,
                body=json.dumps({"name": "JoeSandbox report", "url": report_link}),
            )
        )

        request.result
