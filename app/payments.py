import requests
from requests import Response
from stickmatic import app


class PaystackPay(object):
    """
     Paystack functions
    """
    def __init__(self):
        self.authorization_url = 'https://api.paystack.co/transaction/initialize'
        self.trans_verification_url = 'https://api.paystack.co/transaction/verify/{}'
        self.bvn_verification_url = 'https://api.paystack.co/bank/resolve_bvn/{}'

    def fetch_authorization_url(self, **kwargs):
        # always send email and amount
        response: Response = requests.post(self.authorization_url, json=kwargs,
                                           headers={'Authorization': f"Bearer {app.config.get('PAYSTACK_KEY')}"})
        return response

    def verify_reference_transaction(self, reference):
        response: Response = requests.get(self.trans_verification_url.format(reference),
                                          headers={'Authorization': f"Bearer {app.config.get('PAYSTACK_KEY')}"})

        return response
