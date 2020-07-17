#!/usr/bin/env python
#! coding: utf-8


#Esse script percorre o arquivo que contem o resultados de atendimentos dos pacientes na tabela criada pelo script prepare_data.py
from xgboost import XGBClassifier
from sklearn.preprocessing import scale
import numpy as np
from sklearn.model_selection import StratifiedKFold
import pandas
from pandas import DataFrame
from pandas import concat
import io
from db import DBConnection



dataPath = "/home/pablomoreira/projetos/machine_learning_covid/sirio-libanes/"
resultFile = "hsl_lab_result_1.csv"
fixedResultFile = "hsl_lab_result_1_fix.csv"
desfecho_file = "../dados/sirio-libanes/hsl_desfecho_1_fixed.csv"
lab_result_file = "../dados/sirio-libanes/hsl_lab_result_1_fixed.csv"
pacient_info_file = "../dados/sirio-libanes/hsl_patient_1.csv"


lab_result = pandas.read_csv(lab_result_file,sep='|')

dbconn = DBConnection('../dados/testdb')

cursor = dbconn.connection.cursor()

for index,row in lab_result.iterrows():
    print str(index)
    query = "SELECT * FROM organized_exams WHERE ID_PACIENTE = '"+row['ID_PACIENTE']+"' AND ID_ATENDIMENTO = '" +row['ID_ATENDIMENTO'] +"';"
    cursor.execute(query)
    result = cursor.fetchall()

    header = row['DE_EXAME'] + ".(" + row['DE_ANALITO'] + ")"
    header = header.replace(" ","_")
    
    value = row['DE_RESULTADO'].replace("'","''")
    if not result:        
        insertQuery = "INSERT INTO organized_exams(ID_PACIENTE,ID_ATENDIMENTO,DT_COLETA,DE_ORIGEM,["+ header +"])" + " VALUES('" + row['ID_PACIENTE'] +"','"+ row['ID_ATENDIMENTO'] +"','" + row['DT_COLETA'] +"','" + row['DE_ORIGEM'] +"','"+ value +"');"
        cursor.execute(insertQuery)
    else:
        updateQuery = "UPDATE organized_exams SET [" + header + "] = '"+ value + "' WHERE ID_PACIENTE = '"+ row['ID_PACIENTE'] + "' AND ID_ATENDIMENTO = '" + row['ID_ATENDIMENTO'] + "';"
        cursor.execute(updateQuery)

print "commiting to database"
dbconn.connection.commit()
print "finished"