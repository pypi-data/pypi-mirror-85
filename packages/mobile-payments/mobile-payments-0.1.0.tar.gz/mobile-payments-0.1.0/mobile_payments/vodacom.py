from .open_api import APIContext, APIMethodType, APIRequest

BASE_URL = 'openapi.m-pesa.com'
get_session_url = '/sandbox/ipg/v2/vodacomTZN/getSession/'
c2bPayment_url = '/sandbox/ipg/v2/vodacomTZN/c2bPayment/singleStage/'
reversal_url = '/sandbox/ipg/v2/vodacomTZN/reversal/'
b2cPayment_url = '/sandbox/ipg/v2/vodacomTZN/b2cPayment/'
b2bPayment_url = '/openapi/ipg/v2/vodacomTZN/b2bPayment/'
transaction_status_url = '/openapi/ipg/v2/vodacomTZN/queryTransactionStatus/'


class MPESA:

    def __init__(self, api_key, public_key, ssl=True):
        """
        Generate context with API to request a Session ID.
        """
        self.context = APIContext(
            api_key, public_key, ssl=ssl, address=BASE_URL, port=443)
        self.context.add_header('Origin', '*')

    def get_encrypted_api_key(self):
        """
        Return encrypted API key.
        """
        return APIRequest(self.context).create_bearer_token()

    def get_session_id(self, path=get_session_url):
        """
        Return a valid Session ID needed to transact on M-Pesa using
        OpenAPI.
        """
        self.context.update({'method_type': APIMethodType.GET,
                             'path': path})

        response = None

        try:
            response = APIRequest(self.context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if response is None:
            raise Exception(
                'SessionKey call failed to get response. Please check.')
        else:
            return response.body['output_SessionID']

    def _get_api_response(self, context):
        """
        Return results from API call.
        """
        response = None
        try:
            response = APIRequest(context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if response is None:
            raise Exception('API call failed to get result. Please check.')
        else:
            return response

    def c2b(self, parameters: dict, path=c2bPayment_url):
        """
        A standard customer-to-business transaction

        parameters = {
            'input_Amount': 10,
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
                'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PurchasedItemsDesc': 'Shoes',
        }
        """

        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        response = self._get_api_response(self.context)
        return response

    def reversal(self, path, reversal_parameters: dict):
        """
        Reverse a successful transaction.

        reversal_parameters = {
            'input_ReversalAmount': '25',
            'input_Country': 'TZN',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
                'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionID': '0000000000001',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.PUT,
            'path': path,
            'parameters': {k: v for k, v in reversal_parameters.items()}
        })

        response = self._get_api_response(self.context)
        return response

    def b2c(self, parameters: dict, path=b2cPayment_url):
        """
        A standard customer-to-business transaction.

        parameters = {
            'input_Amount': '10',
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':
            'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PaymentItemsDesc': 'Salary payment',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        response = self._get_api_response(self.context)
        return response

    def b2b(self, parameters: dict, path=b2bPayment_url):
        """
        Business-to-business transactions (Single Stage).

        parameters = {
            'input_Amount': '10',
            'input_Country': 'TZN',
            'input_Currency': 'TZS',
            'input_CustomerMSISDN': '000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':'asv02e5958774f7ba228d83d0d689761',
            'input_TransactionReference': 'T1234C',
            'input_PaymentItemsDesc': 'Salary payment',
            }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.POST,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        response = None
        try:
            response = APIRequest(self.context).execute()
        except Exception as e:
            print('Call Failed: ', e)

        if response is None:
            raise Exception('API call failed to get result. Please check.')
        else:
            return response

    def query_transaction_status(self, parameters: dict,
                                 path=transaction_status_url):
        """
        Query the status of the transaction that has been initiated.

        parameters = {
            'input_QueryReference': '000000000000000000001',
            'input_ServiceProviderCode': '000000',
            'input_ThirdPartyConversationID':'asv02e5958774f7ba228d83d0d689761',
            'input_Country': 'TZN',
        }
        """
        self.context.update({
            'api_key': self.get_session_id(),
            'method_type': APIMethodType.GET,
            'path': path,
            'parameters': {k: v for k, v in parameters.items()}
        })

        response = self._get_api_response(self.context)
        return response
