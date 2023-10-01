import azure.functions as func
from azure.communication.email import EmailClient
import json
import os
from dotenv import load_dotenv


load_dotenv()
connection_string = os.getenv("MAPS_CONNECTION_STRING")


def main(request: func.HttpRequest) -> func.HttpResponse:
    if request.method == "GET":
        user_request = request.get_json()
        user_email = user_request['email']

        try:
            client = EmailClient.from_connection_string(connection_string)

            message = {
                "senderAddress": "DoNotReply@17ea2d74-5675-4e8b-8541-f5826d818e63.azurecomm.net",
                "recipients": {
                    "to": [{"address": f"{user_email}"}],
                },
                "content": {
                    "subject": "Weather Alerts",
                    "plainText": "Welcome! Thank you for subscribing to weather alerts.",
                }
            }

            poller = client.begin_send(message)
            result = poller.result()
            print(result)
            return func.HttpResponse(json.dumps({"message": "success"}))

        except Exception as ex:
            print(ex)
            return func.HttpResponse(json.dumps({"message": "failed"}))
