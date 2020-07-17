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

query = """select organized_exams.* from atendimentos_covid 
            inner join organized_exams
            on atendimentos_covid.ID_PACIENTE = organized_exams.ID_PACIENTE;"""

covidTestedPatientExams = pandas.read_sql_query(query,dbconn.connection)

print len(covidTestedPatientExams.columns.values)

# threshold30=len(covidTestedPatientExams)*0.3
# covidTestedPatientExams = covidTestedPatientExams.dropna(axis=1,how='any',thresh=threshold30)


colapsedDataframe = DataFrame(columns=[covidTestedPatientExams.columns.values])

for testedIdx, row in covidTestedPatientExams.iterrows():
    print "processing line: " + str(testedIdx)
    alreadyExists = colapsedDataframe.loc[colapsedDataframe['ID_PACIENTE'] == row['ID_PACIENTE']]
    
    if(alreadyExists.empty ):
        colapsedDataframe = colapsedDataframe.append(row, ignore_index=True)    
    else:
        line = colapsedDataframe.index.get_loc(alreadyExists.iloc[0].name)
        
        existentDate = alreadyExists['DT_COLETA'].values[0].split("-")
        candidateDate = row['DT_COLETA'].split("-")

        existentDate = date(int(existentDate[0]), int(existentDate[1]), int(existentDate[2])) 
        candidateDate = date(int(candidateDate[0]), int(candidateDate[1]), int(candidateDate[2])) 

        for index, item in alreadyExists.iteritems():
            
            if item is None and row[index] is not None:
                colapsedDataframe.at[line,index] = row[index]
            elif item is not None and row[index] is not None:
                if existentDate > candidateDate:
                    colapsedDataframe.at[line,index] = row[index]          
            




       

dbconn = DBConnection('testdb')
colapsedDataframe.to_sql('merged_covid_atendimentos',con=dbconn.connection,index=False)

    

print covidTestedPatientExams.columns.values
