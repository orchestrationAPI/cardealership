from cloudant.client import Cloudant
from cloudant.error import CloudantException, CloudantClientException
import requests

def main(args):
    SUCCESS_MESSAGE = 'Successful database query'
    client = None
    http_response = {}
    try:
        USERNAME = args["__bx_creds"]["cloudantnosqldb"]["username"]
        API_KEY =args["__bx_creds"]["cloudantnosqldb"]["apikey"]
        http_response = {
                "body" : {"datas": None},
                "statusCode" : 200,
                "headers" :{ 'Content-Type': 'application/json'}
                }
        dealer_id = args["dealerId"]
        db_name = "reviews"
        client = Cloudant.iam(
            account_name=USERNAME,
            api_key=API_KEY,
            connect=True,
        )
        if client is None:
            raise CloudantClientException()
        db = client[db_name]
        selector = {"dealership" :{"$eq" : int(dealer_id)}}
        reviews =  db.get_query_result(selector, raw_result=True, limit=50)
        if not reviews["docs"]:
            raise CloudantException("dealerId does not exist", code=404)
        for doc in reviews["docs"]:
            print(doc)
        http_response["body"]["docs"] = reviews["docs"]
        http_response["body"]["message"] = SUCCESS_MESSAGE
        return http_response
    except CloudantException  as ce:
        print(f"Error occured: {ce}, statusCode: {ce.status_code}")
        http_response["statusCode"] =str(ce.status_code) if ce.status_code else "500"
        http_response["body"]["message"] = "Database error occured"
        http_response["body"]["error"] = str(ce)
        return http_response
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print(f"Error occured: {err}")
        http_response["statusCode"] = "404"
        http_response["body"]["message"] = "Connection failed"
        http_response["body"]["error"] = str(repr(err))
        return http_response
    except Exception as err:
        print(f"Error occured: {repr(err)}")
        http_response["statusCode"] = "500"
        http_response["body"]["message"] = "Something went wrong on the server"
        http_response["body"]["error"] = str(repr(err))
        return http_response
    finally:
        if client is not None:
            client.disconnect()
            print("Session is closed")
