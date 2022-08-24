from . import load_env

import os
import sys
import logging
import azure.functions as func
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()
# Define project main path
MAIN_FOLDER = os.getenv('MAIN_PATH')

sys.path.insert(0, os.path.join(os.getcwd(), os.path.join(MAIN_FOLDER, "src") ))

from . import locksmiths


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    test = req.params.get('test')
    if not test:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            test = req_body.get('test')
            
    special = req.params.get('special')
    if not test:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            special = req_body.get('special')

    try:
        response = locksmiths.send_locksmiths_report(special, test)
        message = f"Report send to Telegram Chat. This HTTP triggered function executed successfully.\n\nspecial={special},\ntest={test}"
        if response:
            return  func.HttpResponse(f"This HTTP triggered function FAIL.\n\nspecial={special},\ntest={test}\n\nERROR:\n{response}",
                                      status_code=500)
        return  func.HttpResponse(message)
    except Exception as e:
        return func.HttpResponse(
             f"This HTTP triggered function FAIL successfully.\n\n{str(e)}",
             status_code=500
        )
