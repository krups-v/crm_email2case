from flask import Flask, request
import re
from simple_salesforce import Salesforce

sf_login = {
    'username': '',
    'password': '',
    'token': ''
}

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index():
        req_data = request.get_json()
        body = req_data['body']
        res = re.search(r"Asset: (\d{8})\r\n", body)
        name = re.search(r"Contact: (\[A-Z]{8})\r\n", body)
        asset = res.group(1)
        sf = Salesforce(username=sf_login['username'], password=sf_login['password'], security_token=sf_login['token'])
        asset = sf.Asset.get_by_custom_id('Name', asset)
        contac = sf.Contact.get_by_custom_id('Email', name)
        print(asset['Id'])
        res_create_case = sf.Case.create({'AssetId': asset['Id'], 'Subject': req_data['subject'], 'Description': req_data['body'], 'ContactId': contac['Id']})
        if res_create_case['success']:
            res_case = sf.Case.get(res_create_case['id'])
            return 'Case {} successfully created'.format(res_case['CaseNumber'])
        else:
            return 'Case was not created, something went wrong'