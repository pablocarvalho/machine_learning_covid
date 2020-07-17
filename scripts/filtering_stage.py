#!/usr/bin/env python
#! coding: utf-8

from xgboost import XGBClassifier
from sklearn.preprocessing import scale
import numpy as np
from sklearn.model_selection import StratifiedKFold
import pandas
from pandas import DataFrame
from pandas import concat
import io
from db import DBConnection
from datetime import *


dbconn = DBConnection('../dados/testdb')

query = """select * from merged_covid_atendimentos where ([COVID-19-PCR_para_SARS-COV-2,_Varios_Materiais_(Fleury).(Coronavirus_(2019-nCoV))] is not null
or [Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica).(Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica))] is not null) and 
([COVID-19-PCR_para_SARS-COV-2,_Varios_Materiais_(Fleury).(Coronavirus_(2019-nCoV))] is null
or [Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica).(Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica))] is null);"""

inputDF = pandas.read_sql_query(query,dbconn.connection)

print len(inputDF)

covid_pcr = list()
for index,row in inputDF.iterrows():
    result1 = ""
    result2 = ""
    result1 = row['COVID-19-PCR_para_SARS-COV-2,_Varios_Materiais_(Fleury).(Coronavirus_(2019-nCoV))']
    result2 = row['Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica).(Deteccao_de_Coronavirus_(NCoV-2019)_POR_PCR_(Anatomia_Patologica))']

    if(result1 is None and result2 is not None):
        covid_pcr.append(result2)
    elif(result1 is not None and result2 is None):
        covid_pcr.append(result1)


print len(covid_pcr)
        
inputDF['covid_pcr']=covid_pcr

# threshold = len(inputDF)*0.7

print "before drop " + str(len(inputDF.columns.values))
inputDF = inputDF.dropna(axis=1, how='all')
print "after drop " + str(len(inputDF.columns.values))

inputDF = inputDF.dropna(axis=0, how='any',thresh=40)

threshold = len(inputDF)*0.7
inputDF = inputDF.dropna(axis=1, how='any',thresh=threshold)

percent_missing = inputDF.isnull().sum() * 100 / len(inputDF)
missing_value_df = DataFrame({'column_name': inputDF.columns,
                                 'percent_missing': percent_missing})
missing_value_df.sort_values('percent_missing', inplace=True)

inputDF = inputDF.dropna(axis=0, how='any',thresh=len(inputDF.columns.values)*0.8)

inputDF.to_sql('treated_dataset',con=dbconn.connection,index=False)