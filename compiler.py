# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 08:56:47 2021

@author: Neal
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:26:17 2021

@author: Neal
"""

import cProfile
import json
import requests
import pandas as pd
import numpy as np
import sqlite3
import MySQLdb
from sqlalchemy import create_engine
import pymysql
import time
from dateutil.relativedelta import relativedelta
import datetime
import time
import cProfile, pstats, io

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


# BELOW IS TO CALCUALTE THE CAGR


def cashflow_before(df, current_date, years, column_name,symbol):
    before_date = (current_date - relativedelta(years = years)).year

    create_df = df.xs(symbol, level = 1)

    try:

        return create_df.loc[[before_date]][column_name].values[0]
    except:
        #print(symbol, current_date)
        #print(before_date)

        last_date = create_df['date'].iloc[-1]
        new_year = (current_date.year - last_date.year)
        return  new_year, create_df[column_name].iloc[-1]


def cagr_calc(cashflow_current, cashflow_past, years):
    if cashflow_current >= cashflow_past and cashflow_past !=0 and years !=0:
        if cashflow_past > 0:
            return (cashflow_current/cashflow_past) ** (1/years) - 1
        else:
            return ((cashflow_current - cashflow_past)/abs(cashflow_past) + 1) ** (1/years)-1
    else:
            return 0



"""IN ORDER TO USE THE BELOW:
    1. create a dataframe that parses the year out of the sql table
    2.make sure you set_index to 'year' and 'symbol'

    """
@profile
def df_test_func(df):
    count = 0
    try:
        df.insert(1, 'cagr', 0)
        print(df)
        for index,row in df.iterrows():
            cash_now = row['freeCashFlow']
            #print(row['date'])
            #print('index[1]: ',index[1])
            try:
                cash_before = cashflow_before(df, row['date'], 8, 'freeCashFlow', index[1])
                cagr_value = cagr_calc(cash_now, cash_before, 8)

            except:
                new_year, cash_before  = cashflow_before(df, row['date'], 8, 'freeCashFlow', index[1])
                cagr_value = cagr_calc(cash_now, cash_before, new_year)
            #print(cash_before, index)

            df['cagr'].iloc[count] = cagr_value
            count +=1
        return df
    except:

        for index,row in df.iterrows():
            cash_now = row['freeCashFlow']
            #print(row['date'])
            #print('index[1]: ',index[1])
            try:
                cash_before = cashflow_before(df, row['date'], 8, 'freeCashFlow', index[1])
                cagr_value = cagr_calc(cash_now, cash_before, 8)

            except:
                new_year, cash_before  = cashflow_before(df, row['date'], 8, 'freeCashFlow', index[1])
                cagr_value = cagr_calc(cash_now, cash_before, new_year)
            #print(cash_before, index)

            df['cagr'].iloc[count] = cagr_value
            count +=1
    return df


@profile
def neg_check(df):

    #USEFUL TO CHECK CAGR CALCULATIONS CORRECT. SHOULD BE ZERO NEGATIVE CAGR VALUES

    columns_dict = dict(zip(df.columns, range(len(df.columns))))
    index_dict = dict(zip(range(len(df)), df.index))
    count = 0
    df_array = df.values
    array_list = []
    for row in df_array:
        if row[columns_dict['cagr']] < 0:
            array_list.append(index_dict[count])
        count +=1
    return array_list

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

def prep_mysqlUpload(df):
    try:
        if len(df['level_0']) > 0:
            df.drop('level_0', axis = 1, inplace = True)
            df_index = df.reset_index()
            df_index = df_index.replace([np.inf, -np.inf], np.nan)
            df_index = df_index.fillna(0)
        else:
            return df_index
    except:
        df_index = df.reset_index()
        df_index = df_index.replace([np.inf, -np.inf], np.nan)
        df_index = df_index.fillna(0)
    return df_index

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:27:04 2021

@author: Neal
"""



def eight_yr(df):
    column_dict = dict(zip(df.columns, range(len(df.columns))))
    df_sample_array = df.values
    count = 0
    try:
        df.insert(1,'eight_year_value', 0)
        df.insert(1,'eight_year_stockPrice', 0)

    except:
        df

    for row in df_sample_array:
        freecashflow = row[column_dict['freeCashFlow']]
        cagr_value = row[column_dict['cagr']]
        cashandq = row[column_dict['cashAndCashEquivalents']] + row[column_dict['shortTermInvestments']]
        debt = row[column_dict['totalDebt']]
        common_stock = row[column_dict['numberOfShares']]
        if cagr_value > 0 and freecashflow > 0:


            eight_year = sum([freecashflow * (1+cagr_value) ** x for x in range(1,9)])
            df['eight_year_value'].iloc[count] = eight_year
            #print("eight year: ", eight_year)
            #print("cash and q: ", cashandq)
            #print("total debt: ", debt)
        else:
            df['eight_year_value'].iloc[count] = float(0)

        try:
            df['eight_year_stockPrice'].iloc[count] = eight_year/common_stock
        except:
            df['eight_year_stockPrice'].iloc[count] = float(0)
        count+=1
    return df

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 13:27:27 2021

@author: Neal
"""




"""
THE BELOW IS MEANT TO CALCULATE THE FOLLOWING:
    1. WINDAGE VALUES
    2. LESSER WINDAGE VALUE
    3. MARGIN OF SAFETY
"""

@profile
def mos(df, marr):

    count = 0
    try:
        df.insert(1, 'margin_of_safety', 0)
        df.insert(1, 'lesser_windage', 0)

    except:
        df
    column_dict = dict(zip(df.columns, range(len(df.columns))))
    df_array = df.values
    for row in df_array:
        if row[column_dict['eps']] > 0:
            future_share_price = row[column_dict['eps']] * (1 + row[column_dict['cagr']])**10
        else:
            future_share_price = 0
        if row[column_dict['windage_value']] < row[column_dict['windage_max_pe_value']]:
            lesser_windage = row[column_dict['windage_value']]
            df['lesser_windage'].iloc[count] = lesser_windage
        else:
            lesser_windage = row[column_dict['windage_max_pe_value']]
            df['lesser_windage'].iloc[count] = lesser_windage
        value = lesser_windage * future_share_price
        mos = value/((1 + marr)**10)
        df['margin_of_safety'].iloc[count] = mos/2
        count +=1

    return df

#array version
#@profile
def shiller_windage_func_array(df):
    count = 0
    df_array= df.values
    column_dict = dict(zip(df.columns, range(len(df.columns))))
    df.insert(1, 'shiller_pe', 0)
    df.insert(1, 'windage_value', 0)
    for row in df_array:
        if row[column_dict['eps']] > 0:
            df['shiller_pe'].iloc[count] = row[column_dict['stockPrice']]/ row[column_dict['eps']]
        else:
            df['shiller_pe'].iloc[count] = 0
        df['windage_value'].iloc[count] = 100 * 2 * row[column_dict['cagr']]
        count +=1
    return df

#pandas version
#@profile
def shiller_windage_func(df):
    count = 0
    for index, row in df.iterrows():
        if row['eps'] > 0:
            df['shiller_pe'].iloc[count] = row['stockPrice']/row['eps']
        else:
            df['shiller_pe'].iloc[count] = 0
        df['windage_value'].iloc[count] = 100 * 2 * row['cagr']
        count +=1
    return df

#@profile
def windage_pe_value(df, years):#omitted symbol
    #create_df = df.xs(symbol, level = 1)
    #current_date = create_df['date'].iloc[0]
    #before_date = (current_date - relativedelta(years = years)).year

    count = 0
    try:
        df.insert(1, 'windage_max_pe_value', 0)
    except:
        df
    for index,row in df.iterrows():

        try:
            create_df = df.xs(index[1], level = 1)
            current_date = row['date']
            before_date = (current_date - relativedelta(years = years)).year

            max_pe = create_df[(create_df['date'] <= current_date) & (create_df['date']>= str(before_date))]['shiller_pe'].max()

            df['windage_max_pe_value'].iloc[count] = max_pe
        except:
           max_pe = 0
           df['windage_max_pe_value'].iloc[count] = max_pe
        count +=1
    return df


#@profile
def windage_pe(df):
    count = 0
    for index, row in df.iterrows():
        windage_pe_v = windage_pe_value(df, index[1], 10)
        df['windage_pe_value'].iloc[count] = windage_pe_v
        count+=1
    return df

import time

start_overall = time.time()
start_sql= time.time()
query = 'SELECT * FROM finance.finance_statements'
sqlEngine = create_engine('mysql+pymysql://nnakagawa:Soccer1984!@localhost/finance')
dbConnection = sqlEngine.connect()
finance_statements = pd.read_sql(query, dbConnection)
finance_statements['date'] = finance_statements['date'].astype('datetime64[ns]')
finance_statements.insert(3, 'year', [d.year for d in finance_statements['date']])
finance_statements = finance_statements.sort_values(['symbol','date'], ascending = False)
finance_statements = finance_statements.set_index(['year','symbol'])

end_sql = time.time()



start_cagr = time.time()

df_cagr = df_test_func(finance_statements)
end_cagr = time.time()



start_eight = time.time()

df_eight = eight_yr(df_cagr)
end_eight= time.time()


start_shill = time.time()

df_shillerWindage = shiller_windage_func_array(df_eight)
end_shill = time.time()


start_wind = time.time()

df_windage_pe_value= windage_pe_value(df_shillerWindage, 10)
end_wind = time.time()




start_mos = time.time()

df_mos= mos(df_windage_pe_value, .15)
end_mos = time.time()

end_overall = time.time()

print("Overall Time: ", end_overall - start_overall)
print('time to sql: ', end_sql - start_sql)
print('this is the time for cagr: ', end_cagr - start_cagr)
print('this is the time for eight year: ', end_eight- start_eight)
print('this is the time for Shiller Windage: ', end_shill - start_shill)
print('this is the time for Windage PE Max value: ', end_wind - start_wind)
print('this is the time for mos: ', end_mos - start_mos)
