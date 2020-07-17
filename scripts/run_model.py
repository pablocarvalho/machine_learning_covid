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
from results import Results
from sklearn.metrics import accuracy_score, precision_score, recall_score, cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
import tabulate


query = """
select pacient_info.ic_sexo, 2020 - pacient_info.aa_nascimento as idade,  desfecho.de_tipo_atendimento, desfecho.de_desfecho, treated_dataset.* 
from
treated_dataset 
	inner join 
pacient_info 
	on pacient_info.id_paciente = treated_dataset.ID_PACIENTE
	inner join  
desfecho
	on desfecho.id_paciente = treated_dataset.ID_PACIENTE and desfecho.id_atendimento = treated_dataset.ID_ATENDIMENTO 
	and desfecho.de_desfecho != "Transferencia Inter-Hospitalar Externa - Servico de Ambulancia"  
	and desfecho.de_desfecho != "Alta por abandono" 
	and desfecho.de_desfecho != "Assistencia Domiciliar"
	and desfecho.de_desfecho != "Alta a pedido"
	and treated_dataset.[Hemograma.(Plaquetas)] != "vide contagem de plaquetas especial,"
    and covid_pcr == "DETECTADO";"""


dbconn = DBConnection('../dados/testdb')

inputDF = pandas.read_sql_query(query,dbconn.connection)

tipoAtendimento = inputDF.de_tipo_atendimento
desfecho = inputDF.de_desfecho
origem = inputDF.DE_ORIGEM
inputDF = inputDF.drop(["ID_PACIENTE","ID_ATENDIMENTO","DT_COLETA","de_tipo_atendimento","de_desfecho","DE_ORIGEM"],axis=1)

#TRATAR CAMPOS TEXTUAIS
sexo_lb = LabelEncoder()
inputDF["ic_sexo"] = sexo_lb.fit_transform(inputDF["ic_sexo"])

hemo_sve_lb = LabelEncoder()
inputDF["Hemograma.(Morfologia,_SVE)"] = hemo_sve_lb.fit_transform(inputDF["Hemograma.(Morfologia,_SVE)"])

hemo_sb_lb = LabelEncoder()
inputDF["Hemograma.(Morfologia,_SB)"] = hemo_sb_lb.fit_transform(inputDF["Hemograma.(Morfologia,_SB)"])

covid_lb = LabelEncoder()
inputDF["covid_pcr"] = covid_lb.fit_transform(inputDF["covid_pcr"])


splits = 10
xgb = XGBClassifier(nthread=6)

step = 1
seed = 8000

skf = StratifiedKFold(n_splits=splits,shuffle=True,random_state=seed)

xgb_results = Results(splits)	
xgb_prediction_list = []

origin = inputDF
origin_Y = origem

y_lb = LabelEncoder()
origin_Y = pandas.Series( y_lb.fit_transform(origin_Y) )
y_name_mapping = dict(zip(y_lb.classes_, y_lb.transform(y_lb.classes_)))

for column in inputDF:
    if inputDF.dtypes[column] == "object":
        inputDF[column] = inputDF[column].apply(lambda x: str(x).replace(',','.'))
        inputDF[column] = pandas.to_numeric(inputDF[column])


xgb_confusionmatrix = None
for train, test in skf.split(origin, origin_Y):
    step+=1

    xgb.fit(origin.iloc[train], origin_Y.iloc[train])
    xgb_prediction = xgb.predict(origin.iloc[test])
    xgb_confusionmatrix = confusion_matrix(origin_Y.iloc[test], xgb_prediction)
    xgb_prediction_list.extend(xgb_prediction)    

    xgb_results.addResult(accuracy_score(origin_Y.iloc[test],xgb_prediction),precision_score(origin_Y.iloc[test],xgb_prediction,average='macro'),
        recall_score(origin_Y.iloc[test],xgb_prediction,average='macro'),cohen_kappa_score(origin_Y.iloc[test],xgb_prediction))

print "\nXGBoost"
print y_name_mapping
print xgb_confusionmatrix
print "\n"

xgb_results.printStatistics()

 	
print "XGBoost Feature importance: "
	
headers = ['Score','Parameter']

weightGain = None
weightGain = xgb.get_booster().get_score(importance_type='weight')
data = sorted([(v,k) for k,v in weightGain.items()], reverse=True) # flip the code and name and sort
print "Feature Importance (weight):\n"
print tabulate.tabulate(data, headers=headers)	 
print "\n"

