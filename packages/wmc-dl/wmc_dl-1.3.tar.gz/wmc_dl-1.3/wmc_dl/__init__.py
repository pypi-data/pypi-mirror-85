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

#@title FUNÇÕES
def create_keyfile_dict():
    variables_keys = {
        "type": "service_account",
        "project_id": "gspread-python-244519",
        "private_key_id": "c5fc10405750137da1e1d7d7646464a8ba640b0c",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCY6dekSTgUMIfL\n8PDQZfEtfBaZjEpw2C0MiyDJM55w16rlX7y4ZQ7pNowBpTLfIuZL+pp8Ns43CZKD\nSPTVgkMXnPyU+6vlDLyA5R9Mq4rV0QJBIuks5y0AoI+3D/uXF9V39DhjhT25CG3H\npiGBBar0oEq34/vnPRI3/mS2dV5H1ZB4Zcguus9hWpP7uGyv44eDkZHWxEgIi+oj\nDqTLzj6qZ8r8j1MYHPxBtgWiD9Ro3U2Okv7hsCM0QjjTvb8zR4AXyUytQdIa8Zz1\ny2J9FeZAFTT6kenklqDrkU7bFJV4LOauq4j0WRCfFKE6o1wRZQrMmtDJokU6wM3d\n92FSpHmdAgMBAAECggEAM+RznliMs+lOREsFZiuaP63TO5OM9aOfEhkq7KzcUX4X\nDFVDha4h88njlHFcBLZiwhkPESVGMQ5KDsyU7doRa7OGUgbgbFA4rmNTDmFOscYG\nxlUTHX5sWsCiVOUTI9DeTCFwe3GNozv1iWHbD959CBxXjvVLGMu0YZUu126YKrcM\nD2TXn6ot5C6nv37IQS1cU69pcYhANZ0wHW+ASGHtZDqOB3FZuuEdC/Q/OSMy7E17\nXZtW3cM8dVLEzQw1fXMQ8hj3s0oKDHMd0xSQAM4gwq26JCXWEIJrNJ4+pYKGaI/h\nROo1DrDZl1NUyzhqCJid8MSfZBqxAToPVsyGIT6Z7wKBgQDScdYQIQV9sDS2PHEx\niLf9lKGMbWooxOWeJ4vUa2CpN0qSi+lXCfzaAqopZcADOwiNubnrezIhr18sOly2\nad5i5nLdP9R2gFjNlH3Lt5HBjAmMYG14iTQKuL9Z/Y52lGHXXLEVOEfrMFADSdm4\njJhriMjeZSOoCAxjNSU1Cz/smwKBgQC6A8+/AATN8DJCEj10q+5lEgHmuZ/PUz3m\nPsV98gFOiwE/NVAeqioCusrtZi0uZCxiAhCRgLk5nujcUIddLKXkDu2Kx36M+QKZ\nqH3D7FKLMf/rgLXIqogeveWPyFwdKYg+Pspg8GmFVh/4C1/k8cpyOzWhyZW7UPoJ\njugW/6IqJwKBgFle7sG6xFI0Wq5pzMh0f265iEHS1Zqqw7j+omt7jnlOeeTydg34\nt+D98LXT+E9m6qMFlOdkUk3r5EcsIeN14nOt2moLiXcp2oyz2xiAxO2lQwjSiqr9\n2ZQUEW9uNuo06bhELRAN7rz6r4A2BLhTPQet92A7I4FgqaIYF80HEgaxAoGAPiF7\nyG43LJooD02MXWX4EKY9IFWr/VHugPNCf9jPeu6PEg+6nSN1OMgvc7AHM1GeSXYr\nFo6KT6a2XLBBJmv9VPlvekU8DdY2eiB/MWvD/l5K/txU25uqL6p5/NaNfegba78J\nVeu3MyQbNXyHIS9p0VHZjhqI+rIHch3bg6MLBU0CgYEAoezltvlbiiWBf032a9FM\nx93rS6qTIlz+RRRypjYslIKn/cJ8ylj5inusrS1yrmCPEAIWmfmhZXty0SdVJv5B\n4viq2dXTrrtBJfF75u7UzLVKKcQ2M4XuMfjBzSW0RT6A2KQoeiIA1ei/A9GCscqf\nTx60k9LxIgvjokA3bJK3dig=\n-----END PRIVATE KEY-----\n",
        "client_email": "gspread-python@gspread-python-244519.iam.gserviceaccount.com",
        "client_id": "111784061462585317776",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gspread-python%40gspread-python-244519.iam.gserviceaccount.com"
    }
    return variables_keys


def connect_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scope)
    gc = gspread.authorize(credentials=credentials)
    return gc

def read_google_sheet(gc, sheetname, worksheet):
    wks = gc.open(sheetname).worksheet(worksheet)
    records = wks.get_all_records()
    dataframe = pd.DataFrame.from_dict(records)

    return dataframe

def google_spreadsheet_to_bq(
        sheetname,
        worksheet,
        project_id, schema, table_name,
        df_columns=None):
    '''
    Leitura da tabela do Google SpreadSheet
    '''
    gc = connect_google_sheet()
    df_gspread = read_google_sheet(gc, sheetname=sheetname, worksheet=worksheet)
    df_gspread = df_gspread[df_columns]

    '''
    Padronização dos nomes das colunas para o Google BigQuery
    '''

    try:
        # print(df_columns)
        if df_columns is None:
            df_columns = df_gspread.columns.to_list()
        print(df_columns)
    except NameError:
        df_columns = df_gspread.columns.to_list()

    col_names = [col.lower().replace(' ', '_').replace('&', 'e') for col in df_columns]
    col_names = [col.lower().replace('(', '').replace(')', '') for col in col_names]
    col_names = [col.lower().replace('-', '_').replace('%', 'perc') for col in col_names]
    col_names = [col.lower().replace('.', '') for col in col_names]
    col_names = [unidecode.unidecode(col) for col in col_names]

    df_gspread.columns = col_names

    '''
    Tratamento de valores decimais
    '''

    for col in col_names:
        col_type = df_gspread[col].dtype.str
        if col_type == '|O':
            df_gspread[col] = df_gspread[col].apply(lambda x: x.replace(',', '.') if isinstance(x, str) else x)

    '''
    Envio da tabela para o Google Big Query
    '''
    # df_gspread.to_gbq(
    #     destination_table=schema + '.' + table_name,  # Dataset.Tablename
    #     project_id=project_id,  # Project Id extracted from Big Query credentials
    #     chunksize=None,
    #     if_exists='replace'  # 'fail', 'replace' or 'append'
    # )
    credentials_info = create_keyfile_dict_google_big_query_nestle_br()
    credentials = service_account.Credentials.from_service_account_info(credentials_info)


    df_gspread.to_gbq(
        destination_table=schema + '.' + table_name,  # Dataset.Tablename
        project_id=project_id,  # Project Id extracted from Big Query credentials
        chunksize=None,
        if_exists='replace',  # 'fail', 'replace' or 'append'
        credentials=credentials
    )

    time.sleep(5)

    print("Tabela " + table_name + " criada em " + project_id + "." + schema)



def create_keyfile_dict_google_big_query_nestle_br():
    variables_keys = {
        "type": "service_account",
        "project_id": "nestle-br",
        "private_key_id": "351fb0b1ae372df2df0d0d5bdcf5647d3788ec5c",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCpXNvV0L9BNz0u\n/2tTY+QGMzVdSHDfpHw86Wy38t2cmhVt3+SQQcPh14GC+hOaus4ZpLqKS5etnrLL\nJ5sNurCWOnFufY2BAd++uUNzg/pOeJfKzHX1wpDZDY7w9wq0oenbHqsl6FiQN4wr\n7mD5Fr0w1ZP0RRrUmqPHg4t3TTLf2captdxBiUhWCn+tJrM8j7yod82UpERxYMbd\nWipOid3ajkaow8AGUXZvJiyKDMoOK9EKJBNI5zFxjKKhOlAJeW6gbOhSl74pA/Ui\n0ffXj/+T9hN7ixjU7v4NN1sHOvJXLgKd4E5SjS/jzi6jAPGgvnZD0FRvKPtPrsk6\na2DU/prFAgMBAAECggEAJoaVC2Jc3zztkg9QHrwOVsq3TOz5oCYOjNyceouolcMH\nNONFXvtWz7zyHRU9+GieEX9DX8oqSrha+5Oa1dit6r6IpxWwZrRCbWQ/T7up6MfN\n37f67VjBEl7fMTlBGi3qwImNbSYZX1UDccrcDE174+vxqBNAMzSqJOxrgUvyUrEc\ndoW63DL6+skob3KPkQdr3NUdNgmKvTA0oj6MR3Lehwk2Cm3Oh3YGLH8q7bp1bDo2\n9xplmkV0Pt0wJ5Cl0w3/036vA7efGaPB7ZCGKYiHwLAHKt7A1OrgBkBbVO++G6jn\nwWRVswO151RaqResfGtq+plWBFgptlwZp09UaIvVgQKBgQDc08VCquEVtADMMg3O\nP1RS7y5/4gxISs3+sOLfHIS8k5nMNhunHEq/K1T7DIcDe8IlB9ky0b1MARl24vIY\nv9pxstNLtTn+lhQtnmQ2m3/0ENNTgDoZdrzwN2v3lWmmspdKt/coN1ZBJR9Hqr8E\nMsyybDTdwZvffKviqVUq8g17eQKBgQDEVp+X1pLrKssSMO52VwZNSFi5I+GsfpSs\nhOGl5dwW32DH3Ymm8GebRAAMYiky6lbvGC44yWY60BuKuc24s2dNIUdq+xR6hVsl\nZBpw5y/TTfmbu78/L0lkSz6NDBtJ75zpCgn/Twy+D8PRYHxakrGwgZrEIQwCOqFd\nEEersD76rQKBgQCDbXKgzAzsmtZCsaOv1dc9COd26zV+LS9O3z4XpeSGS56kgKuS\nmO8Puh140Srl8tlIqtQlP9lXC+x46ndGLaE4PEMvcuvSTsYxpGxmZ8QOoZj0wINT\ntmya15FlqEJaGT6cFMN/5vdqDEsCn2fSet2Db41DUkCQEaZHX5q11ZwamQKBgFy9\nPe0OoZ8LO5iAHGMxf/yJK79nv3Um5TsIGT2vcWIsaR5++kIsVAP2/r7arvMp1Z5i\nIZMZLnyhSCEi2pVfyG+aRI23w1iMHR1wRz0FNoXs0vZInHFP+K6zC/y7tzgZQlih\nMU+zGyW7dJc1qAdwOxZQYbY6ld2HrCi1Q+VI/raRAoGBAMW5g8mJEkge1VtYjVuM\nqT4koPWJIi+8ufg0bQtak0HHu5siBi8gGie/mpayWmVZ+2JZGZxlzu3t/bX4Wagy\nQIHJv9cosvAbkvIYONe1JKoZbHEUoe2MdbjIVoOI6Fboc8xkpYx+o3ZVEfvQwm3/\niy+ANIN9Nn80o62441NoTGuD\n-----END PRIVATE KEY-----\n",
        "client_email": "analyst@nestle-br.iam.gserviceaccount.com",
        "client_id": "114418917477877634367",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/analyst%40nestle-br.iam.gserviceaccount.com"
    }
    return variables_keys


def connect_google_big_query():
    credentials_info = create_keyfile_dict_google_big_query_nestle_br()
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    client = bigquery.Client(
        credentials=credentials,
        project='nestle-br',
    )
    return client


def csv_file_to_bq(
    file_path, encoding,
    skiprows, sep,
    df_columns, project_id,
    schema, table_name
):

    import pandas as pd
    import codecs

    doc = codecs.open(file_path, 'rU', encoding)  # open for reading with "universal" type set
    df_csv = pd.read_csv(doc, skiprows=skiprows, sep=sep)

    df_csv = df_csv[df_columns]

    try:
        # print(df_columns)
        if df_columns is None:
            df_columns = df_csv.columns.to_list()
        print(df_columns)
    except NameError:
        df_columns = df_csv.columns.to_list()

    col_names = [col.lower().replace(' ', '_').replace('&', 'e') for col in df_columns]
    col_names = [col.lower().replace('(', '').replace(')', '') for col in col_names]
    col_names = [col.lower().replace('-', '_').replace('%', 'perc') for col in col_names]
    col_names = [col.lower().replace('.', '') for col in col_names]
    col_names = [unidecode.unidecode(col) for col in col_names]

    df_csv.columns = col_names

    '''
    Tratamento de valores decimais
    '''

    for col in col_names:
        col_type = df_csv[col].dtype.str
        if col_type == '|O':
            df_csv[col] = df_csv[col].apply(lambda x: x.replace('.', '').replace(',', '.') if isinstance(x, str) else x)

    '''
    Envio da tabela para o Google Big Query
    '''
    credentials_info = create_keyfile_dict_google_big_query_nestle_br()
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    df_csv.to_gbq(
        destination_table=schema + '.' + table_name,  # Dataset.Tablename
        project_id=project_id,  # Project Id extracted from Big Query credentials
        chunksize=None,
        if_exists='replace',  # 'fail', 'replace' or 'append'
        credentials=credentials
    )

    time.sleep(5)

    print("Tabela " + table_name + " criada em " + project_id + "." + schema)



def get_bq_table_from_datalake_gads(
        schema, table_name, account_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ===============================================================
    == CRIAÇÃO DA TABELA analyst.nestle_XXX_gads ==
    ===============================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM(
    SELECT
    adperf.date_id as data
    ,EXTRACT(YEAR FROM adperf.date_id) ano
    ,EXTRACT(MONTH FROM adperf.date_id) mes
    ,CASE 
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) LIKE '%shopping%' THEN 'Shopping'
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) NOT LIKE '%shopping%' THEN 'Search'
        ELSE ''
    END canal
    ,'Mídia' as tipo_origem
    ,cmp.campaign_name as campanha
    ,CASE 
    WHEN lower(cmp.campaign_name) LIKE '%nonbrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%nobrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%brand%' THEN 'Brand' 
    ELSE 'Outros'
    END as campaign_strategy
    ,adg.ad_group_name as grupo_anuncios
    ,ad.headline as headline_anuncio
    ,SUM(ROUND(adperf.cost/1000/1000,2)) as investimento 
    ,SUM(adperf.impressions) as impressoes  
    ,SUM(adperf.clicks) as cliques  
    ,SUM(adperf.interactions) as interacoes
    ,SUM(adperf.conversions ) as conversoes
    ,SUM(adperf.conversion_value) as valor_conversoes
    ,SUM(video_views) as video_starts
    ,SUM(
    (CAST(REPLACE(video_quartile25_rate,'%','')AS FLOAT64)/100) *
	  video_views
    ) as video_watches_at_25perc
    ,SUM(
    (CAST(REPLACE(video_quartile50_rate,'%','')AS FLOAT64)/100) *
	  video_views
    ) as video_watches_at_50perc
    ,SUM(
    (CAST(REPLACE(video_quartile75_rate,'%','')AS FLOAT64)/100) *
	  video_views
    ) as video_watches_at_75perc
    ,SUM(
    (CAST(REPLACE(video_quartile100_rate,'%','')AS FLOAT64)/100) *
	video_views
    ) as video_completions
    
    ,0 as receita
    ,0 as vendas
    ,0 as sessoes
    FROM `nestle-br`.gads.managed_customer cust
    LEFT JOIN `nestle-br`.gads.campaign cmp 
    ON cust.customer_id = cmp.external_customer_id 
    LEFT JOIN `nestle-br`.gads.ad_group adg 
    ON adg.campaign_id = cmp.campaign_id 
    LEFT JOIN `nestle-br`.gads.ad ad 
    ON adg.ad_group_id = ad.ad_group_id 
    LEFT JOIN `nestle-br`.gads.ad_performance adperf 
    ON adperf.ad_id = ad.ad_id
    WHERE cust.customer_id = '''+"'"+account_id+"'"+'''
    GROUP BY adperf.date_id ,
    cmp.campaign_name, 
    adg.ad_group_name,
    ad.headline 
    ) t0
    CROSS JOIN (
    SELECT MAX(adperf.date_id) as ultima_atualizacao
    FROM `nestle-br`.gads.ad_performance adperf) t1
    )

    '''
    
    # query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def get_bq_table_from_datalake_gads2(
        schema, table_name, account_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ===============================================================
    == CRIAÇÃO DA TABELA analyst.nestle_XXX_gads ==
    ===============================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM(
    SELECT 
    adperf.date_id as data
    ,EXTRACT(YEAR FROM adperf.date_id) ano
    ,EXTRACT(MONTH FROM adperf.date_id) mes
    ,CASE 
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) LIKE '%shopping%' THEN 'Shopping'
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) NOT LIKE '%shopping%' THEN 'Search'
        ELSE ''
    END canal
    ,'Mídia' as tipo_origem
    ,cmp.campaign_name as campanha
    ,CASE 
    WHEN lower(cmp.campaign_name) LIKE '%nonbrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%nobrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%brand%' THEN 'Brand' 
    ELSE 'Outros'
    END as campaign_strategy
    ,adg.adgroup_name as grupo_anuncios
    ,ad.ad_name as headline_anuncio
    ,SUM(ROUND(adperf.cost_micros/1000/1000,2)) as investimento 
    ,SUM(adperf.impressions) as impressoes  
    ,SUM(adperf.clicks) as cliques  
    ,SUM(adperf.interactions) as interacoes
    ,SUM(adperf.conversions ) as conversoes
    ,SUM(adperf.conversions_value) as valor_conversoes
    ,SUM(video_views) as video_starts
    ,SUM(video_quartile_p25_rate*video_views) as video_watches_at_25perc
    ,SUM(video_quartile_p50_rate*video_views) as video_watches_at_50perc
    ,SUM(video_quartile_p75_rate*video_views) as video_watches_at_75perc
    ,SUM(video_quartile_p100_rate*video_views) as video_completions
    ,0 as receita
    ,0 as vendas
    ,0 as sessoes
    FROM gads2.customer cust
    LEFT JOIN gads2.campaign cmp 
    ON cust.customer_id = cmp.customer_id
    LEFT JOIN gads2.adgroup adg 
    ON adg.campaign_id = cmp.campaign_id 
    LEFT JOIN gads2.adgroup_ad ad 
    ON adg.adgroup_id = ad.adgroup_id 
    LEFT JOIN gads2.ad_performance adperf 
    ON adperf.ad_id = ad.ad_id
    WHERE CAST(cust.customer_id AS STRING) = "'''+account_id+'''"
    GROUP BY adperf.date_id ,
    cmp.campaign_name, 
    adg.adgroup_name,
    ad.ad_name  
    ) t0
    CROSS JOIN (
    SELECT MAX(adperf.date_id) as ultima_atualizacao
    FROM `nestle-br`.gads2.ad_performance adperf) t1
    )

    '''
    
    # query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''get_bq_table_from_datalake_dv
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')




def create_bq_table_nestle_nhs_avante_dv(
        schema, table_source, table_name
):
    
    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_dv_temp ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    CAST(date AS DATE) as data, 
    campaign as campaign_name, 
    '' as campaign_objective,
    insertion_order AS io_name , line_item as line_item,
    --SPLIT(line_item,'|')[OFFSET(12)] as line_item_custom,
    CASE
    WHEN STRPOS(line_item,'|') > 0
    AND ARRAY_LENGTH(SPLIT(line_item,'|')) - 1 > 12
    THEN SPLIT(line_item,'|')[OFFSET(12)] 
    ELSE line_item
    END as line_item_custom,
    'Youtube' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(revenue,'R$ ','') AS FLOAT64) AS investimento,
    impressions as impressoes,
    clicks as cliques,
    video_plays as video_starts,
    video_1st_quartile_completes_ as video_watches_at_25perc,
    video_mid_points as video_watches_at_50perc,
    video_3rd_quartile_completes as video_watches_at_75perc,
    video_completions
    FROM ''' + schema + '''.''' + table_source + '''
    ) t0
    CROSS JOIN (
    SELECT MAX(CAST(date AS DATE)) ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + '''
    ) t1
    )
    
    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



def get_bq_table_from_datalake_keywords(
        schema, table_name, account_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ===============================================================
    == CRIAÇÃO DA TABELA analyst.nestle_XXX_keyword ==
    ===============================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM(
    SELECT 
    cust.name as account_name
    ,kw.date_id as data
    ,EXTRACT(YEAR FROM kw.date_id) ano
    ,EXTRACT(MONTH FROM kw.date_id) mes
    ,cmp.campaign_name as campanha
    ,CASE 
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) LIKE '%shopping%' THEN 'Shopping'
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) NOT LIKE '%shopping%' THEN 'Search'
        ELSE ''
    END canal
    ,adg.ad_group_name as grupo_anuncios
    ,REPLACE(kw.criteria,'"','') as palavras_chave
    ,CASE 
    WHEN lower(cmp.campaign_name) LIKE '%nonbrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%nobrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%brand%' THEN 'Brand' 
    ELSE 'Outros'
    END as campaign_strategy
    ,SUM(ROUND(kw.cost/1000/1000,2)) as investimento
    ,SUM(kw.impressions) as impressoes
    ,SUM(kw.clicks) as cliques
    FROM `nestle-br`.gads.managed_customer cust
    LEFT JOIN `nestle-br`.gads.campaign cmp 
    ON cust.customer_id = cmp.external_customer_id 
    LEFT JOIN `nestle-br`.gads.ad_group adg 
    ON adg.campaign_id = cmp.campaign_id 
    --LEFT JOIN `nestle-br`.gads.ad ad 
    --ON adg.ad_group_id = ad.ad_group_id 
    LEFT JOIN `nestle-br`.gads.keyword_performance kw 
    ON kw.ad_group_id = adg.ad_group_id
    WHERE cust.customer_id = '''+"'"+account_id+"'"+'''
    GROUP BY 
    cust.name, kw.date_id,
    cmp.campaign_name,
    adg.ad_group_name,
    kw.criteria
    ) t0
    CROSS JOIN (
    SELECT MAX(adperf.date_id) as ultima_atualizacao
    FROM `nestle-br`.gads.ad_performance adperf) t1
    )

    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def get_bq_table_from_datalake_keywords2(
        schema, table_name, account_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ===============================================================
    == CRIAÇÃO DA TABELA analyst.nestle_XXX_keyword ==
    ===============================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM(
    SELECT 
    cust.customer_name as account_name
    ,kw.date_id as data
    ,EXTRACT(YEAR FROM kw.date_id) ano
    ,EXTRACT(MONTH FROM kw.date_id) mes
    ,cmp.campaign_name as campanha
    ,CASE 
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) LIKE '%shopping%' THEN 'Shopping'
        WHEN LENGTH(cmp.campaign_name) > 0 
            AND lower(cmp.campaign_name) NOT LIKE '%shopping%' THEN 'Search'
        ELSE ''
    END canal
    ,adg.adgroup_name as grupo_anuncios
    ,kw_criterion.keyword_text as palavras_chave
    ,kw_criterion.keyword_match_type as match_type
    ,CASE 
    WHEN lower(cmp.campaign_name) LIKE '%nonbrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%nobrand%' THEN 'Non Brand'
    WHEN lower(cmp.campaign_name) LIKE '%brand%' THEN 'Brand' 
    ELSE 'Outros'
    END as campaign_strategy
    ,SUM(ROUND(kw.cost_micros/1000/1000,2)) as investimento
    ,SUM(kw.impressions) as impressoes
    ,SUM(kw.clicks) as cliques
    FROM gads2.customer cust
    LEFT JOIN gads2.campaign cmp 
    ON cust.customer_id = cmp.customer_id
    LEFT JOIN gads2.adgroup adg 
    ON adg.campaign_id = cmp.campaign_id 
    --LEFT JOIN gads2.adgroup_ad ad 
    --ON adg.adgroup_id = ad.adgroup_id 
    LEFT JOIN gads2.keyword_performance kw 
    ON kw.adgroup_id = adg.adgroup_id
    LEFT JOIN gads2.adgroup_criterion kw_criterion
    ON kw.criterion_id = kw_criterion.criterion_id
    AND kw_criterion.adgroup_id = adg.adgroup_id
    WHERE CAST(cust.customer_id AS STRING) = "'''+account_id+'''"
    GROUP BY 
    cust.customer_name
    ,kw.date_id
    ,cmp.campaign_name
    ,adg.adgroup_name
    ,kw_criterion.keyword_text
    ,kw_criterion.keyword_match_type
    ) t0
    CROSS JOIN (
    SELECT MAX(adperf.date_id) as ultima_atualizacao
    FROM `nestle-br`.gads2.ad_performance adperf) t1
    )

    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')




def get_bq_table_from_datalake_fb(
        schema, table_name, account_id):


    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXXX_fb ====
    ================================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    acc.name as conta
    ,ins.date_start as data
    ,EXTRACT(YEAR FROM date_start) ano
    ,EXTRACT(MONTH FROM date_start) mes
    ,'Facebook' as canal
    ,aset.name as adset_name
    ,cmp.name as campaign_name
    ,CASE
    WHEN STRPOS(cmp.name,'|') > 0
    AND ARRAY_LENGTH(SPLIT(cmp.name,'|')) - 1 > 1
    THEN SPLIT(cmp.name,'|')[OFFSET(1)] 
    ELSE cmp.name
    END as campaign_name_custom
    ,CASE
    WHEN STRPOS(cmp.name,'|') > 0
    AND ARRAY_LENGTH(SPLIT(cmp.name,'|')) - 1 > 3
    THEN SPLIT(cmp.name,'|')[OFFSET(3)] 
    ELSE cmp.name
    END as campaign_pilar
    ,CASE
    WHEN STRPOS(aset.name,'|') > 0
    AND ARRAY_LENGTH(SPLIT(cmp.name,'|')) - 1 > 15
    THEN SPLIT(aset.name,'|')[OFFSET(15)] 
    ELSE aset.name
    END as adset_format
    ,ad.name as ad_name
    ,cr.name as creative_name
    ,ins.objective as campaign_objective
    ,ins.publisher_platform as plataforma
    ,ins.spend as investimento
    ,ins.impressions as impressoes
    ,ins.reach as alcance
    --,ins.clicks as cliques
    ,ins.inline_link_clicks as cliques
    ,ins.frequency as frequencia
    --,ins.actn_post_engagement 
    --,ins.inline_post_engagement 
    --,ins.vc2s_video_view as two_second_video_views
    ,ins.actn_video_view as three_second_video_views
    ,ins.vp25_video_view as video_watches_at_25perc
    ,ins.vp50_video_view as video_watches_at_50perc
    ,ins.vp75_video_view as video_watches_at_75perc
    ,ins.v100_video_view as video_watches_at_100perc
    ,cr.thumbnail_url as ad_creative_thumbnail
    --,CURRENT_TIMESTAMP() as ultima_atualizacao
    FROM `nestle-br`.facebook.account acc
    LEFT JOIN `nestle-br`.facebook.campaign cmp 
    ON acc.account_id = cmp.account_id 
    LEFT JOIN `nestle-br`.facebook.adset aset 
    ON aset.campaign_id  = cmp.id 
    LEFT JOIN `nestle-br`.facebook.ad ad 
    ON aset.id  = ad.adset_id 
    LEFT JOIN `nestle-br`.facebook.insight ins 
    ON ins.ad_id  = ad.id 
    LEFT JOIN `nestle-br`.facebook.creative cr 
    ON cr.id  = ad.creative_id 
    WHERE acc.account_id =  '''+"'"+account_id+"'"+'''
    ) t0
    CROSS JOIN (
    SELECT MAX(ins.date_start) as ultima_atualizacao
    FROM `nestle-br`.facebook.insight ins) t1
    )
    

    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_from_query(
        dataset, table_name, query):


    '''
    ================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXXX ====
    ================================================================
    '''

    inicio = datetime.now()

    create_or_replace_query = '''

    CREATE OR REPLACE TABLE 
    ''' + dataset + '''.''' + table_name + ''' AS 
    (
    ''' +query+'''
    ) 

    '''

    print('Criando tabela: '+dataset+'.'+table_name)
    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    query_job = client.query(create_or_replace_query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)
    fim = datetime.now()

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    Tempo de Execução: '''+show_exec_time(inicio, fim)+'''
    ''')


def show_exec_time(inicio, fim):
    tempo = fim - inicio
    tempo_string = str(divmod(tempo.days * 86400 + tempo.seconds, 60)[0]) \
                   + " minutos e " + \
                   str(divmod(tempo.days * 86400 + tempo.seconds, 60)[1]) \
                   + " segundos "
    return tempo_string


def get_bq_table_from_datalake_dv(
        schema, table_name, advertiser_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXXX_dv ====
    ================================================================
    '''


    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    cmmet.date_id as data 
    ,EXTRACT(YEAR FROM date_id) ano
    ,EXTRACT(MONTH FROM date_id) mes
    ,'Youtube' as canal
    ,cmp.display_name as campaign_name
    ,cmp.cpngol_campaign_goal_type as campaign_objective
    ,dvins.display_name as insertion_name
    ,ARRAY_REVERSE(SPLIT(dvins.display_name,'|'))[SAFE_OFFSET(0)] as insertion_name_custom
    ,line_item_type
    ,dbm_cost as investimento
    ,impressions as impressoes
    ,active_view_viewable_impressions as viewable_impressions
    ,clicks as cliques
    ,rich_media_video_plays as video_starts
    ,rich_media_video_first_quartile_completes as video_watches_at_25perc
    ,rich_media_video_midpoints as video_watches_at_50perc
    ,rich_media_video_third_quartile_completes as video_watches_at_75perc
    ,rich_media_video_completions as video_completions
    ,dvcr.display_name creative_name
    --,SPLIT(dvcr.display_name,'|')[OFFSET(18)] creative_format
    FROM `nestle-br`.gmkt.dv_advertiser dvadv
    LEFT JOIN `nestle-br`.gmkt.dv_campaign cmp
    ON cmp.advertiser_id = dvadv.advertiser_id 
    LEFT JOIN `nestle-br`.gmkt.dv_insertion_order dvins
    ON cmp.campaign_id = dvins.campaign_id 
    --LEFT JOIN `nestle-br`.gmkt.dv_line_item dvline
    --ON dvline.campaign_id = dvins.campaign_id 
    LEFT JOIN `nestle-br`.gmkt.cm_standard_metrics cmmet
    ON cmmet.dbm_advertiser_id = dvadv.advertiser_id 
    AND cmmet.dbm_campaign_id = cmp.campaign_id 
    AND cmmet.dbm_insertion_order_id = dvins.insertion_order_id 
    LEFT JOIN `nestle-br`.gmkt.dv_creative dvcr
    ON dvcr.creative_id = cmmet.dbm_creative_id 
    LEFT JOIN `nestle-br`.gmkt.dv_line_item dvline
    ON dvline.line_item_id = cmmet.dbm_line_item_id 
    WHERE dvadv.advertiser_id IN ('''+"'"+"','".join(advertiser_id)+"'"+''')
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(cmmet.date_id) AS DATE) as ultima_atualizacao
    FROM `nestle-br`.gmkt.cm_standard_metrics cmmet) t1
    )

    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def get_bq_table_from_datalake_dv2(
        schema, table_name, advertiser_id):



    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXXX_dv ====
    ================================================================
    '''


    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    
    SELECT * FROM (
    SELECT 
    dbm_rep.date_id as data 
    ,EXTRACT(YEAR FROM dbm_rep.date_id) ano
    ,EXTRACT(MONTH FROM dbm_rep.date_id) mes
    ,'Youtube' as canal
    ,dvadv.display_name advertiser_name
    ,cmp.display_name as campaign_name
    ,cmp.cpngol_campaign_goal_type as campaign_objective
    ,dvins.display_name as io_name
    ,ARRAY_REVERSE(SPLIT(dvins.display_name,'|'))[SAFE_OFFSET(0)] as io_custom
    ,dvline.line_item_type	
    ,dvline.display_name as line_item
    ,ARRAY_REVERSE(SPLIT(dvline.display_name,'|'))[SAFE_OFFSET(0)] as line_item_custom
    --,dvline.*
    --,dvlinecr.*
    ,dvcr.display_name as creative_name
    --,SPLIT(dvcr.display_name,'|')[OFFSET(20)] as placement
    ,dvcr.cm_placement_id as placement_id
    ,ARRAY_REVERSE(SPLIT(dvcr.display_name,'|'))[SAFE_OFFSET(0)] as creative_name_custom
    --,dbm_rep.*
    ,investimento
    ,impressoes
    --,active_view_viewable_impressions as viewable_impressions
    ,cliques
    ,video_starts
    ,video_watches_at_25perc
    ,video_watches_at_50perc
    ,video_watches_at_75perc
    ,video_completions
    FROM (
    SELECT 
    CAST(advertiser_id AS STRING) advertiser_id, 
    CAST(REPLACE(date_id,'/','-')AS DATE) as date_id, insertion_order_id , 
    creative_id , 
    line_item_id , campaign_id 
    ,SUM(CAST(client_cost_advertiser_currency AS FLOAT64)) as investimento
    ,SUM(CAST(impressions AS INT64)) as impressoes
    ,SUM(CAST(clicks AS INT64)) as cliques
    ,SUM(CAST(rich_media_video_plays AS INT64)) as video_starts
    ,SUM(CAST(rich_media_video_first_quartile_completes AS INT64)) as video_watches_at_25perc
    ,SUM(CAST(rich_media_video_midpoints AS INT64)) as video_watches_at_50perc
    ,SUM(CAST(rich_media_video_third_quartile_completes AS INT64)) as video_watches_at_75perc
    ,SUM(CAST(rich_media_video_completions AS INT64)) as video_completions
    FROM gmkt.dbm_general_report 
    WHERE CAST(advertiser_id AS STRING) IN ('''+"'"+"','".join(advertiser_id)+"'"+''')
    GROUP BY 
    partner_id, advertiser_id, 
    date_id, insertion_order_id ,
    creative_id , line_item_id , campaign_id 
    ) dbm_rep
    LEFT JOIN gmkt.dv_advertiser dvadv
    ON dbm_rep.advertiser_id = dvadv.advertiser_id 
    LEFT JOIN gmkt.dv_campaign cmp
    ON dbm_rep.campaign_id = cmp.campaign_id 
    LEFT JOIN gmkt.dv_insertion_order dvins
    ON dbm_rep.insertion_order_id = dvins.insertion_order_id
    LEFT JOIN gmkt.dv_line_item dvline
    ON dbm_rep.line_item_id = dvline.line_item_id
    --LEFT JOIN gmkt.dv_line_item_creative dvlinecr
    --ON dvline.line_item_id = dvlinecr.line_item_id
    --LEFT JOIN gmkt.dv_creative dvcr
    --ON dvcr.creative_id = dvlinecr.creative_id AND dvcr.creative_id = dbm_rep.creative_id
    LEFT JOIN gmkt.dv_creative dvcr
    ON dbm_rep.creative_id = dvcr.creative_id 
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(CAST(REPLACE(date_id,'/','-')AS DATE)) AS DATE) as ultima_atualizacao
    FROM gmkt.dbm_general_report) t1
    )

    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



def create_bq_table_nestle_nhs_avante_metas(
        schema, table_source, table_name
):
    

    '''
    ============================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_avante_metas ====
    ============================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT 
    ano,
    mes,
    veiculo,
    CAST(investimento AS FLOAT64) as investimento
    FROM ''' + schema + '''.''' + table_source + '''

    )
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nav_criteo_temp(
    schema, table_source, table_name
):

    

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_criteo_temp ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
        SELECT * FROM (
    SELECT ano, mes, data, campaign_name, canal, tipo_origem,
    CAST(
    investimento_numeral||'.'||
    investimento_decimal AS FLOAT64) as investimento,
    impressoes,
    cliques,
    receita,
    vendas,
    sessoes
    FROM (
    SELECT *,
    CASE
    WHEN SUBSTR(investimento,-3,1) = '.'  
    THEN REPLACE(SUBSTR(investimento,1, LENGTH(investimento) -3),'.','')
    WHEN SUBSTR(investimento,-2,1) = '.'  
    THEN REPLACE(SUBSTR(investimento,1, LENGTH(investimento) -2),'.','')
    END as investimento_numeral,
    CASE
    WHEN SUBSTR(investimento,-3,1) = '.'  
    THEN REPLACE(SUBSTR(investimento,LENGTH(investimento)-2 ),'.','')
    WHEN SUBSTR(investimento,-2,1) = '.'  
    THEN REPLACE(SUBSTR(investimento,LENGTH(investimento)-1 ),'.','')
    END as investimento_decimal
    FROM (
    SELECT 
    CAST(SUBSTR(data,7,4) AS INT64) as ano,
    CAST(SUBSTR(data,4,2) AS INT64) as mes,
    SUBSTR(data,7,4)||"-"||SUBSTR(data,4,2)||"-"||SUBSTR(data,1,2) as data, 
    'Criteo' as campaign_name,
    'Criteo' as canal,
    'Mídia' tipo_origem,
    REPLACE(REPLACE(investimento,'R$ ',''),'R$','') as investimento,
    impressoes,
    cliques,
    0 as receita,
    0 as vendas,
    0 as sessoes
    FROM '''+schema+'''.'''+table_source+''' 	
    ) t0
    ) t1
    ) t_0
    CROSS JOIN (
    SELECT 
    CAST(MAX(SUBSTR(data,7,4)||"-"||SUBSTR(data,4,2)||"-"||SUBSTR(data,1,2)) AS DATE) as ultima_atualizacao_temp
    FROM '''+schema+'''.'''+table_source+''' ) t_1
   

    )

    
    '''

    
    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT *
    EXCEPT (date),
    date as data
    FROM (
    SELECT 
    CAST(SUBSTR(data,1,4) AS INT64) as ano,
    CAST(SUBSTR(data,6,2) AS INT64) as mes,
    CAST(data AS DATE) as date,
    'Criteo' as campaign_name,
    'Criteo' as canal,
    'Mídia' tipo_origem,
    investimento,
    impressoes,
    cliques,
    0 as receita,
    0 as vendas,
    0 as sessoes
    FROM '''+schema+'''.'''+table_source+'''
    ) t_0
    CROSS JOIN (
    SELECT 
    MAX(CAST(data AS DATE)) as ultima_atualizacao_temp
    FROM '''+schema+'''.'''+table_source+''' ) t_1  
    )
    '''





    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nhs_nutren_protein_search_temp(schema, table_name):
    # credentials_file = "bqcredentials.json"
    # log = logger("bigquery_loader.log")
    # bq = BigQuery(credentials_file, log)



    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_protein_search_temp ====
    ========================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    date as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    'Search' as canal,
    campaign_name as campanha,
    ad_group_name as grupo_anuncios,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    clicks as cliques,
    cpc as cpc
    FROM `analyst.nestle_nhs_nutren_protein_search_stg`
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM `analyst.nestle_nhs_nutren_protein_search_stg`
    )t1
    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



def create_bq_table_nestle_nhs_avante_gads(schema, table_name):
    # credentials_file = "bqcredentials.json"
    # log = logger("bigquery_loader.log")
    # bq = BigQuery(credentials_file, log)



    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_protein_search_temp ====
    ========================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    date as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    'Search' as canal,
    campaign_name as campanha,
    '' as grupo_anuncios,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    clicks as cliques,
    cpc as cpc
    FROM `analyst.nestle_nhs_avante_gads_stg`
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM `analyst.nestle_nhs_avante_gads_stg`
    )t1
    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nhs_nutren_protein_fb(schema, table_name):



    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_protein_search_temp ====
    ========================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    'Facebook' as canal,
    campaign_name as campanha,
    CASE 
    WHEN campaign_name LIKE '%BL_HUMANO%' THEN 'Humano'
    WHEN campaign_name LIKE '%BL_RAPOSA%' THEN 'Raposa'
    WHEN campaign_name LIKE '%NUTRENPROTEIN_SATISFYING%' THEN 'Satisfying'
    WHEN campaign_name LIKE '%STORIES%' THEN 'Stories'
    WHEN campaign_name LIKE '%Alok%' THEN 'Oportunidade Alok'
    WHEN campaign_name LIKE '%ONGS%' THEN 'Micro - ONGs'
    WHEN campaign_name LIKE '%PRODUTO%' THEN 'Nutren Protein Produtos'
    WHEN campaign_name LIKE '%NESTLE%CONTENT%' THEN 'Nutren Protein Content'
    WHEN campaign_name LIKE '%NAMORADOS%' THEN 'Dia dos Namorados'
    WHEN campaign_name LIKE '%OFERTACO%' THEN 'Ofertaço'
    WHEN campaign_name LIKE '%ZUMBA%' THEN 'Micro - Zumba'
    WHEN campaign_name LIKE '%CHEGOU_NUTREN_PROTEIN%' THEN 'Personagens'
    ELSE 'Não Identificado'
    END campaign_name,
    campaign_objective,
    publisher_platform as plataforma,
    placement,
    ad_set_name as adset_name,
    ad_creative_thumbnail_url as ad_creative_thumbnail,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    reach as alcance,
    link_clicks as cliques,
    CAST(REPLACE(ctr_all,',','.') AS FLOAT64) ctr_all, 
    CAST(REPLACE(cpc_all,',','.') AS FLOAT64) cpc_all, 
    cpm_cost_per_1000_impressions, 
    three_second_video_views, 
    video_watches_at_25perc,
    video_watches_at_50perc,
    video_watches_at_75perc,
    video_watches_at_100perc, 
    cost_per_three_second_video_view,
    CAST(frequency AS FLOAT64) as frequencia
    FROM `analyst.nestle_nhs_nutren_protein_fb_stg`
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM `analyst.nestle_nhs_nutren_protein_fb_stg`
    )t1
    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')




def create_bq_table_nestle_nhs_senior_compiled_midias(
    schema, source_table_1, source_table_2, source_table_3,
    table_name):
    
    

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_senior_compiled_midias ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT 
    *  
    FROM (
        SELECT 
        CAST(data as DATE) as date, 
        ano, mes, canal, 
        campanha,
        '' as objetivo_campanha,
        '' as plataforma,
        grupo_anuncios,
        investimento, 
        impressoes, 
        0 as alcance,
        cliques,
        0 as frequencia,
        0 as three_second_video_views,
        0 as video_watches_at_100perc,
        NULL as ad_creative_thumbnail,
        ultima_atualizacao
        FROM ''' + schema + '''.''' + source_table_1 + '''
        UNION ALL
        SELECT 
        data as date,ano,mes,canal,
        campaign_name as campanha,
        campaign_objective as objetivo_campanha,
        plataforma,
        adset_name as grupo_anuncios,
        investimento, 
        impressoes, 
        alcance, 
        cliques,
        frequencia,
        three_second_video_views,
        video_watches_at_100perc,
        ad_creative_thumbnail,
        ultima_atualizacao
        FROM ''' + schema + '''.''' + source_table_2 + '''
        UNION ALL
        SELECT 
        data as date,ano,mes,canal,
        campaign_name as campanha,
        NULL as objetivo_campanha,
        NULL AS plataforma,
        insertion_name as grupo_anuncios,
        investimento, 
        impressoes, 
        NULL AS alcance, 
        cliques,
        NULL AS frequencia,
        video_starts as three_second_video_views,
        video_completions as video_watches_at_100perc,
        NULL AS ad_creative_thumbnail,
        ultima_atualizacao
        FROM ''' + schema + '''.''' + source_table_3 + '''
    ) t

    )


    '''


    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



def create_bq_table_nestle_metas_investimento(
    schema, table_source, table_name, plan_cliente
):

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ==================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXX_metas ====
    ==================================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT 
    "'''+plan_cliente+'''" as cliente,
    '' as mes_nome,
    mes,
    ano,
    veiculo as midia,
    CAST(investimento AS FLOAT64) as investimento
    --CAST(roas AS FLOAT64) as roas,
    --CAST(investimento AS FLOAT64) * CAST(roas AS FLOAT64) as receita
    FROM '''+schema+'''.'''+table_source+'''

    )
    '''


    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nhs_avante_linkedin(
        schema, table_source, table_name
):
    
    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_avante_linkedin_stg ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(SPLIT(start_date_in_utc,'/')[OFFSET(2)] AS INT64) as ano,
    CAST(SPLIT(start_date_in_utc,'/')[OFFSET(1)] AS INT64) as mes,
    CAST(
    SPLIT(start_date_in_utc,'/')[OFFSET(2)] || "-" || 
    SPLIT(start_date_in_utc,'/')[OFFSET(1)] || "-" ||
    SPLIT(start_date_in_utc,'/')[OFFSET(0)]
    AS DATE)as data,
    campaign_name,
    campaign_status,
    'LinkedIn' as canal,
    creative_name,
    ad_headline,
    video_views,
    video_views_at_25perc,
    video_views_at_50perc,
    video_views_at_75perc,
    video_completions,
    CAST(REPLACE(total_spent,'R$ ','') AS FLOAT64) AS investimento,
    impressions as impressoes,
    clicks as cliques,
    conversions as conversoes,
    reach as alcance
    --CURRENT_TIMESTAMP() as ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + '''
    ) t0
    CROSS JOIN (
    SELECT MAX(CAST(
    SPLIT(start_date_in_utc,'/')[OFFSET(2)] || "-" || 
    SPLIT(start_date_in_utc,'/')[OFFSET(1)] || "-" ||
    SPLIT(start_date_in_utc,'/')[OFFSET(0)]
    AS DATE)) data_max
    FROM ''' + schema + '''.''' + table_source + '''
    )
    )
    '''

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def get_bq_table_from_criteo_api(
    CLIENT_ID, CLIENT_SECRET,
    start_date, dataset, table_name):
  

  GRANT_TYPE = 'client_credentials'

  configuration = Configuration(username=CLIENT_ID, password=CLIENT_SECRET)

  client = cm.ApiClient(configuration)

  # Get a valid token. The configuration is accessible through the client
  auth_api = cm.AuthenticationApi(client)
  auth_response = auth_api.o_auth2_token_post(client_id=client.configuration.username,
                                              client_secret=client.configuration.password,
                                              grant_type=GRANT_TYPE)

  # Token type is always "BEARER"
  token = auth_response.token_type + " " + auth_response.access_token

  api_instance = cm.StatisticsApi(client)
  authorization = 'Bearer VALID_JWT_TOKEN_BASE64' # str | JWT Bearer Token (default to 'Bearer VALID_JWT_TOKEN_BASE64')
  report_query = cm.CampaignReportQueryMessage() # CampaignReportQueryMessage | 

  stats_api = cm.StatisticsApi(client)
  from datetime import datetime
  today = datetime.today().strftime("%Y-%m-%d")


  stats_query = cm.StatsQueryMessageEx(
          report_type="CampaignPerformance",
          dimensions=['Day'],
          metrics=['AdvertiserCost',
                  'Displays',
                  'Clicks'
          ],
          currency='BRL',
          start_date=start_date,
          end_date=today,
          timezone='America/Sao Paulo',
          format="JSON")


  api_response = stats_api.get_stats(authorization, stats_query)
  stats_dict = json.loads(api_response.replace('\ufeff',''))
  df_criteo = pd.DataFrame.from_dict(stats_dict['Rows'])
  df_criteo['Cost'] = df_criteo['Cost'].astype(float).round(2)
  df_criteo.head(100)
  df_criteo.columns = ['advertiser_name','day','currency',
                      'cost','impressions','clicks']

  credentials_info = create_keyfile_dict_google_big_query_nestle_br()
  credentials = service_account.Credentials.from_service_account_info(credentials_info)


  df_criteo.to_gbq(
      destination_table=dataset+'.'+table_name+'_stg',  # Dataset.Tablename
      project_id="nestle-br",  # Project Id extracted from Big Query credentials
      chunksize=None,
      if_exists='replace',  # 'fail', 'replace' or 'append'
      credentials=credentials
  )



  create_bq_table_from_query(
  dataset=dataset, 
  table_name =table_name,
  query = '''
  SELECT * FROM(
  SELECT * FROM (
  SELECT 
  CAST(
  LPAD(ano,4,'0')||"-"||
  LPAD(CAST(mes AS STRING),2,'0') ||"-"||
  LPAD(CAST(dia AS STRING),2,'0')
  AS DATE) as data,
  CAST(ano as INT64) as ano,
  CAST(mes as INT64) as mes,
  'Criteo' as campaign_name,
  'Criteo' as canal,
  'Mídia' as tipo_origem,
  investimento,
  impressoes,
  cliques,
  0 as receita,
  0 as vendas,
  0 as sessoes
  FROM (
  SELECT
  SPLIT(SPLIT(day,'/')[OFFSET(0)],' ')[OFFSET(1)] as mes
  ,SPLIT(day,'/')[OFFSET(1)] as dia
  ,SPLIT(day,'/')[OFFSET(2)] as ano
  ,CAST(cost AS FLOAT64) as investimento
  ,CAST(impressions AS INT64) as impressoes
  ,CAST(clicks AS INT64) as cliques
  FROM '''+dataset+'''.'''+table_name+'''_stg
  ) t0
  ) t00
  CROSS JOIN (
  SELECT MAX(
  CAST(
  LPAD(SPLIT(day,'/')[OFFSET(2)],4,'0')||"-"||
  LPAD(CAST(SPLIT(SPLIT(day,'/')[OFFSET(0)],' ')[OFFSET(1)] AS STRING),2,'0') ||"-"||
  LPAD(CAST(SPLIT(day,'/')[OFFSET(1)] AS STRING),2,'0')
  AS DATE)) as ultima_atualizacao_temp
  FROM '''+dataset+'''.'''+table_name+'''_stg) t1 
  )
  ''')


def create_bq_table_nestle_nhs_avante_compiled_midias(
    schema,
    table_source1,
    table_source2,
    table_source3,
    table_source4,
    table_name
):

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_compiled_midias ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT 
    *  
    FROM (
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    video_starts as video_starts,
    video_completions as video_completions,
    ultima_atualizacao
    FROM '''+schema+'''.'''+table_source1+''' 
    UNION ALL
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    three_second_video_views as video_starts,
    video_watches_at_100perc as video_completions,
    ultima_atualizacao
    FROM '''+schema+'''.'''+table_source2+'''
    UNION ALL
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    video_starts as video_starts,
    video_completions as video_completions,
    data_max as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source3+'''
    UNION ALL
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    video_views as video_starts,
    video_completions as video_completions,
    data_max as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source4+'''
        
    ) t

    )


    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id 
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nav_dv_temp(
    schema, table_source, table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_dv_temp ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
     campaign as campaign_name, 
     '' as campaign_objective,
     insertion_order as io_name, 
     'Display' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(revenue,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    clicks as cliques,
    0 as video_starts ,
    0 as video_completions ,
    0 as receita,
    0 as vendas,
    0 as sessoes
    FROM '''+schema+'''.'''+table_source+'''
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+''') t1
    )
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id 
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def google_drive_excel_to_gbq(
    project_id,
    dataset,
    table_name,
    google_drive,
    drive_folder_path,
    sheet_name,
    df_columns):

  # Deleção da tabela temp
  query = '''
    DROP TABLE IF EXISTS ''' + dataset + '''.''' + table_name + '''
    '''
  
  client = connect_google_big_query()
  job_config = bigquery.QueryJobConfig()
  job_config.priority = bigquery.QueryPriority.INTERACTIVE

  query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
  time.sleep(5)
  results = query_job.result()
  print(results)


  # Leitura dos arquivos
  import os
  drive.mount(google_drive, force_remount=False)
  df_gdrive = pd.read_excel(os.path.join(google_drive,drive_folder_path),
                      sheet_name=sheet_name)
  for col in df_columns:
      if col not in df_gdrive.columns:
          df_gdrive[col] = ''
  df_gdrive = df_gdrive[df_columns]

  col_names = [col.lower().replace(' ', '_').replace('&', 'e') for col in df_columns]
  col_names = [col.lower().replace('(', '').replace(')', '') for col in col_names]
  col_names = [col.lower().replace('-', '_').replace('%', 'perc') for col in col_names]
  col_names = [unidecode.unidecode(col) for col in col_names]

  df_gdrive.columns = col_names
  print(df_gdrive.head())
  credentials_info = create_keyfile_dict_google_big_query_nestle_br()
  credentials = service_account.Credentials.from_service_account_info(credentials_info)
  df_gdrive.to_gbq(
      destination_table=dataset + '.' + table_name,  # Dataset.Tablename
      project_id=project_id,  # Project Id extracted from Big Query credentials
      chunksize=None,
      if_exists='append',  # 'fail', 'replace' or 'append',
      credentials=credentials
  )


def google_drive_excel_mounted_to_gbq(
    filepath, sheetname,
    df_columns, project_id,
    schema, table_name
    ):

  client = connect_google_big_query()
  job_config = bigquery.QueryJobConfig()
  job_config.priority = bigquery.QueryPriority.INTERACTIVE

  '''
  Deleção da tabela temp
  '''

  query = '''
    DROP TABLE ''' + schema + '''.''' + table_name + '''
  '''

  query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
  time.sleep(5)
  results = query_job.result()
  print(results)

  state = query_job.state
  errors = query_job.errors
  created = query_job.created
  destination = query_job.destination
  project = destination.project
  dataset_id = destination.dataset_id
  table_id = destination.table_id
  print('''
  Status: '''+state+'''
  Erros: '''+str(errors)+'''
  Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
  Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
  ''')

  credentials_info = create_keyfile_dict_google_big_query_nestle_br()
  credentials = service_account.Credentials.from_service_account_info(credentials_info)


  all_files = glob(filepath + "/*.xlsx")
  for file in all_files:
    print(file)
    df_gdrive = pd.read_excel(file,sheet_name=sheetname)
    for col in df_columns:
        if col not in df_gdrive.columns:
            df_gdrive[col] = ''

    print(df_gdrive.columns)
    df_gdrive = df_gdrive[df_columns]
    col_names = [col.lower().replace(' ', '_').replace('&', 'e') for col in df_columns]
    col_names = [col.lower().replace('(', '').replace(')', '') for col in col_names]
    col_names = [col.lower().replace('-', '_').replace('%', 'perc') for col in col_names]
    col_names = [unidecode.unidecode(col) for col in col_names]

    df_gdrive.columns = col_names
    print(df_gdrive.head())
    df_gdrive.to_gbq(
      destination_table=schema + '.' + table_name,  # Dataset.Tablename
      project_id=project_id,  # Project Id extracted from Big Query credentials
      chunksize=None,
      if_exists='replace',  # 'fail', 'replace' or 'append'
      credentials=credentials
    )


def create_bq_table_nestle_nhs_avante_cursos(
        schema, table_name):


    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_avante_cursos ====
    ========================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (

    SELECT
    EXTRACT(YEAR FROM data) ano,
    EXTRACT(YEAR FROM data) mes,
    data,
    codigo, contador, nome, email, tipousuario,
    formacao, especialidade, cursoid, curso,
    data_cadastro_curso, aulaid, aula,
    percentual, videoid, status,
    qdteaulas, qdteaulasiniciadas,
    qdteaulasconcluidas,
    qdteaulasiniciadas - qdteaulasconcluidas as qtdeaulasnaoconcluidas
    FROM analyst.nestle_nhs_avante_cursos_stg

    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')




def create_bq_table_nestle_nhs_nutren_senior_overview_investimento(
        plan_cliente, schema, table_metas, table_compiled, table_name
):
    
    

    '''
    ====================================================================
    ==== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_senior_overview ===
    ====================================================================
    '''

    # query = '''
    #     CREATE OR REPLACE TABLE 
    # '''+schema+'''.'''+table_name+''' AS 
    # (

    # SELECT 
    # ano, mes, canal, 
    # COALESCE(investimento_realizado,0) investimento_realizado,
    # --COALESCE(receita_realizada,0) receita_realizada,
    # COALESCE(investimento_plan,0) investimento_plan,
    # --COALESCE(roas_plan,0) roas_plan,
    # --COALESCE(receita_plan,0) receita_plan
    # FROM (
    #     SELECT 
    #     plan.ano,
    #     plan.mes,
    #     plan.veiculo as canal,
    #     realizado.investimento_realizado,
    #     --realizado.receita_realizada,
    #     plan.investimento as investimento_plan,
    #     --plan.roas as roas_plan,
    #     --plan.receita as receita_plan
    #     FROM ( 
    #         SELECT *
    #         FROM '''+schema+'''.'''+table_metas+''' 
    #     ) plan
    #     LEFT JOIN ( 
    #         SELECT 
    #         ano,mes,canal,
    #         SUM(investimento) investimento_realizado,
    #         --SUM(receita) receita_realizada
    #         FROM '''+schema+'''.'''+table_compiled+'''
    #         GROUP BY ano,mes,canal
    #         ORDER BY SUM(investimento) DESC
    #     ) realizado
    #     ON plan.ano = realizado.ano
    #     AND plan.mes = realizado.mes
    #     AND plan.veiculo = realizado.canal
    # )t1 WHERE investimento_plan IS NOT NULL
    # )
    # '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (

    SELECT 
    ano, mes, canal, 
    COALESCE(investimento_realizado,0) investimento_realizado,
    --COALESCE(receita_realizada,0) receita_realizada,
    COALESCE(investimento_plan,0) investimento_plan,
    --COALESCE(roas_plan,0) roas_plan,
    --COALESCE(receita_plan,0) receita_plan
    FROM (
        SELECT 
        plan.cliente,
        plan.ano,
        plan.mes,
        plan.midia as canal,
        realizado.investimento_realizado,
        --realizado.receita_realizada,
        plan.investimento as investimento_plan,
        --plan.roas as roas_plan,
        --plan.receita as receita_plan
        FROM ( 
            SELECT *
            FROM '''+schema+'''.'''+table_metas+''' 
        ) plan
        LEFT JOIN ( 
            SELECT 
            ano,mes,
            CASE 
            WHEN canal = 'Youtube' THEN 'DV360'
            WHEN canal = 'Search' THEN 'Google Ads'
            ELSE canal 
            END canal,
            SUM(investimento) investimento_realizado,
            --SUM(receita) receita_realizada
            FROM '''+schema+'''.'''+table_compiled+'''
            GROUP BY ano,mes,canal
            ORDER BY SUM(investimento) DESC
        ) realizado
        ON plan.ano = realizado.ano
        AND plan.mes = realizado.mes
        AND plan.midia = realizado.canal
        WHERE plan.cliente = "'''+plan_cliente+'''"
    )t1 WHERE investimento_plan IS NOT NULL

    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_overview_investimento(
        plan_cliente, schema, table_metas, table_compiled, table_name
):
    
    

    '''
    ====================================================================
    ==== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_senior_overview ===
    ====================================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (

    SELECT 
    ano, mes, canal, 
    COALESCE(investimento_realizado,0) investimento_realizado,
    --COALESCE(receita_realizada,0) receita_realizada,
    COALESCE(investimento_plan,0) investimento_plan,
    --COALESCE(roas_plan,0) roas_plan,
    --COALESCE(receita_plan,0) receita_plan
    FROM (
        SELECT 
        plan.cliente,
        plan.ano,
        plan.mes,
        plan.midia as canal,
        realizado.investimento_realizado,
        --realizado.receita_realizada,
        plan.investimento as investimento_plan,
        --plan.roas as roas_plan,
        --plan.receita as receita_plan
        FROM ( 
            SELECT *
            FROM '''+schema+'''.'''+table_metas+''' 
        ) plan
        LEFT JOIN ( 
            SELECT 
            ano,mes,
            CASE 
            WHEN canal = 'Youtube' THEN 'DV360'
            WHEN canal = 'Search' THEN 'Google Ads'
            WHEN canal = 'LinkedIn' THEN 'Linkedin'
            ELSE canal 
            END canal,
            SUM(investimento) investimento_realizado,
            --SUM(receita) receita_realizada
            FROM '''+schema+'''.'''+table_compiled+'''
            GROUP BY ano,mes,canal
            ORDER BY SUM(investimento) DESC
        ) realizado
        ON plan.ano = realizado.ano
        AND plan.mes = realizado.mes
        AND plan.midia = realizado.canal
        WHERE plan.cliente = "'''+plan_cliente+'''"
    )t1 WHERE investimento_plan IS NOT NULL

    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



# def create_bq_table_nestle_overview_investimento(
#         schema, table_metas, table_compiled, table_name
# ):
    
    

#     '''
#     ====================================================================
#     ==== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_senior_overview ===
#     ====================================================================
#     '''

#     query = '''
#         CREATE OR REPLACE TABLE 
#     '''+schema+'''.'''+table_name+''' AS 
#     (

#     SELECT 
#     ano, mes, canal, 
#     COALESCE(investimento_realizado,0) investimento_realizado,
#     --COALESCE(receita_realizada,0) receita_realizada,
#     COALESCE(investimento_plan,0) investimento_plan,
#     --COALESCE(roas_plan,0) roas_plan,
#     --COALESCE(receita_plan,0) receita_plan
#     FROM (
#         SELECT 
#         plan.ano,
#         plan.mes,
#         plan.veiculo as canal,
#         realizado.investimento_realizado,
#         --realizado.receita_realizada,
#         plan.investimento as investimento_plan,
#         --plan.roas as roas_plan,
#         --plan.receita as receita_plan
#         FROM ( 
#             SELECT *
#             FROM '''+schema+'''.'''+table_metas+''' 
#         ) plan
#         LEFT JOIN ( 
#             SELECT 
#             ano,mes,canal,
#             SUM(investimento) investimento_realizado,
#             --SUM(receita) receita_realizada
#             FROM '''+schema+'''.'''+table_compiled+'''
#             GROUP BY ano,mes,canal
#             ORDER BY SUM(investimento) DESC
#         ) realizado
#         ON plan.ano = realizado.ano
#         AND plan.mes = realizado.mes
#         AND plan.veiculo = realizado.canal
#     )t1 WHERE investimento_plan IS NOT NULL

#     )

#     '''

#     client = connect_google_big_query()
#     job_config = bigquery.QueryJobConfig()
#     job_config.priority = bigquery.QueryPriority.INTERACTIVE
#     query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
#     time.sleep(5)
#     results = query_job.result()
#     print(results)

#     state = query_job.state
#     errors = query_job.errors
#     created = query_job.created
#     destination = query_job.destination
#     project = destination.project
#     dataset_id = destination.dataset_id
#     table_id = destination.table_id
#     print('''
#     Status: '''+state+'''
#     Erros: '''+str(errors)+'''
#     Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
#     Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
#     ''')


def create_bq_table_nestle_overview_investimento_roas(
        schema, table_metas, table_compiled, table_name
):
    

    '''
    ====================================================================
    ==== CRIAÇÃO DA TABELA analyst.nestle_XXX_overview ===
    ====================================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (

    SELECT 
    ano, mes, canal, 
    COALESCE(investimento_realizado,0) investimento_realizado,
    COALESCE(receita_realizada,0) receita_realizada,
    COALESCE(investimento_plan,0) investimento_plan,
    COALESCE(roas_plan,0) roas_plan,
    COALESCE(receita_plan,0) receita_plan
    FROM (
        SELECT 
        plan.ano,
        plan.mes,
        plan.veiculo as canal,
        realizado.investimento_realizado,
        realizado.receita_realizada,
        plan.investimento as investimento_plan,
        plan.roas as roas_plan,
        plan.receita as receita_plan
        FROM ( 
            SELECT *
            FROM '''+schema+'''.'''+table_metas+''' 
        ) plan
        LEFT JOIN ( 
            SELECT 
            ano,mes,canal,
            SUM(investimento) investimento_realizado,
            SUM(receita) receita_realizada
            FROM '''+schema+'''.'''+table_compiled+'''
            GROUP BY ano,mes,canal
            ORDER BY SUM(investimento) DESC
        ) realizado
        ON plan.ano = realizado.ano
        AND plan.mes = realizado.mes
        AND plan.veiculo = realizado.canal
    )t1 WHERE investimento_plan IS NOT NULL

    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')



def create_bq_table_nestle_ultima_atualizacao(schema, 
    source_table_senior,
    source_table_avante,
    source_table_nav,
    source_table_fiber_mais,
    source_table_beauty,
    source_table_dolce_gusto,
    source_table_protein,
    source_table_celltrient,
    source_table_pip,
    source_table_molico,
    table_name):

    

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_ultima_atualizacao ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT 
    *  
    FROM (
    SELECT 
    DISTINCT 'Nutren Senior' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_senior + ''' 
    UNION ALL
    SELECT 
    DISTINCT 'Avante' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_avante + ''' 
    UNION ALL
    SELECT 
    DISTINCT 'NAV' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_nav + '''  
    UNION ALL
    SELECT 
    DISTINCT 'Fiber Mais' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_fiber_mais + ''' 
    UNION ALL
    SELECT 
    DISTINCT 'Nutren Beauty' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_beauty + ''' 
    UNION ALL
    SELECT 
    DISTINCT 'Dolce Gusto' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_dolce_gusto + '''
    UNION ALL
    SELECT 
    DISTINCT 'Nutren Protein' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_protein + '''
    UNION ALL
    SELECT 
    DISTINCT 'Nutren Celltrient' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_celltrient + '''
    UNION ALL
    SELECT 
    DISTINCT 'Pip Oncologia' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_pip + '''  
    UNION ALL
    SELECT 
    DISTINCT 'Molico' as conta, 
    canal, 
    ultima_atualizacao
    FROM ''' + schema + '''.''' + source_table_molico + '''    
    ) t

    )


    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_all_accounts(dataset, 
    table_name):

    

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_all_accounts_cdm ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    ''' + dataset + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (  
    SELECT 
    api_source ,
    fct.date_id as data,
    calendar.year_id as ano,
    calendar.month_number as mes,
    dim.account_name as conta,
    campaign_name as campanha,
    campaign_objective as objetivo_campanha,
    SUM(fct.spend ) as investimento,
    SUM(fct.impressions ) as impressoes,
    SUM(fct.clicks ) as cliques,
    SUM(fct.video_views_100pct ) as views_completas
    FROM cdm.ad_dim dim 
    LEFT JOIN cdm.ad_fct fct
    ON dim.ad_sk = fct.ad_sk 
    LEFT JOIN wmcpub.public.time_dim calendar
    ON fct.date_id = calendar.date_id
    WHERE 
    fct.date_id >= '2019-01-01'
    GROUP BY 
    api_source,
    fct.date_id,
    calendar.year_id ,
    calendar.month_number ,
    dim.account_name,
    campaign_name ,
    campaign_objective
    ORDER BY 
    calendar.year_id ,
    calendar.month_number ,
    dim.account_name
   
    ) t

    )


    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nav_ga_temp(schema, table_name, table_name_2):

    # credentials_file = "bqcredentials.json"
    # log = logger("bigquery_loader.log")
    # bq = BigQuery(credentials_file, log)




    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_ga_temp ====
    ========================================================
    '''

    query = '''
    
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,    
    campaign as campanha,
    source_e_medium,
    CASE 
        WHEN lower(campaign) LIKE '%shopping%' THEN 'Shopping' 
        WHEN source_e_medium LIKE '%google / cpc%' AND lower(campaign) NOT LIKE '%shopping%' THEN 'Search' 
        WHEN source_e_medium LIKE '%organic%' THEN 'Orgânico'
        WHEN source_e_medium LIKE '%referral%' THEN 'Referência'
        WHEN source_e_medium LIKE '%bing / cpc%' THEN 'Bing'
        WHEN (source_e_medium LIKE '%kwanko%' AND source_e_medium NOT LIKE '%referral%' )
            OR lower(campaign) LIKE '%kwanko%' THEN 'Kwanko'
        WHEN lower(campaign) LIKE '%ybox%' THEN 'Ybox'    
        WHEN lower(source_e_medium) LIKE '%fb%' OR lower(source_e_medium) LIKE 'if%'  THEN 'Facebook'
        WHEN lower(source_e_medium) LIKE '%criteo%'  THEN 'Criteo'
        WHEN lower(source_e_medium) LIKE '%comvoce-rf_click / portal%'  THEN 'Portal Nestlé'
        WHEN lower(source_e_medium) LIKE '%direct%' 
            OR lower(source_e_medium) LIKE '%direto%' THEN 'Direto'
        WHEN lower(source_e_medium) LIKE '%shopback%'  THEN 'Shopback'
        WHEN lower(source_e_medium) LIKE '%newsletter%'  THEN 'Newsletter'
        WHEN lower(source_e_medium) LIKE '%insightmedia%'   
            OR lower(campaign) LIKE '%insight%' THEN 'Insight Media'
        WHEN lower(source_e_medium) LIKE '%verizon / portal%'  THEN 'Verizon'
        WHEN lower(source_e_medium) LIKE '%crm%'  THEN 'CRM'
        WHEN lower(source_e_medium) LIKE '%/ lett%'  THEN 'Lett'
        WHEN lower(source_e_medium) LIKE '%email / email%'  THEN 'Email'
        WHEN lower(source_e_medium) LIKE '%sms / sms%'  THEN 'SMS'
        WHEN lower(source_e_medium) LIKE '%anivernav / email%'  THEN 'NAV'
        WHEN lower(source_e_medium) LIKE '%adaction%'  THEN 'Adaction'
        WHEN lower(source_e_medium) LIKE '%dv360%'  
            OR source_e_medium IN (
            'dbm-cpm / display','gmail-cpc / display',
            'dfa / DIS','DV_OA_MultiplePubs / DIS')
            THEN 'Display'
        ELSE 'Nenhum' 
    END as canal,
    CAST(REPLACE(transaction_revenue,',','.') AS FLOAT64) as receita,
    CAST(transactions AS INT64) as vendas,
    CAST(sessions AS INT64) as sessoes
    --t1.ultima_atualizacao
    FROM `analyst.nestle_nav_ga` 
    ) t0
    CROSS JOIN (
    SELECT MAX(date) as ultima_atualizacao
    FROM `analyst.nestle_nav_ga`) t1

    )
    
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

    '''
    ========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_ga_temp_2 ====
    ========================================================
    '''



    query_2 = '''

        CREATE OR REPLACE TABLE 
        '''+schema+'''.'''+table_name_2+''' AS 
        (
        SELECT 
        EXTRACT(YEAR FROM data) ano,
        EXTRACT(MONTH FROM data) mes,
        data, campanha, canal,
        source_e_medium,
        CASE
            WHEN canal IN (
            'Search','Shopping','Bing',
            'Facebook','Shopback','Kwanko',
            'Display','Adaction','Inflr','Ybox',
            'Insight Media','Criteo','Logan','Verizon'
            ) 
            THEN 'Mídia'
            ELSE 'Outros'
        END tipo_origem,
        CASE 
            WHEN canal = 'Shopback' THEN ROUND(receita * 0.065,2)
            WHEN canal = 'Kwanko' 
            AND data <= '2020-04-30'
            THEN ROUND(receita * 0.1,2)
            WHEN canal = 'Adaction' THEN ROUND(receita * 0.1,2)
            WHEN canal = 'Ybox' THEN ROUND(receita * 0.08,2)
            ELSE 0
        END as investimento,
        receita,
        vendas,
        sessoes,
        CAST(ultima_atualizacao AS DATE) as ultima_atualizacao
        FROM analyst.nestle_nav_ga_temp
        )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query_2, job_config= job_config, job_id_prefix='table_2_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nav_search_temp(
        schema, table_source, table_name
):



    '''
    ==========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_search_temp ====
    ==========================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    CASE 
        WHEN LENGTH(campaign_name) > 0 
            AND lower(campaign_name) LIKE '%shopping%' THEN 'Shopping'
        WHEN LENGTH(campaign_name) > 0 
            AND lower(campaign_name) NOT LIKE '%shopping%' THEN 'Search'
        ELSE ''
    END canal,
    campaign_name as campanha,
    ad_group_name as grupo_anuncios,
    'Mídia' tipo_origem,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    clicks as cliques,
    0 as receita,
    0 as vendas,
    0 as sessoes
    --CURRENT_TIMESTAMP() as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+'''
     ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+''') t1
    )

    
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_2_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nav_logan_temp(
        schema, table_source, table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_logan_temp ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    select 
    CAST(SPLIT(data,'/')[OFFSET(2)] AS INT64) as ano,
    CAST(SPLIT(data,'/')[OFFSET(0)] AS INT64) as mes,
    --CAST(SPLIT(data,'/')[OFFSET(1)] AS INT64) as dia,
    LPAD(CAST(SPLIT(data,'/')[OFFSET(2)] AS STRING),4,'0')||"-"||
    LPAD(CAST(SPLIT(data,'/')[OFFSET(0)] AS STRING),2,'0') ||"-"||
    LPAD(CAST(SPLIT(data,'/')[OFFSET(1)] AS STRING),2,'0') as data,
    'Logan' as campaign_name,
    'Logan' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(REPLACE(total_investido,'R$','') ,',','.') AS FLOAT64) as investimento,
    0 as receita,
    0 as vendas,
    0 as sessoes
    --CURRENT_TIMESTAMP() as ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + '''
    ) t0
    CROSS JOIN (
    SELECT CAST(
    MAX(
    LPAD(CAST(SPLIT(data,'/')[OFFSET(2)] AS STRING),4,'0')||"-"||
    LPAD(CAST(SPLIT(data,'/')[OFFSET(0)] AS STRING),2,'0') ||"-"||
    LPAD(CAST(SPLIT(data,'/')[OFFSET(1)] AS STRING),2,'0'))
     AS DATE) as ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + ''') t1
   

    )


    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_2_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')





def create_bq_table_nestle_nav_bing_temp(
    schema, table_source, table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_bing_temp ====
    ======================================================
    '''

    query = '''
    
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    campaign_name,
    'Bing' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    clicks as cliques,
    0 as receita,
    0 as vendas,
    0 as sessoes
    --CURRENT_TIMESTAMP() as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+'''
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+''') t1

    )
    
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_2_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nav_facebook_temp(
    schema, table_source, table_name
):



    '''
    ==========================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_facebook_temp ====
    ==========================================================
    '''



    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
     campaign_name,
     campaign_objective,
     publisher_platform as plataforma,
     ad_set_name as adset_name,
    'Facebook' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    CASE 
    	WHEN reach LIKE '%calculated%' 
    	THEN 0
    	ELSE CAST(reach AS INT64) 
    END as alcance,
    link_clicks as cliques,
    CAST(frequency AS FLOAT64) as frequencia,
    three_second_video_views,
    video_watches_at_100perc,
    ad_creative_thumbnail_url as ad_creative_thumbnail,
    0 as receita,
    0 as vendas,
    0 as sessoes
    FROM '''+schema+'''.'''+table_source+'''
    ) t0
    CROSS JOIN (
    SELECT CAST(MAX(date) AS DATE) as ultima_atualizacao
    FROM '''+schema+'''.'''+table_source+''') t1
    )
    
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nhs_nutren_beauty_compiled_midias(
        schema,
        table_source1,
        table_source2,
        table_source3,
        table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_compiled_midias ====
    ======================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT 
    *  
    FROM (
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    video_starts as video_starts,
    video_completions as video_completions,
    ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source1 + ''' 
    UNION ALL
    SELECT 
    ano, mes, CAST(data AS DATE) data, canal,
    investimento,
    impressoes,
    cliques,
    three_second_video_views as video_starts,
    video_watches_at_100perc as video_completions,
    ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source2 + '''
    UNION ALL
    SELECT 
    ano, mes, data, canal,
    investimento,
    impressoes,
    cliques,
    video_starts as video_starts,
    video_completions as video_completions,
    data_max as ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source3 + '''
    ) t

    )


    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')


def create_bq_table_nestle_nav_compiled_midias_temp(
    schema,
    table_source1,
    table_source2,
    table_source3,
    table_source4,
    table_source5,
    table_source6,
    table_source7,
    table_name
):



    '''
    ===============================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_compiled_midias ====
    ===============================================================
    '''

    query = '''
        CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT 
    *
    FROM (
        SELECT * FROM '''+schema+'''.'''+table_source1+'''
        UNION ALL
        SELECT * FROM '''+schema+'''.'''+table_source2+'''
        --SELECT ano, mes, 
        --CAST(data AS STRING) as data, campanha as campaign_name,
        --canal, 'Mídia' as tipo_origem, investimento,
        --0 as receita, 0 as vendas, 0 as sessoes,
        --ultima_atualizacao
        --FROM analyst.nestle_nav_gads
        UNION ALL
        SELECT * FROM '''+schema+'''.'''+table_source3+'''
        --SELECT ano, mes, 
        --CAST(data AS STRING) as data, campaign_name as campaign_name,
        --canal, 'Mídia' as tipo_origem, investimento,
        --0 as receita, 0 as vendas, 0 as sessoes,
        --ultima_atualizacao
        --FROM analyst.nestle_nav_fb
        UNION ALL
        SELECT * FROM '''+schema+'''.'''+table_source4+'''
        --SELECT ano, mes, 
        --CAST(data AS STRING) as data, insertion_name as campaign_name,
        --canal, 'Mídia' as tipo_origem, investimento,
        --0 as receita, 0 as vendas, 0 as sessoes,
        --ultima_atualizacao
        --FROM analyst.nestle_nav_dv 
        UNION ALL
        SELECT * FROM '''+schema+'''.'''+table_source5+'''
        UNION ALL
        SELECT
        ano, mes, data,
        campaign_name , canal, tipo_origem ,
        investimento , receita , vendas , sessoes ,
        CAST(ultima_atualizacao_temp AS DATE) as ultima_atualizacao 
        FROM '''+schema+'''.'''+table_source6+'''
        UNION ALL
        SELECT * FROM '''+schema+'''.'''+table_source7+'''
    ) t

    )

    
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_metas_investimento_roas(
    schema, table_source, table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_XXX_metas ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    '''+schema+'''.'''+table_name+''' AS 
    (
    SELECT 
    ano,
    mes,
    veiculo,
    CAST(investimento AS FLOAT64) as investimento,
    CAST(roas AS FLOAT64) as roas,
    CAST(investimento AS FLOAT64) * CAST(roas AS FLOAT64) as receita
    FROM '''+schema+'''.'''+table_source+'''

    )
    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nhs_nutren_beauty_fb(
    schema,table_source, table_name):



    '''
    ================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_beauty_fb ====
    ================================================================
    '''

    query = '''

    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(date AS DATE) as data,
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    'Facebook' as canal,
    campaign_name,
    /*
    CASE 
    WHEN campaign_name LIKE '%BL_HUMANO%' THEN 'Humano'
    WHEN campaign_name LIKE '%BL_RAPOSA%' THEN 'Raposa'
    WHEN campaign_name LIKE '%NUTRENPROTEIN_SATISFYING%' THEN 'Satisfying'
    WHEN campaign_name LIKE '%STORIES%' THEN 'Stories'
    WHEN campaign_name LIKE '%Alok%' THEN 'Oportunidade Alok'
    WHEN campaign_name LIKE '%ONGS%' THEN 'Micro - ONGs'
    WHEN campaign_name LIKE '%PRODUTO%' THEN 'Nutren Protein Produtos'
    WHEN campaign_name LIKE '%NESTLE%CONTENT%' THEN 'Nutren Protein Content'
    WHEN campaign_name LIKE '%NAMORADOS%' THEN 'Dia dos Namorados'
    WHEN campaign_name LIKE '%OFERTACO%' THEN 'Ofertaço'
    WHEN campaign_name LIKE '%ZUMBA%' THEN 'Micro - Zumba'
    WHEN campaign_name LIKE '%CHEGOU_NUTREN_PROTEIN%' THEN 'Personagens'
    ELSE 'Não Identificado'
    END campanha,
    */
    ad_set_name as adset_name,
    ad_creative_thumbnail_url as ad_creative_thumbnail,
    campaign_objective,
    publisher_platform as plataforma,
    CAST(REPLACE(cost,',','.') AS FLOAT64) as investimento,
    impressions as impressoes,
    reach as alcance,
    link_clicks as cliques,
    CAST(frequency AS FLOAT64) as frequencia,
    CAST(REPLACE(ctr_all,',','.') AS FLOAT64) ctr_all, 
    CAST(REPLACE(cpc_all,',','.') AS FLOAT64) cpc_all, 
    CAST(REPLACE(ctr_link_click_through_rate,',','.') AS FLOAT64) ctr_link_click, 
    cpm_cost_per_1000_impressions, 
    three_second_video_views, 
    video_watches_at_25perc,
    video_watches_at_50perc,
    video_watches_at_75perc,
    video_watches_at_100perc, 
    cost_per_three_second_video_view
    FROM ''' + schema + '''.''' + table_source + '''
    )t0
    CROSS JOIN (
    SELECT MAX(CAST(date AS DATE)) ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + '''
    ) t1
    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nhs_nutren_beauty_dv(
        schema, table_source, table_name
):


    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_dv_temp ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    ''' + schema + '''.''' + table_name + ''' AS 
    (
    SELECT * FROM (
    SELECT 
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    CAST(date AS DATE) as data, 
    campaign as campaign_name,
    '' as campaign_objective,
    line_item as line_item,
    SPLIT(line_item,'|')[OFFSET(12)] as line_item_custom,
    insertion_order as io_name,
    'Youtube' as canal,
    'Mídia' tipo_origem,
    CAST(REPLACE(revenue,'R$ ','') AS FLOAT64) AS investimento,
    impressions as impressoes,
    clicks as cliques,
    video_plays as video_starts,
    video_1st_quartile_completes_ as video_watches_at_25perc,
    video_mid_points as video_watches_at_50perc,
    video_3rd_quartile_completes as video_watches_at_75perc,
    video_completions
    FROM ''' + schema + '''.''' + table_source + '''
    ) t0
    CROSS JOIN (
    SELECT MAX(CAST(date AS DATE)) ultima_atualizacao
    FROM ''' + schema + '''.''' + table_source + '''
    ) t1
    )

    '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')

def create_bq_table_nestle_nav_assisted_conversion_temp(schema, table_name):


    '''
    ========================================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nav_assisted_conversion_temp ====
    ========================================================================
    '''

    # query = '''
    #
    # CREATE OR REPLACE TABLE
    # ''' + schema + '''.''' + table_name + ''' AS
    # (
    #
    # SELECT
    # CAST(SUBSTR(date,1,4) AS INT64) as ano,
    # CAST(SUBSTR(date,6,2) AS INT64) as mes,
    # date as data,
    # campaign as campaign_name,
    # CASE
    #     WHEN lower(campaign) LIKE '%shopping%' THEN 'Shopping'
    #     WHEN lower(campaign) LIKE '%(not set)%' THEN 'Direto'
    #     ELSE 'Search'
    # END as canal,
    # CAST(REPLACE(assisted_conversion_value,',','.') AS FLOAT64) as receita_assistida,
    # assisted_conversions as vendas_assistidas
    #
    # FROM `analyst.nestle_nav_assisted_conversion`
    #
    # )
    #
    # '''

    query = '''

        CREATE OR REPLACE TABLE 
        ''' + schema + '''.''' + table_name + ''' AS 
        (

            SELECT 
    CAST(SUBSTR(date,1,4) AS INT64) as ano,
    CAST(SUBSTR(date,6,2) AS INT64) as mes,
    date as data,    
    campaign as campaign_name,
    /*
    CASE 
        WHEN lower(campaign) LIKE '%shopping%' THEN 'Shopping' 
        WHEN lower(campaign) LIKE '%(not set)%' THEN 'Direto'
        ELSE 'Search' 
    END as canal,
    */
    CASE 
        WHEN lower(campaign) LIKE '%shopping%' THEN 'Shopping' 
        WHEN source_e_medium LIKE '%google / cpc%' AND lower(campaign) NOT LIKE '%shopping%' THEN 'Search' 
        WHEN source_e_medium LIKE '%organic%' THEN 'Orgânico'
        WHEN source_e_medium LIKE '%referral%' THEN 'Referência'
        WHEN source_e_medium LIKE '%bing / cpc%' THEN 'Bing'
        WHEN (source_e_medium LIKE '%kwanko%' AND source_e_medium NOT LIKE '%referral%' )
            OR lower(campaign) LIKE '%kwanko%' THEN 'Kwanko'
        WHEN lower(campaign) LIKE '%ybox%' THEN 'Ybox'    
        WHEN lower(source_e_medium) LIKE 'fb%' OR lower(source_e_medium) LIKE 'if%'  THEN 'Facebook'
        WHEN lower(source_e_medium) LIKE '%criteo%'  THEN 'Criteo'
        WHEN lower(source_e_medium) LIKE '%comvoce-rf_click / portal%'  THEN 'Portal Nestlé'
        WHEN lower(source_e_medium) LIKE '%direct%' 
            OR lower(source_e_medium) LIKE '%direto%' THEN 'Direto'
        WHEN lower(source_e_medium) LIKE '%shopback%'  THEN 'Shopback'
        WHEN lower(source_e_medium) LIKE '%newsletter%'  THEN 'Newsletter'
        WHEN lower(source_e_medium) LIKE '%insightmedia%'   
            OR lower(campaign) LIKE '%insight%' THEN 'Insight Media'
        WHEN lower(source_e_medium) LIKE '%verizon / portal%'  THEN 'Verizon'
        WHEN lower(source_e_medium) LIKE '%crm%'  THEN 'CRM'
        WHEN lower(source_e_medium) LIKE '%/ lett%'  THEN 'Lett'
        WHEN lower(source_e_medium) LIKE '%email / email%'  THEN 'Email'
        WHEN lower(source_e_medium) LIKE '%sms / sms%'  THEN 'SMS'
        WHEN lower(source_e_medium) LIKE '%anivernav / email%'  THEN 'NAV'
        WHEN lower(source_e_medium) LIKE '%adaction%'  THEN 'Adaction'
        WHEN lower(source_e_medium) LIKE '%dv360%'  
            OR source_e_medium IN (
            'dbm-cpm / display','gmail-cpc / display',
            'dfa / DIS','DV_OA_MultiplePubs / DIS')
            THEN 'Display'
        ELSE 'Nenhum' 
    END as canal,
    CAST(REPLACE(assisted_conversion_value,',','.') AS FLOAT64) as receita_assistida,
    assisted_conversions as vendas_assistidas
    FROM `analyst.nestle_nav_assisted_conversion`

        )

        '''


    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE
    query_job = client.query(query, job_config= job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: '''+state+'''
    Erros: '''+str(errors)+'''
    Tabela: '''+project+'.'+dataset_id+'.'+table_id+'''
    Data: '''+created.strftime("%d/%m/%Y %H:%M:%S")+'''
    ''')




def create_bq_table_nestle_compiled_midias(
        dataset, 
        source_table_ganl,
        source_table_gads, 
        source_table_fb, 
        source_table_dv,
        source_table_linkedin,
        source_table_bing,
        source_table_criteo,
        table_name):


    query_ganl = '''
        SELECT 
        CAST(data as DATE) as date, 
        ano, mes, canal,
        tipo_origem,
        campanha,
        '' as objetivo_campanha,
        '' as plataforma,
        '' as grupo_anuncios,
        investimento,
        0 as impressoes,
        0 as alcance,
        0 as cliques,
        0 as frequencia,
        0 as three_second_video_views,
        0 as video_watches_at_100perc,
        NULL as ad_creative_thumbnail,
        receita,
        vendas,
        sessoes,
        ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_ganl + '''

    '''

    if source_table_ganl == '':
        query_ganl = ''

    query_gads = '''
        SELECT 
        CAST(data as DATE) as date, 
        ano, mes, canal, 
        'Mídia' as tipo_origem,
        campanha,
        '' as objetivo_campanha,
        '' as plataforma,
        grupo_anuncios,
        investimento, 
        impressoes, 
        0 as alcance,
        cliques,
        0 as frequencia,
        0 as three_second_video_views,
        0 as video_watches_at_100perc,
        NULL as ad_creative_thumbnail,
        0 as receita,
        0 as vendas,
        0 as sessoes,
        ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_gads + '''

    '''

    if source_table_gads == '':
        query_gads = ''

    query_fb = '''
        SELECT 
        CAST(data as DATE) as date,ano,mes,canal,
        'Mídia' as tipo_origem,
        campaign_name as campanha,
        campaign_objective as objetivo_campanha,
        plataforma,
        adset_name as grupo_anuncios,
        investimento, 
        impressoes, 
        alcance, 
        cliques,
        frequencia,
        three_second_video_views,
        video_watches_at_100perc,
        ad_creative_thumbnail,
        0 as receita,
        0 as vendas,
        0 as sessoes,
        ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_fb + '''

    '''

    if source_table_fb == '':
        query_fb = ''

    query_dv = '''
        SELECT 
        data as date,ano,mes,canal,
        'Mídia' as tipo_origem,
        campaign_name as campanha,
        campaign_objective as objetivo_campanha,
        '' AS plataforma,
        io_name as grupo_anuncios,
        investimento, 
        impressoes, 
        0 AS alcance, 
        cliques,
        0 AS frequencia,
        video_starts as three_second_video_views,
        video_completions as video_watches_at_100perc,
        NULL AS ad_creative_thumbnail,
        0 as receita,
        0 as vendas,
        0 as sessoes,
        ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_dv + '''
    '''

    if source_table_dv == '':
        query_dv = ''
    
    query_linkedin = '''
        SELECT 
        data as date,ano,mes,canal,
        'Mídia' as tipo_origem,
        campaign_name as campanha,
        '' as objetivo_campanha,
        '' AS plataforma,
        ad_headline as grupo_anuncios,
        investimento, 
        impressoes, 
        0 AS alcance, 
        cliques,
        0 AS frequencia,
        video_views as three_second_video_views,
        video_completions as video_watches_at_100perc,
        NULL AS ad_creative_thumbnail,
        0 as receita,
        0 as vendas,
        0 as sessoes,
        data_max as ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_linkedin + '''
    '''

    if source_table_linkedin == '':
        query_linkedin = ''

    query_bing = '''
        SELECT 
        CAST(data as DATE) as date, 
        ano, mes, canal, 
        'Mídia' as tipo_origem,
        campaign_name as campanha,
        '' as objetivo_campanha,
        '' as plataforma,
        '' as grupo_anuncios,
        investimento, 
        impressoes, 
        0 as alcance,
        cliques,
        0 as frequencia,
        0 as three_second_video_views,
        0 as video_watches_at_100perc,
        NULL as ad_creative_thumbnail,  
        0 as receita,
        0 as vendas,
        0 as sessoes,
        ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_bing + '''

    '''

    if source_table_bing == '':
        query_bing = ''

    query_criteo = '''
        SELECT 
        CAST(data as DATE) as date, 
        ano, mes, canal, 
        'Mídia' as tipo_origem,
        campaign_name as campanha,
        '' as objetivo_campanha,
        '' as plataforma,
        '' as grupo_anuncios,
        investimento, 
        impressoes, 
        0 as alcance,
        cliques,
        0 as frequencia,
        0 as three_second_video_views,
        0 as video_watches_at_100perc,
        NULL as ad_creative_thumbnail,  
        0 as receita,
        0 as vendas,
        0 as sessoes,
        ultima_atualizacao_temp as ultima_atualizacao
        FROM ''' + dataset + '''.''' + source_table_criteo + '''

    '''

    if source_table_criteo == '':
        query_criteo = ''

    queries = [query_ganl,
               query_gads, 
               query_fb, 
               query_dv,
               query_linkedin,
               query_bing,
               query_criteo]
    while ("" in queries):
        queries.remove("")
    query_union = ' UNION ALL '.join(queries)

    '''
    ======================================================
    ===== CRIAÇÃO DA TABELA analyst.nestle_nhs_nutren_senior_compiled_midias ====
    ======================================================
    '''

    query = '''
    CREATE OR REPLACE TABLE 
    ''' + dataset + '''.''' + table_name + ''' AS 
    (
    SELECT 
    *  
    FROM (
    '''+query_union+'''
    )t
    )
    '''


    # query = '''
    #     CREATE OR REPLACE TABLE
    # ''' + dataset + '''.''' + table_name + ''' AS
    # (
    # SELECT
    # *
    # FROM (
    #     SELECT
    #     CAST(data as DATE) as date,
    #     ano, mes, canal,
    #     campanha,
    #     '' as objetivo_campanha,
    #     '' as plataforma,
    #     grupo_anuncios,
    #     investimento,
    #     impressoes,
    #     0 as alcance,
    #     cliques,
    #     0 as frequencia,
    #     0 as three_second_video_views,
    #     0 as video_watches_at_100perc,
    #     NULL as ad_creative_thumbnail,
    #     ultima_atualizacao
    #     FROM ''' + dataset + '''.''' + source_table_gads + '''
    #     UNION ALL
    #     SELECT
    #     data as date,ano,mes,canal,
    #     campaign_name as campanha,
    #     campaign_objective as objetivo_campanha,
    #     plataforma,
    #     adset_name as grupo_anuncios,
    #     investimento,
    #     impressoes,
    #     alcance,
    #     cliques,
    #     frequencia,
    #     three_second_video_views,
    #     video_watches_at_100perc,
    #     ad_creative_thumbnail,
    #     ultima_atualizacao
    #     FROM ''' + dataset + '''.''' + source_table_fb + '''
    #     UNION ALL
    #     SELECT
    #     data as date,ano,mes,canal,
    #     campaign_name as campanha,
    #     NULL as objetivo_campanha,
    #     NULL AS plataforma,
    #     insertion_name as grupo_anuncios,
    #     investimento,
    #     impressoes,
    #     NULL AS alcance,
    #     cliques,
    #     NULL AS frequencia,
    #     video_starts as three_second_video_views,
    #     video_completions as video_watches_at_100perc,
    #     NULL AS ad_creative_thumbnail,
    #     ultima_atualizacao
    #     FROM ''' + dataset + '''.''' + source_table_dv + '''
    # ) t
    #
    # )
    #
    #
    # '''

    client = connect_google_big_query()
    job_config = bigquery.QueryJobConfig()
    job_config.priority = bigquery.QueryPriority.INTERACTIVE

    query_job = client.query(query, job_config=job_config, job_id_prefix='table_')
    time.sleep(5)
    results = query_job.result()
    print(results)

    state = query_job.state
    errors = query_job.errors
    created = query_job.created
    destination = query_job.destination
    project = destination.project
    dataset_id = destination.dataset_id
    table_id = destination.table_id
    print('''
    Status: ''' + state + '''
    Erros: ''' + str(errors) + '''
    Tabela: ''' + project + '.' + dataset_id + '.' + table_id + '''
    Data: ''' + created.strftime("%d/%m/%Y %H:%M:%S") + '''
    ''')



