import psycopg2
import pandas as pd
import h2o
from h2o.estimators import H2OGradientBoostingEstimator

def make_prediction():
    # Connection parameters
    host = 'localhost'
    database = 'masters'
    user = 'postgres'
    password = 'Jolano268'

    # Establish a connection
    connection = psycopg2.connect(host=host, database=database, user=user, password=password)

    # Create a cursor
    cursor = connection.cursor()

    # Execute a SELECT query
    query = "SELECT * FROM inference_data;"
    cursor.execute(query)

    # Fetch the column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]
    print("\nCOLUMN NAMES::\n")
    print(column_names)

    # Fetch all rows from the cursor
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]
    # print("\nDATA:\n")
    # print(data)

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(data)
    print("\nDATA FRAME:\n")
    print(df)

    # Initialize the H2O cluster
    h2o.init()

    # Convert the Pandas DataFrame to an H2O Frame
    h2o_df = h2o.H2OFrame(df)
    print("\nH2O DATA FRAME:\n")
    print(h2o_df)

    # Define the features and target variable      
    features = [column for column in column_names if column != 'recovery_duration_minutes']  
    print("\nfeatures:\n")
    print(features)

    target = "recovery_duration_minutes" 
    print("\ntarget:\n")
    print(target)

    # Use the existing model to make the prediction for the patient row
    model_path = "C:/Users/erwee/Desktop/Models/model.zip/GBM_model_python_1689593169152_1"
    saved_model = h2o.load_model(model_path)

    patient_row = h2o_df[0, features]  # Select the patient row from the validation set

    prediction = saved_model.predict(patient_row)
    print("\nprediction:\n")
    print(prediction)

    predicted_recovery_time = prediction[0, 'predict']
    print("\npredicted_recovery_time:\n")
    print(predicted_recovery_time)

    result = {
        "predicted_recovery_time": predicted_recovery_time
    }

    return result






