import json
import requests
class CloudRequestException(Exception):
    """
    Exception for handling errors of requests, especially when error occurs on the remote process. In this case, the remote process should return whit an error and a message within the body.
    """
    def __init__(self, error, message, description='The request failed'):
        self.error = error
        self.message = message
        self.description = description
        super().__init__(message)

    def __str__(self) -> str:
        return f"\t{type(self).__name__}:\n\t\t{self.description}\n\t\tMessage: {self.message}\n\t\tError: {self.error}"


class CloudRequest():
    """
    Class for sending requests to a service, uses requests package. It retrows the errors.  
    """
    def get_request(self, url, session_object, **kwargs):
        """
        request get method for handling response and reraise error if any occurred
        @param url (str): url
        @param session_object (requests.session):a requests.session instance
        @param **kvargs: keyword arguments to pass to requests.get() method 
        @raise CloudRequestException: raises if the returned response body contains any error
        @return response body as dict
        """
        response = {}
        print(kwargs)
        print(f"GET from {format(url)}")
        try:
            # Call get method of requests library with URL and parameters
            response = session_object.get(
                url, headers={
                    'Content-Type': 'application/json'}, **kwargs)
            status_code = response.status_code

            print(f"With status {format(status_code)}")
            print(response.text)
            json_data = json.loads(response.text)
            if json_data.get("error"):
                print(json_data["error"])
                if json_data.get("message"):
                    print(json_data["message"])
                else:
                    json_data["message"] = "some connection error"
                raise CloudRequestException(
                    json_data["error"], json_data["message"])
            response.raise_for_status()
            return json_data
        except requests.HTTPError as ht:
            print(ht)
            raise ht
        except CloudRequestException as re:
            print(str(re))
            raise re
        except Exception as err:
            print(err)
            raise err

    def post_request(self, url, session_object, **kwargs):
        """
        request post method for handling response and reraise error if any occurred
        @param url (str): url
        @param session_object (requests.session):a requests.session instance
        @param **kvargs: keyword arguments to pass to requests.post() method 
        @raise CloudRequestException: raises if the returned response body contains any error
        @return response body as dict
        """
        response = {}
        print(f"POST to {format(url)}")
        print(kwargs)
        try:
            # Call get method of requests library with URL and parameters
            response = session_object.post(
                url, headers={
                    'Content-Type': 'application/json'}, **kwargs)
            status_code = response.status_code
            print(f"With status {format(status_code)}")
            # print(response.text)
            json_data = json.loads(response.text)
            if json_data.get("error"):
                print(json_data["error"])
                if json_data.get("message"):
                    print(json_data["message"])
                else:
                    json_data["message"] = "Some connection error"
                raise CloudRequestException(
                    json_data["error"], json_data["message"])
            response.raise_for_status()
            return json_data
        except CloudRequestException as re:
            print(str(re))
            raise re
        except requests.HTTPError as ht:
            print(ht)
            raise ht
        except Exception as err:
            print(err)
            raise err

