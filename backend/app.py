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
from collections import Counter
from collections import defaultdict

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


@app.route('/api/ethnic-group-data', methods=['GET'])
def ethnic_group_data():
    try:
        db = client['predictions']['dataset']
        query_result = db.find({}, {
            'EthnicGroup_group A': 1, 'EthnicGroup_group B': 1, 'EthnicGroup_group C': 1,
            'EthnicGroup_group D': 1, 'EthnicGroup_group E': 1, '_id': 0
        })

        # Initialize counters for each ethnic group
        ethnic_group_counters = {
            'EthnicGroup_group A': Counter(),
            'EthnicGroup_group B': Counter(),
            'EthnicGroup_group C': Counter(),
            'EthnicGroup_group D': Counter(),
            'EthnicGroup_group E': Counter()
        }

        for doc in query_result:
            for group in ethnic_group_counters.keys():
                if doc.get(group, False):
                    ethnic_group_counters[group].update(doc)

        # Convert Counter objects to dictionaries
        ethnic_group_data = {group: dict(counter) for group, counter in ethnic_group_counters.items()}

        return jsonify(ethnic_group_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/api/line-scores', methods=['GET'])
def line_scores_chart_data():
    try:
        db = client['predictions']['dataset']
        query_result = db.find({}, {'MathScore': 1, 'ReadingScore': 1, 'WritingScore': 1, '_id': 0})

        # Check if query returned any documents
        query_result_list = list(query_result)
        if not query_result_list:
            print("No documents found in the database.")
            return jsonify({'error': 'No data available'}), 404

        # Extract scores and count occurrences
        math_score_counts = Counter(doc.get('MathScore', 0) for doc in query_result_list)
        reading_score_counts = Counter(doc.get('ReadingScore', 0) for doc in query_result_list)
        writing_score_counts = Counter(doc.get('WritingScore', 0) for doc in query_result_list)

        # Convert Counter objects to dictionaries
        math_scores_dict = dict(math_score_counts)
        reading_scores_dict = dict(reading_score_counts)
        writing_scores_dict = dict(writing_score_counts)

        chart_data = {
            'labels': ['Math', 'Reading', 'Writing'],
            'datasets': [
                {
                    'label': 'Math Score',
                    'data': math_scores_dict,
                    'borderColor': '#42A5F5',
                    'fill': False
                },
                {
                    'label': 'Reading Score',
                    'data': reading_scores_dict,
                    'borderColor': '#66BB6A',
                    'fill': False
                },
                {
                    'label': 'Writing Score',
                    'data': writing_scores_dict,
                    'borderColor': '#FFA726',
                    'fill': False
                }
            ]
        }

        print(chart_data)
        return jsonify(chart_data)
    except Exception as e:
        print(f"An error occurred: {e}")
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


@app.route('/api/ethnic-grade-distribution', methods=['GET'])
def ethnic_grade_distribution():
    try:
        db = client['predictions']['dataset']
        query_result = db.find({}, {
            'MathScore': 1, 'ReadingScore': 1, 'WritingScore': 1,
            'EthnicGroup_group A': 1, 'EthnicGroup_group B': 1,
            'EthnicGroup_group C': 1, 'EthnicGroup_group D': 1,
            'EthnicGroup_group E': 1, '_id': 0
        })

        # Initialize data structures
        grade_distribution = {
            'EthnicGroup_group A': defaultdict(int),
            'EthnicGroup_group B': defaultdict(int),
            'EthnicGroup_group C': defaultdict(int),
            'EthnicGroup_group D': defaultdict(int),
            'EthnicGroup_group E': defaultdict(int)
        }

        # Process each document
        for doc in query_result:
            for group in grade_distribution:
                if doc.get(group, False):
                    # Ensure the scores are integers
                    math_score = int(doc.get('MathScore', 0))
                    reading_score = int(doc.get('ReadingScore', 0))
                    writing_score = int(doc.get('WritingScore', 0))

                    grade_distribution[group]['MathScore'][math_score] += 1
                    grade_distribution[group]['ReadingScore'][reading_score] += 1
                    grade_distribution[group]['WritingScore'][writing_score] += 1

        # Convert defaultdict to regular dict for JSON serialization
        for group in grade_distribution:
            for subject in grade_distribution[group]:
                grade_distribution[group][subject] = dict(grade_distribution[group][subject])

        return jsonify(grade_distribution)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
