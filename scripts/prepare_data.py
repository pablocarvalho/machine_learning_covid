#!/usr/bin/env python
#! coding: utf-8-sig


# Esse script cria uma tabela no banco sqlite contendo cada tipo de exame.(analise) como uma coluna
from xgboost import XGBClassifier
from sklearn.preprocessing import scale
import numpy as np
from sklearn.model_selection import StratifiedKFold
import pandas
from pandas import DataFrame
from pandas import concat
import io
from db import DBConnection



dataPath = "../dados/sirio-libanes/"
resultFile = "../dados_tratados/hsl_lab_result_1.csv"
fixedResultFile = "../dados_tratados/hsl_lab_result_1_fix.csv"
desfecho_file = "../dados_tratados/sirio-libanes/hsl_desfecho_1_fixed.csv"
lab_result_file = "../dados_tratados/sirio-libanes/hsl_lab_result_1_fixed.csv"
pacient_info_file = "../dados_tratados/sirio-libanes/hsl_patient_1.csv"



# print len(desfecho.id_paciente.unique())
# print len(origin)

lab_result = pandas.read_csv(lab_result_file,sep='|')
print "total de pacientes: "+ str(len(lab_result.ID_PACIENTE.unique()))

pacientInfo = pandas.read_csv(pacient_info_file,sep='|')
desfecho = pandas.read_csv(desfecho_file,sep='|')

# print len(lab_result.ID_PACIENTE.unique())

# print lab_result.DE_ANALITO

examSet = set(lab_result.DE_EXAME)
analysisSet = set(lab_result.DE_ANALITO)
print "total de tipos de exames: " + str(len(examSet))
print "total de tipos de analise: " + str(len(analysisSet))

examAnalisysSet = set()

cutDuplicates = lab_result.drop_duplicates(subset=['DE_EXAME','DE_ANALITO'])

fixedHeaders = list(lab_result.columns.values)[:4]
examHeaders = list()
examHeadersHelp = set()

print "selecionando os tipos de exame e analise"
for index,row in cutDuplicates.iterrows():
    newHeader = row['DE_EXAME'] + ".(" + row['DE_ANALITO'] + ")"
    newHeader = newHeader.replace(" ","_")
    lower = newHeader.lower()

    if lower not in examHeadersHelp:
        examHeadersHelp.add(lower)
        examHeaders.append(newHeader)

outputDatasetHeaders = fixedHeaders + examHeaders

treatedDataframe = DataFrame(columns=[outputDatasetHeaders])

print treatedDataframe.columns.values


dbconn = DBConnection('../dados/testdb')
treatedDataframe.to_sql('organized_exams',con=dbconn.connection,index=False)





