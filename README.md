### Prerequisites

- Python 2.7 com Scikit-Learn (Anaconda é altamente recomendado)
  - https://www.anaconda.com/distribution/

- XGboost ( versão >= 0.82 para evitar bugs  )
  - siga os passos em https://pypi.org/project/xgboost/

- funcsigs library
  - siga  os passos em https://pypi.org/project/funcsigs/

- sqlite3
  - para uma experiência amigável ao navegar na base de dados   
    https://sqlitebrowser.org/
  

### Estrutura do repositório
	- dados - pasta que contém os dados utilizados no experimento (as bases estão zipadas, extraia nessa pasta)
	- dados_tratados - contém os dados tratados usados no trabalho e alguns .csv usados de suporte
		- testdb.zip - arquivo zipado que contém a base do sqlite com os dados tratados (zipado devido ao tamanho descompactado ser maior que 100 MB, extraia nessa pasta)
	- scripts		
		- db.py - implementação de conector da base de dados
		- filtering_stage.py - script que faz a filtragem dos dados
		- merge_atendimentos.py - script que faz merge de atendimentos de um paciente
		- populate_table.py - script que lê o arquivo hsl_lab_result_1_fixed.csv e popula a tabela criada em prepare_data.py
		- prepare_data.py - script que cria a tabela no testdb onde cada tipo de análise é uma coluna
		- results.py - implementação de classe de estatística para análise da matriz de confusão 		
		- run_model.py - script que roda o XGBoost
