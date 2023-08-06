'''
python setup.py sdist
python -m twine upload -u DanielBR08 -p DWhouse130_ --repository-url https://upload.pypi.org/legacy/ dist/*

'''

import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import unidecode
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from google.oauth2 import service_account
from google.cloud import bigquery
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from glob import glob
import time
from google.colab import drive
import json
import os
from datetime import date, datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import criteo_marketing as cm
from criteo_marketing import Configuration



def add_numbers(num1,num2):
    return num1+num2


# def create_keyfile_dict():
#     variables_keys = {
#         "type": "service_account",
#         "project_id": "gspread-python-244519",
#         "private_key_id": "c5fc10405750137da1e1d7d7646464a8ba640b0c",
#         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCY6dekSTgUMIfL\n8PDQZfEtfBaZjEpw2C0MiyDJM55w16rlX7y4ZQ7pNowBpTLfIuZL+pp8Ns43CZKD\nSPTVgkMXnPyU+6vlDLyA5R9Mq4rV0QJBIuks5y0AoI+3D/uXF9V39DhjhT25CG3H\npiGBBar0oEq34/vnPRI3/mS2dV5H1ZB4Zcguus9hWpP7uGyv44eDkZHWxEgIi+oj\nDqTLzj6qZ8r8j1MYHPxBtgWiD9Ro3U2Okv7hsCM0QjjTvb8zR4AXyUytQdIa8Zz1\ny2J9FeZAFTT6kenklqDrkU7bFJV4LOauq4j0WRCfFKE6o1wRZQrMmtDJokU6wM3d\n92FSpHmdAgMBAAECggEAM+RznliMs+lOREsFZiuaP63TO5OM9aOfEhkq7KzcUX4X\nDFVDha4h88njlHFcBLZiwhkPESVGMQ5KDsyU7doRa7OGUgbgbFA4rmNTDmFOscYG\nxlUTHX5sWsCiVOUTI9DeTCFwe3GNozv1iWHbD959CBxXjvVLGMu0YZUu126YKrcM\nD2TXn6ot5C6nv37IQS1cU69pcYhANZ0wHW+ASGHtZDqOB3FZuuEdC/Q/OSMy7E17\nXZtW3cM8dVLEzQw1fXMQ8hj3s0oKDHMd0xSQAM4gwq26JCXWEIJrNJ4+pYKGaI/h\nROo1DrDZl1NUyzhqCJid8MSfZBqxAToPVsyGIT6Z7wKBgQDScdYQIQV9sDS2PHEx\niLf9lKGMbWooxOWeJ4vUa2CpN0qSi+lXCfzaAqopZcADOwiNubnrezIhr18sOly2\nad5i5nLdP9R2gFjNlH3Lt5HBjAmMYG14iTQKuL9Z/Y52lGHXXLEVOEfrMFADSdm4\njJhriMjeZSOoCAxjNSU1Cz/smwKBgQC6A8+/AATN8DJCEj10q+5lEgHmuZ/PUz3m\nPsV98gFOiwE/NVAeqioCusrtZi0uZCxiAhCRgLk5nujcUIddLKXkDu2Kx36M+QKZ\nqH3D7FKLMf/rgLXIqogeveWPyFwdKYg+Pspg8GmFVh/4C1/k8cpyOzWhyZW7UPoJ\njugW/6IqJwKBgFle7sG6xFI0Wq5pzMh0f265iEHS1Zqqw7j+omt7jnlOeeTydg34\nt+D98LXT+E9m6qMFlOdkUk3r5EcsIeN14nOt2moLiXcp2oyz2xiAxO2lQwjSiqr9\n2ZQUEW9uNuo06bhELRAN7rz6r4A2BLhTPQet92A7I4FgqaIYF80HEgaxAoGAPiF7\nyG43LJooD02MXWX4EKY9IFWr/VHugPNCf9jPeu6PEg+6nSN1OMgvc7AHM1GeSXYr\nFo6KT6a2XLBBJmv9VPlvekU8DdY2eiB/MWvD/l5K/txU25uqL6p5/NaNfegba78J\nVeu3MyQbNXyHIS9p0VHZjhqI+rIHch3bg6MLBU0CgYEAoezltvlbiiWBf032a9FM\nx93rS6qTIlz+RRRypjYslIKn/cJ8ylj5inusrS1yrmCPEAIWmfmhZXty0SdVJv5B\n4viq2dXTrrtBJfF75u7UzLVKKcQ2M4XuMfjBzSW0RT6A2KQoeiIA1ei/A9GCscqf\nTx60k9LxIgvjokA3bJK3dig=\n-----END PRIVATE KEY-----\n",
#         "client_email": "gspread-python@gspread-python-244519.iam.gserviceaccount.com",
#         "client_id": "111784061462585317776",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gspread-python%40gspread-python-244519.iam.gserviceaccount.com"
#     }
#     return variables_keys

