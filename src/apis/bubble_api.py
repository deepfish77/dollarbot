import boto3
from src.apis.api_requests import get_call, make_request

ssm = boto3.client("ssm")

# X_API_KEY = ssm.get_parameter(Name="/api/bubble", WithDecryption=True)["Parameter"][
#     "Value"
# ]

BUBBLE_BASE_URL = "https://makeuity.com/version-test/api/1.1/obj/"

ENPOINTS_DICT = {
    "payments_all": "bot_payments",
}


class BubbleApiOperations:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def _construct_url_for_object(self, object_id):
        constructed_url = (
            f"""{BUBBLE_BASE_URL}{ENPOINTS_DICT.get(self.endpoint)}/{object_id}"""
        )
        return constructed_url

    def _construct_headers(self):
        return {
            "x-api-key": "59c96877b645605213b97af46b7203fa",  # Put in param Store!! soon!!
            "Content-Type": "application/json",
        }

    def execute_get_bubble_object(self, object_id):
        constructed_url = self._construct_url_for_object(object_id=object_id)
        api_result = get_call(
            header=self._construct_headers(),
            url=constructed_url,
        )
        return api_result

    def update_bubble_object(self, object_id, key, data):
        constructed_url = self._construct_url_for_object(object_id=object_id)
        payload = {
            key: data,  # Replace with actual field names and values
        }
        # print("payload, ", payload)
        # print("URL:", constructed_url)
        # print("Headers:", self._construct_headers())
        response = make_request(
            method="patch",
            url=constructed_url,
            json=payload,
            headers=self._construct_headers(),
        )
        print("update object response, ", response)
        if response.status_code >= 200 <= response.status_code < 300:
            print("successfully updated object")
            return True
        else:
            print("There was an error with the request", response)
            return False

    def update_bubble_object_multiple(self, object_id, payload):
        constructed_url = self._construct_url_for_object(object_id=object_id)
        response = make_request(
            method="patch",
            url=constructed_url,
            data=payload,
            headers=self._construct_headers(),
        )
        print("update object response, ", response)
        if response.status_code == 200 <= response.status_code < 300:
            print("successfully updated object")
            return True
        else:
            print("There was an error with the request", response)
            return False

    def get_all_objects(self):
        constructed_url = self._construct_url_for_object(object_id="")
        print("constructed_url", constructed_url)
        api_result = get_call(
            header=self._construct_headers(),
            url=constructed_url,
        )
        return api_result


# BubbleApiOperations("payments_all").update_bubble_object(
#     "1733736904127x254553459662782460", "stripe_order", "lets see if this works"
# )
