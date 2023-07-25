import psycopg2
import pandas as pd
import h2o
import os
from h2o.estimators import H2OGradientBoostingEstimator
from h2o.estimators import H2OGeneralizedLinearEstimator

def train_model(Model):
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
    query = "SELECT * FROM training_data;"
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

    # Split the data into training and validation sets
    train, valid = h2o_df.split_frame(ratios=[0.8], seed=42)

    #Define the input features and target variable      
    features = [column for column in column_names if column != 'recovery_duration_minutes']  
    print("\nfeatures:\n")
    print(features)

    target = "recovery_duration_minutes" 
    print("\ntarget:\n")
    print(target)

    # Insert a conditional statement that will train the correct model
    if Model == 'Gradient Boosting Estimator':
        print("Entered the Gradient Boosting Estimator training block!!!")
        #Create an instance of the H2OGradientBoostingEstimator and specify the model parameters:
        model = H2OGradientBoostingEstimator(ntrees=100, max_depth=5, seed=42)

    elif Model == 'Generalized Linear Estimator':
        print("Entered the Generalized Linear Estimator training block!!!")
        #Create an instance of the ... and specify the model parameters:
        model = H2OGeneralizedLinearEstimator()

    #Train the model:
    model.train(x=features, y=target, training_frame=train, validation_frame=valid)

    # Evaluate the model
    performance = model.model_performance(valid)
    mse = round(performance.mse(), 2)
    rmse = round(performance.rmse(), 2)
    mae = round(performance.mae(), 2)
    rmsle = round(performance.rmsle(), 2)
    mean_residual_deviance = round(performance.mean_residual_deviance(), 2)

    # Save the mertrics into a dictionary
    metrics = {
        "MSE": mse,
        "RMSE": rmse,
        "MAE": mae,
        "RMSLE": rmsle,
        "MRD": mean_residual_deviance
    }

    print("\nmetrics:\n")
    print(metrics)

    # Create the full model path 
    model_path = os.path.join("C:/Users/erwee/Desktop/Models.pkl")

    # # Remove the previous model file if it exists
    # if os.path.exists(model_path):
    #     os.remove(model_path)

    # Save the new model to the specified path
    model_path = h2o.save_model(model=model, path=model_path)
    print("Model saved to:", model_path)

    return metrics






