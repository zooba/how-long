import os
import requests

from datetime import date

LENGTH_OF_EMPLOYMENT_SERVICE = "https://ussouthcentral.services.azureml.net/workspaces/9c3d243c5e8b4ae2bd17f5aafc46e781/services/0d21128f027843f89fdeb1f681d80893/execute?api-version=2.0&details=true"
LENGTH_OF_EMPLOYMENT_KEY = os.getenv('LENGTH_OF_EMPLOYMENT_KEY')

def length_of_employment(department, start_date):
    if not LENGTH_OF_EMPLOYMENT_KEY:
        return 0
    
    resp = requests.post(
        LENGTH_OF_EMPLOYMENT_SERVICE,
        json={
            "Inputs": {
                "input1": {
                    "ColumnNames": [ "department", "start_date", "days" ],
                    "Values": [[department, (date.today() - start_date).days, 0]],
                }
            },
            "GlobalParameters": {}
        },
        headers={
            "Authorization": 'Bearer ' + LENGTH_OF_EMPLOYMENT_KEY,
            "Accept": "application/json",
        }
    ).json()

    return int(float(resp["Results"]["output1"]["value"]["Values"][0][3]))
