import pandas as pd
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import joblib
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB configuration using environment variables
mongo_uri = os.environ.get('MONGO_URI')  # Set the MONGO_URI environment variable
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Replace the placeholder with your Atlas connection string
uri = os.environ.get('MONGO_CLIENT_URI')  # Set the MONGO_CLIENT_URI environment variable

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Load the trained model
model = joblib.load('final_model.joblib')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json


        required_features = [
            'NrSiblings', 'ReadingScore', 'WritingScore',
            'Gender_male', 'EthnicGroup_group A', 'EthnicGroup_group B',
            'EthnicGroup_group C', 'EthnicGroup_group D', 'EthnicGroup_group E',
            'LunchType_standard', 'TestPrep_completed', 'TestPrep_none',
            'ParentMaritalStatus_divorced', 'ParentMaritalStatus_married',
            'ParentMaritalStatus_single', 'ParentMaritalStatus_widowed',
            'TransportMeans_private', 'TransportMeans_school_bus', 'LinguisticScore'
        ]

        # Check if all required features are present
        if not all(feature in data for feature in required_features):
            return jsonify({'error': 'Missing features'}), 400

        features = [data[feature] for feature in required_features]
        features_df = pd.DataFrame([features], columns=required_features)
        prediction = model.predict(features_df)
        print(prediction)


        # Save prediction to MongoDB
        client['predictions']['pred'].insert_one({'features': data, 'prediction': prediction[0]})

        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chart/line-scores', methods=['GET'])
def line_scores_chart_data():
    try:
        db = client['predictions']['dataset']
        query_result = db.find({}, {'MathScore': 1, 'ReadingScore': 1, 'WritingScore': 1, '_id': 0})

        # Assuming the scores are individual records and you want to plot them as they are
        math_scores = [doc['MathScore'] for doc in query_result]
        reading_scores = [doc['ReadingScore'] for doc in query_result]
        writing_scores = [doc['WritingScore'] for doc in query_result]

        chart_data = {
            'labels': list(range(len(math_scores))),  # Assuming each record is a distinct data point
            'datasets': [
                {
                    'label': 'Math Score',
                    'data': math_scores,
                    'borderColor': '#42A5F5',  # Example color, replace with your own
                    'fill': False
                }, 
                {
                    'label': 'Reading Score',
                    'data': reading_scores,
                    'borderColor': '#66BB6A',  # Example color, replace with your own
                    'fill': False
                },
                {
                    'label': 'Writing Score',
                    'data': writing_scores,
                    'borderColor': '#FFA726',  # Example color, replace with your own
                    'fill': False
                }
            ]
        }

        return jsonify(chart_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/get_data', methods=['GET'])
def get_data():
    try:
        # Connect to the database
        db = client['predictions']['dataset']

        # Fetch all documents from the collection
        query_result = db.find()

        # Convert query result to a list of dictionaries
        data_list = [doc for doc in query_result]

        # Handle non-UTF-8 encodable data
        def handle_encoding(value):
            if isinstance(value, str):
                return value.encode('utf-8', 'replace').decode('utf-8')
            return value

        data_list = [{k: handle_encoding(v) for k, v in doc.items()} for doc in data_list]

        # Convert list to DataFrame
        data_df = pd.DataFrame(data_list)

        # Convert DataFrame to JSON
        data_json = json_util.dumps(data_df.to_dict(orient='records'))
        return jsonify({'data': data_json})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)
