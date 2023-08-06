'''
python setup.py sdist
python -m twine upload -u DanielBR08 -p DWhouse130_ --repository-url https://upload.pypi.org/legacy/ dist/*

'''
#@title IMPORTS
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