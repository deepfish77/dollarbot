from src.apis.api_requests import get_call, make_request


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
        print(api_result.json())
        return api_result.json()

    def update_bubble_object(self, object_id, key, data):
        constructed_url = self._construct_url_for_object(object_id=object_id)
        payload = {
            f"{key}": f"{data}",  # Replace with actual field names and values
        }
        response = make_request(
            method="patch",
            url=constructed_url,
            data=payload,
            headers=self._construct_headers(),
        )
        print("update object response, ", response.json())
        if response.status_code == 200:
            print("successfully updated object")
            return response.json()
        else:
            print("There was an error with the request", response.json())
            return False

    def update_bubble_object_multiple(self, object_id, payload):
        constructed_url = self._construct_url_for_object(object_id=object_id)
        response = make_request(
            method="patch",
            url=constructed_url,
            data=payload,
            headers=self._construct_headers(),
        )
        print("update object response, ", response.json())
        if response.status_code == 200:
            print("successfully updated object")
            return response.json()
        else:
            print("There was an error with the request", response.json())
            return False

    def get_all_objects(self):
        constructed_url = self._construct_url_for_object(object_id="")
        print("constructed_url", constructed_url)
        api_result = get_call(
            header=self._construct_headers(),
            url=constructed_url,
        )
        return api_result.json()


BubbleApiOperations("payments_all").execute_get_bubble_object(
    "1733736904127x254553459662782460"
)
