from cloudant.client import Cloudant
from cloudant.error import CloudantException, CloudantClientException, CloudantDocumentException
import requests
import json
import datetime 
def main(args):
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

        print (args)
        data = {
                "id": int(args["id"]) if args.get("id") and args["id"] else None,
                  "name": args["name"] if args.get("name") and args["name"] else None,
                  "dealership": int(args["dealership"]) if args.get("dealership") and args["dealership"] else None,
                  "review": args["review"] if args.get("review") and args["review"] else None,
                  "review_date": args["review_date"] if args.get("review_date") and args["review_date"] else None,
                  "purchase": args["purchase"] if args.get("purchase") and args["purchase"] else None,
                  "purchase_date": args["purchase_date"] if args.get("purchase_date") and args["purchase_date"] else None,
                  "car_make": args["car_make"] if args.get("car_make") and args["car_make"] else None,
                  "car_model": args["car_model"] if args.get("car_model") and args["car_model"] else None,
                  "car_year": args["car_year"] if args.get("car_year") and args["car_year"] else None
                }

        db_name = "reviews"
        client = Cloudant.iam(
            account_name=USERNAME,
            api_key=API_KEY,
            connect=True,
        )
        if client is None:
            raise CloudantClientException()
        db = client[db_name]
        document = db.create_document(data)
        if document.exists() is None:
            raise CloudantDocumentException()
        http_response["statusCode"] = 200
        http_response["body"]["message"] = "The review is saved succesfuly to the database."
        http_response["body"]["date"] = str(datetime.datetime.now())
        print("Document created succesfuly.")
        return http_response
    except CloudantException  as ce:
        print(f"Error occured: {ce}, statusCode: {ce.status_code}")
        http_response["statusCode"] =str(ce.status_code) if ce.status_code else "500"
        http_response["body"] = str(ce)
        return http_response
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print(f"Error occured: {err}")
        http_response["statusCode"] = "404"
        http_response["body"]["message"] = "Connection failed"
        http_response["body"]["error"] = str(err)
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

