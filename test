# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:51:44 2021

@author: Neal
"""

import json
import requests
import pandas as pd
import numpy as np
import MySQLdb
from sqlalchemy import create_engine
import pymysql
import time
from dateutil.relativedelta import relativedelta
import datetime
import cProfile, pstats, io
import time
import glob
import functools

def profile(fnc):

    """ A decorator that uses cProfile to profile a function"""
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

def mysql_upload(table_name, df, exists):

    # RUN THE prep_mysqlUpload BELOW PRIOR TO UPLOAD

    sqlEngine = create_engine('mysql+pymysql://nnakagawa:Soccer1984!@localhost/finance')
    tableName = table_name
    dbConnection = sqlEngine.connect()
    try:
        frame = df.to_sql(tableName, dbConnection, if_exists = exists)
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        print("Table {} created successfully".format(tableName))

    finally:
        dbConnection.close()


def finance_symbol_list():
    function = 'financial-statement-symbol-lists'
    url= 'https://financialmodelingprep.com/api/v3/{}'.format(function)
    params = {'apikey': apikey}
    lst = requests.get(url, params).json()
    return lst


def industry(symbol_list, function = 'profile'):
    apikey = '59348d6e97ad3aa601f5f85d7668d05a'
    params = {'apikey': apikey}
    df = pd.DataFrame()
    for ticker in symbol_list:
        url = "https://financialmodelingprep.com/api/v3/profile/{}".format(ticker)
        response = requests.get(url, params).json()
        df_response = pd.DataFrame(response)
        df = pd.concat([df, df_response])
    return df

@profile
def statement_pull(year_range, function, period = 'annual'):
    apikey = '59348d6e97ad3aa601f5f85d7668d05a'
    url=  "https://financialmodelingprep.com/api/v4/{}".format(function)
    if function == function_income:
        path = r'C:\Users\nakag\Documents\statements_\income'
    elif function == function_cash:
        path = r'C:\Users\nakag\Documents\statements_\cashflow'
    elif function == function_balance:
        path = r'C:\Users\nakag\Documents\statements_\balance'
    for year in year_range:
        params = {'apikey': apikey, 'year': year, 'period': period}
        response = requests.get(url, params = params)
        loc = path + "/doc_{}.csv".format(year)
        data = response.text
        with open(loc, 'w+') as f:
            f.write(data)

    """ below is to write to pd.dataframe"""
    lst = []
    all_files = glob.glob(path + "/*.csv")
    for file in all_files:
        try:
            df = pd.read_csv(file)
            lst.append(df)
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding = 'unicode_escape')
            lst.append(df)
    df_ = pd.concat(lst)
    df_ = df_.drop(['link', 'finalLink'], axis = 1)
    df_['date'] = df_['date'].astype('datetime64[ns]')
    df_['fillingDate'] = df_['fillingDate'].astype('datetime64[ns]')
    df_['acceptedDate'] = df_['acceptedDate'].astype('datetime64[ns]')
    return df_
'''
@profile
def _api_call_enterprise(symbol_list):
    params = {'apikey': apikey}
    function = 'enterprise-values'
    df = pd.DataFrame()
    for ticker in symbol_list:
        url= 'https://financialmodelingprep.com/api/v3/{}/{}'.format(function, ticker)
        json = requests.get(url,params = params).json()
        df_js = pd.DataFrame(json)
        df = pd.concat([df, df_js])
    df['date'] = df['date'].astype('datetime64[ns]')
    return df

'''


def industry(symbol_list, function = 'profile'):
    apikey = '59348d6e97ad3aa601f5f85d7668d05a'
    params = {'apikey': apikey}
    df = pd.DataFrame()
    for ticker in symbol_list:
        url = "https://financialmodelingprep.com/api/v3/profile/{}".format(ticker)
        response = requests.get(url, params).json()
        df_response = pd.DataFrame(response)
        df = pd.concat([df, df_response])
    return df


@profile
def _api_call_enterprise(symbol_list):
    params = {'apikey': apikey}
    function = 'enterprise-values'
    df = pd.DataFrame()
    not_avail = []
    for ticker in symbol_list:
        try:
            url= 'https://financialmodelingprep.com/api/v3/{}/{}'.format(function, ticker)
            json = requests.get(url,params = params).json()
            df_js = pd.DataFrame(json)
            df = pd.concat([df, df_js])
        except:
            not_avail.append(ticker)
            print(not_avail)
            f = open(r"C:\Users\nakag\Documents\python\not_avail_enterprise.txt", "w")
            f.write(not_avail)
            f.close()
    df['date'] = df['date'].astype('datetime64[ns]')
    return df

apikey = '59348d6e97ad3aa601f5f85d7668d05a'
function_income = 'income-statement-bulk'
function_cash = 'cash-flow-statement-bulk'
function_balance = 'balance-sheet-statement-bulk'
function_symbol_list = 'financial-statement-symbol-lists'




#start = time.time()

#symbol_list = finance_symbol_list()


df_income = statement_pull(range(2000, 2021), function_income)
print('finished: {} '.format(function_income))

mysql_upload('income_statement', df_income, 'replace')

df_balance= statement_pull(range(2000, 2021), function_balance)
print('finished: {} '.format(function_balance))
mysql_upload('balance_statement', df_balance, 'replace')

df_cash= statement_pull(range(2000, 2021), function_cash)
print('finished: {} '.format(function_cash))
mysql_upload('cashflow_statement', df_cash, 'replace')

'''
df_industry = industry(symbol_list)
mysql_upload('industry', df_industry, 'replace')
print("finishd: industry pull")
'''

#df_enterprise = _api_call_enterprise(symbol_list)
#mysql_upload('enterprise_value', df_enterprise, 'replace')
#print("finished: Enterprise Values")


def sql_compiler():
    query_b = 'SELECT * FROM finance.balance_statement'
    query_c = 'SELECT * FROM finance.cashflow_statement'
    query_i = 'SELECT * FROM finance.income_statement'
    query_v = "SELECT * FROM finance.enterprise_value"
    sqlEngine = create_engine('mysql+pymysql://nnakagawa:Soccer1984!@localhost/finance')
    dbConnection = sqlEngine.connect()
    balance_statements = pd.read_sql(query_b, dbConnection)
    cashflow_statements = pd.read_sql(query_c, dbConnection)
    income_statements = pd.read_sql(query_i, dbConnection)
    enterprise_value= pd.read_sql(query_v, dbConnection)

    #combine the dataframes and use functools to merge all 3 statements together
    dfs = [cashflow_statements, balance_statements, income_statements, enterprise_value]
    df_test = functools.reduce(lambda left, right:pd.merge(left, right, on = ['symbol', 'date']), dfs)

    #replace the names of the columns to identify which duplicate columns came from which statement
    df_test = df_test.rename(columns = {'depreciationAndAmortization_x': 'depreciationAndAmortization_cashflow',
                                        'inventory_x' : 'inventory_cashflow', 'netIncome_x': 'netIncome_cashflow'})
    df_test = df_test.rename(columns = {'depreciationAndAmortization_y': 'depreciationAndAmortization_income',
                                        'inventory_y' : 'inventory_balance', 'netIncome_y': 'netIncome_income'})
    mysql_upload('finance_statements',df_test,  'replace')
    return df_test

#sql_compiler()

#end = time.time()
#print("time taken: ", end - start)
