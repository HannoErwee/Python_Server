from flask import Flask, request
from training import train_model
from inference import make_prediction
import json

app = Flask(__name__)


@app.route('/analysis', methods=['POST'])
def handle_analysis():
    Body = request.json  # Assuming JSON payload
    print("Request Body: ", Body)
    RequestType = Body['type']
    print("Request type: ", RequestType)
    Model = Body['model']
    print("Model: ", Model)

    # TRAINING REQUEST
    if RequestType == 'TRAINING':
        print("\nNEW TRAINING REQUEST\n")
        # Train the ML model and get the model parameters back
        metrics_dictionary = train_model(Model) # Pass the model in
        Response = json.dumps(metrics_dictionary)
        print("Response: ", Response)

    # INFERENCE REQUEST
    elif RequestType == 'INFERENCE':
        print("\nNEW INFERENCE REQUEST\n")
        # Fetch the prediction
        prediction_dictionary = make_prediction()
        Response = json.dumps(prediction_dictionary)

    # BAD REQUEST
    else:
        print("\nUNKNOWN REQUEST TYPE!!!\n")
        Response = "NOT A VALID REQUEST..."


    return Response


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
