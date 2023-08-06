import logging
from typing import Callable

from .base import API

logger = logging.getLogger(__name__)


start_integration_query = """
  mutation startIntegration($endpoint: String!, $host: String!, $secret: String!) {
    startIntegration(input: {endpoint: $endpoint, host: $host, secret: $secret}) {
      token
    }
  }
"""

finish_integration_query = """
  mutation finishIntegration($host: String!) {
    finishIntegration(input: {host: $host}) {
      jwt
    }
  }
"""

initiate_integration_mutation = """
  mutation initiateIntegration($host: String!, $organisation_name: String!, $bsecure_integration_secret: String!) {
      initiateIntegration(input: {
          host: $host, organisationName: $organisation_name, bsecureIntegrationSecret: $bsecure_integration_secret
          }) {
          jwt
      }
  }
"""


class IntegrationAPI(API):
    def integrate(self, prepare_endpoint: Callable, endpoint: str, host: str, secret: str) -> str:
        logging.warn("This is a deprecated endpoint please use initiate_integration")
        response_data = self.perform_query(
            start_integration_query,
            {"endpoint": endpoint, "host": host, "secret": secret},
        )
        token = response_data["startIntegration"]["token"]
        prepare_endpoint(token)
        response_data = self.perform_query(finish_integration_query, {"host": host})
        if not response_data["finishIntegration"]:
            response_data["finishIntegration"] = {"jwt": None}
        return response_data["finishIntegration"]["jwt"]

    def initiate_integration(
        self, host: str, organisation_name: str, bsecure_integration_secret: str
    ) -> str:
        """Integrate this host with BSecure. Returns a JWT token if successful."""
        response_data = self.perform_query(
            initiate_integration_mutation,
            {
                "organisation_name": organisation_name,
                "host": host,
                "bsecure_integration_secret": bsecure_integration_secret,
            },
        )
        jwt = response_data["initiateIntegration"]["jwt"]
        return jwt
