from flask import Flask, request

app = Flask(__name__)


@app.route('/analysis', methods=['POST'])
def handle_analysis():
    data = request.json  # Assuming JSON payload
    print("data: ", data)
    # Perform analysis on the received data
    result = {'message': 'Analysis completed successfully'}
    return result


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
