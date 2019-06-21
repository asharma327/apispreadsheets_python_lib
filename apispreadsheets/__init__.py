name = "apispreadsheets"

import requests

class APISpreadsheets:

    def __init__(self, file_id, output_format=None, accessKey=None, secretKey=None):
        self.file_id = file_id

        if output_format not in ['jsonRow', 'jsonColumn', 'matrix']:
            raise ValueError("Output format must be jsonRow, jsonColumn or matrix or not used. Default is jsonRow")
        else:
            self.output_format = output_format

        if (accessKey is None and secretKey is not None) or (secretKey is None and accessKey is not None):
            raise ValueError("Both access and secret key parameters must have values or not be used")
        else:
            self.accessKey = accessKey
            self.secretKey = secretKey

        self.base_url = "https://api-woyera.com/api/data/"

    def get_data(self):
        output = "jsonRow" if self.output_format is None else self.output_format

        url = self.base_url + str(self.file_id) + "/" + output + "/"

        if self.accessKey is None and self.secretKey is None:
            r = requests.get(url)

            get_status_code = r.status_code

            if get_status_code == 200:
                return r.json()
            elif get_status_code == 400:
                raise ValueError("The file is private. Please provide access and secret keys")
            elif get_status_code == 404:
                raise ValueError("This file ID does not exist. Please find the correct ID from your dashboard")
            else:
                raise ValueError("There was something wrong on our server. Try again or contact us at info@apispreadsheets.com if the problem persists")
        else:
            r = requests.post(url, headers={'accessKey': self.accessKey, 'secretKey': self.secretKey})

            post_status_code = r.status_code

            if post_status_code == 200:
                return r.json()
            elif post_status_code == 401:
                raise ValueError("The Access or Secret key is invalid")
            elif post_status_code == 404:
                raise ValueError("This file ID does not exist or is not your file. Please find the correct ID from your dashboard")
            else:
                raise ValueError("There was something wrong on our server. Try again or contact us at info@apispreadsheets.com if the problem persists")
