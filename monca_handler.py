from typing import List

from monca_client import MoncaClient, MoncaRequest, MoncaResponse, VariantInput


class MoncaBinomial:
    def __init__(self, api_key: str):
        self.monca_client: MoncaClient = MoncaClient(api_key)
        self.monca_response: MoncaResponse = None

    def _construct_monca_request(
        self, variants: List[VariantInput], return_posteriors: bool = False
    ):
        return MoncaRequest(variants, return_posteriors=return_posteriors)

    def run_analysis(
        self, variants: List[VariantInput], return_posteriors: bool = False
    ):
        monca_request = self._construct_monca_request(
            variants, return_posteriors=return_posteriors
        )
        self.monca_response = self.monca_client.perform_ab_test(monca_request)

    def __str__(self):
        return f"<MoncaBinomial client={self.monca_client}>"
