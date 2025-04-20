##############################################################################
# Import necessary modules
# #############################################################################

from Lead_scoring_data_pipeline.utils import *
from Lead_scoring_data_pipeline.data_validation_checks import *
from Lead_scoring_data_pipeline.constants import *
from Lead_scoring_data_pipeline.schema import *
from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta


###############################################################################
# Define default arguments and DAG
# ##############################################################################

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025,4,9),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


ML_data_cleaning_dag = DAG(
                dag_id = 'Lead_Scoring_Data_Engineering_Pipeline',
                default_args = default_args,
                description = 'DAG to run data pipeline for lead scoring',
                schedule_interval = '@daily',
                catchup = False
)

###############################################################################
# Create a task for build_dbs() function with task_id 'building_db'
# ##############################################################################
building_db = PythonOperator(
        task_id='building_db',
        dag = ML_data_cleaning_dag,
        python_callable=build_dbs,
        doc_md="""\
        Build Databases: Creates required database structures for the pipeline.
        Essential for storing and querying preprocessed lead scoring data.
        """
    )
###############################################################################
# Create a task for raw_data_schema_check() function with task_id 'checking_raw_data_schema'
# ##############################################################################
checking_raw_data_schema = PythonOperator(
        task_id='checking_raw_data_schema',
        dag = ML_data_cleaning_dag,
        python_callable=raw_data_schema_check,
        doc_md="""\
        Raw Data Schema Check: Validates that the incoming CSV data conforms to the expected schema.
        Prevents schema-related issues downstream.
        """
    )
###############################################################################
# Create a task for load_data_into_db() function with task_id 'loading_data'
# #############################################################################
loading_data = PythonOperator(
        task_id='loading_data',
        dag = ML_data_cleaning_dag,
        python_callable=load_data_into_db,
        doc_md="""\
        Data Loading: Ingests CSV data into the database for subsequent transformations.
        """
    )

###############################################################################
# Create a task for map_city_tier() function with task_id 'mapping_city_tier'
# ##############################################################################
mapping_city_tier = PythonOperator(
        task_id='mapping_city_tier',
        dag = ML_data_cleaning_dag,
        python_callable=map_city_tier,
        doc_md="""\
        City Tier Mapping: Transforms city-related information into standardized tier classifications.
        Improves data consistency for location-based analytics.
        """
    )
###############################################################################
# Create a task for map_categorical_vars() function with task_id 'mapping_categorical_vars'
# ##############################################################################
mapping_categorical_vars = PythonOperator(
        task_id='mapping_categorical_vars',
        dag = ML_data_cleaning_dag,
        python_callable=map_categorical_vars,
        doc_md="""\
        Categorical Variables Mapping: Processes and encodes categorical features into numerical representations.
        Essential for machine learning model compatibility.
        """
    )
###############################################################################
# Create a task for interactions_mapping() function with task_id 'mapping_interactions'
# ##############################################################################
mapping_interactions = PythonOperator(
        task_id='mapping_interactions',
        dag = ML_data_cleaning_dag,
        python_callable=interactions_mapping,
        doc_md="""\
        Interaction Mapping: Computes interaction terms between features, enhancing the feature space for modeling.
        """
    )
###############################################################################
# Create a task for model_input_schema_check() function with task_id 'checking_model_inputs_schema'
# ##############################################################################
checking_model_inputs_schema = PythonOperator(
        task_id='checking_model_inputs_schema',
        dag = ML_data_cleaning_dag,
        python_callable=model_input_schema_check,
        doc_md="""\
        Model Input Schema Check: Ensures that the transformed data matches the expected schema for the lead scoring model.
        """
    )
###############################################################################
# Define the relation between the tasks
# ##############################################################################
building_db >> checking_raw_data_schema >> loading_data >> mapping_city_tier >> \
        mapping_categorical_vars >> mapping_interactions >> checking_model_inputs_schema

