"""
Import necessary modules
############################################################################## 
"""

import pandas as pd
import sqlite3
from sqlite3 import Error
from Lead_scoring_data_pipeline.constants import *
from Lead_scoring_data_pipeline.schema import *
###############################################################################
# Define function to validate raw data's schema
# ############################################################################## 

def raw_data_schema_check():
    '''
    This function check if all the columns mentioned in schema.py are present in
    leadscoring.csv file or not.

   
    INPUTS
        DATA_DIRECTORY : path of the directory where 'leadscoring.csv' 
                        file is present
        raw_data_schema : schema of raw data in the form oa list/tuple as present 
                          in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Raw datas schema is in line with the schema present in schema.py' 
        else prints
        'Raw datas schema is NOT in line with the schema present in schema.py'

    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    try:
        connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)
    
        df_lead_scoring = pd.read_csv(DATA_DIRECTORY+'leadscoring.csv', index_col=[0])

        if set(df_lead_scoring.columns) == set(raw_data_schema):
            print('Raw datas schema is in line with the schema present in schema.py')
        else:
            print('Raw datas schema is NOT in line with the schema present in schema.py')
            print("Columns in CSV but not in schema:", set(df_lead_scoring.columns) - set(raw_data_schema))
            print("Columns in schema but not in CSV:", set(raw_data_schema) - set(df_lead_scoring.columns))
    
    except Exception as e:
        raise RuntimeError("Failure in raw_data_schema_check: " + str(e))
    finally:
        connection.close()
   

###############################################################################
# Define function to validate model's input schema
# ############################################################################## 

def model_input_schema_check():
    '''
    This function check if all the columns mentioned in model_input_schema in 
    schema.py are present in table named in 'model_input' in db file.

   
    INPUTS
        DB_FILE_NAME : Name of the database file
        DB_PATH : path where the db file should be present
        model_input_schema : schema of models input data in the form oa list/tuple
                          present as in 'schema.py'

    OUTPUT
        If the schema is in line then prints 
        'Models input schema is in line with the schema present in schema.py'
        else prints
        'Models input schema is NOT in line with the schema present in schema.py'
    
    SAMPLE USAGE
        raw_data_schema_check
    '''
    try:
        connection = sqlite3.connect(DB_PATH+DB_FILE_NAME)
        df_model_input = pd.read_sql('select * from model_input', connection)
    
        if set(df_model_input.columns) == set(model_input_schema):
            print('Models input schema is in line with the schema present in schema.py')
        else:
            print('Models input schema is NOT in line with the schema present in schema.py')
            print("Columns in CSV but not in schema:", set(df_model_input.columns) - set(model_input_schema))
            print("Columns in schema but not in CSV:", set(model_input_schema) - set(df_model_input.columns))
    
               
    except Error as e:
        raise RuntimeError("Failure in model_input_schema_check: " + str(e))
    finally:
        connection.close()


    
    
