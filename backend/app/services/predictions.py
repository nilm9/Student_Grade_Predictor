from ..utils.utilities import  process_data
import pandas as pd
from flask import  request
from flask import Blueprint
from bson import json_util

from collections import Counter
from collections import defaultdict
import joblib
from flask import Flask, jsonify
from traceback import format_exc
import os
from .config import  get_mongo_client


BASE_COLORS = {
    'blue': '#42A5F5',
    'green': '#66BB6A',
    'orange': '#FFA726',
}

model_path = os.path.join(os.path.dirname(__file__), 'final_model.joblib')
model = joblib.load(model_path)


client = get_mongo_client()

predictions_blueprint = Blueprint('predictions', __name__)

@predictions_blueprint.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        required_features = [
            'ParentEduc', 'PracticeSport', 'IsFirstChild', 'NrSiblings',
            'WklyStudyHours', 'Gender_male', 'EthnicGroup_group A',
            'EthnicGroup_group B', 'EthnicGroup_group C', 'EthnicGroup_group D',
            'EthnicGroup_group E', 'LunchType_standard', 'TestPrep_completed',
            'TestPrep_none', 'ParentMaritalStatus_divorced',
            'ParentMaritalStatus_married', 'ParentMaritalStatus_single',
            'ParentMaritalStatus_widowed', 'TransportMeans_private',
            'TransportMeans_school_bus'
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


@predictions_blueprint.route('/api/ethnic-group-data', methods=['GET'])
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



@predictions_blueprint.route('/api/line-scores', methods=['GET'])
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
                    'borderColor': BASE_COLORS['blue'],
                    'fill': False
                },
                {
                    'label': 'Reading Score',
                    'data': reading_scores_dict,
                    'borderColor': BASE_COLORS['green'],
                    'fill': False
                },
                {
                    'label': 'Writing Score',
                    'data': writing_scores_dict,
                    'borderColor': BASE_COLORS['orange'],
                    'fill': False
                }
            ]
        }

        print(chart_data)
        return jsonify(chart_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@predictions_blueprint.route('/api/get_data', methods=['GET'])
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



@predictions_blueprint.route('/api/grade-distribution', methods=['GET'])
def grade_distribution():
    try:
        grade_counts = defaultdict(int)

        collection = client['predictions']['dataset']

        # Fetch grades from the collection and count each grade occurrence
        for student in collection.find({}, {'grade': 1, '_id': 0}):
            grade_counts[student['grade']] += 1

        # Calculate total number of grades to determine percentages
        total_grades = sum(grade_counts.values())

        # Calculate percentage for each grade
        grade_percentages = {grade: (count / total_grades) * 100 for grade, count in grade_counts.items()}

        return jsonify(grade_percentages)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@predictions_blueprint.route('/api/radar-chart-data', methods=['GET'])
def radar_chart_data():
    try:
        db = client['predictions']['dataset']

        # Aggregation pipeline to compute averages for more features
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avgPracticeSport": {"$avg": "$PracticeSport"},
                    "avgWklyStudyHours": {"$avg": "$WklyStudyHours"},
                    "avgOverallScore": {"$avg": "$Overall_Score"},
                    "avgMathScore": {"$avg": "$MathScore"},
                    "avgReadingScore": {"$avg": "$ReadingScore"},
                    "avgParentEduc": {"$avg": "$ParentEduc"}
                }
            }
        ]

        result = db.aggregate(pipeline)
        data = next(result, None)

        if data:
            # Scale scores from 0-100 to 0-10
            data['avgMathScore'] /= 10
            data['avgReadingScore'] /= 10
            data['avgOverallScore'] /= 10

            # Remove the '_id' field
            data.pop('_id', None)

            # Convert the averages to a suitable format for the radar chart
            radar_data = {
                'labels': ['Practice Sport', 'Weekly Study Hours', 'Overall Score', 'Math Score', 'Reading Score', 'Parent Education'],
                'datasets': [
                    {
                        'label': 'Average',
                        'data': [data['avgPracticeSport'], data['avgWklyStudyHours'], data['avgOverallScore'],
                                 data['avgMathScore'], data['avgReadingScore'], data['avgParentEduc']],
                        'fill': True,
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointBackgroundColor': 'rgb(255, 99, 132)',
                        'pointBorderColor': '#fff',
                        'pointHoverBackgroundColor': '#fff',
                        'pointHoverBorderColor': 'rgb(255, 99, 132)'
                    }
                ]
            }
            return jsonify(radar_data)

        else:
            return jsonify({'error': 'No data available'}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

def process_data(df, feature):

    if feature in df.columns:
        processed_data = df[feature].value_counts().to_dict()
    else:
        # Handle grouped features (like 'Ethnic Groups')
        grouped_features = {
            'Ethnic Groups': ['EthnicGroup_group A', 'EthnicGroup_group B', 'EthnicGroup_group C',
                              'EthnicGroup_group D', 'EthnicGroup_group E'],
            'Test Preparation': ['TestPrep_completed', 'TestPrep_none'],
            'Parent Marital Status': ['ParentMaritalStatus_divorced', 'ParentMaritalStatus_married',
                                      'ParentMaritalStatus_single', 'ParentMaritalStatus_widowed'],
            'Transport Means': ['TransportMeans_private', 'TransportMeans_school_bus']
        }

        if feature in grouped_features:
            processed_data = df[grouped_features[feature]].apply(pd.Series.value_counts).fillna(0).sum(axis=1).to_dict()
        else:
            processed_data = {}

    return processed_data

@predictions_blueprint.route('/api/data_feature', methods=['GET'])
def get_data_feature():
    feature = request.args.get('feature')

    # Fetching data from the database
    data = list(client['predictions']['dataset'].find())

    # Converting to a pandas DataFrame
    df = pd.DataFrame(data)

    # Now df is a DataFrame and should have the 'columns' attribute
    processed_data = process_data(df, feature)
    return jsonify(processed_data)


@predictions_blueprint.route('/api/prep-data', methods=['GET'])
def prep_data():
    try:
        collection = client['predictions']['dataset']

        # Count the number of students who completed test preparation
        test_prep_completed_count = collection.count_documents({'TestPrep_completed': True})

        # Count the number of students who did not complete test preparation
        test_prep_none_count = collection.count_documents({'TestPrep_none': True})

        data = {
            'TestPrepCompleted': test_prep_completed_count,
            'TestPrepNotCompleted': test_prep_none_count
        }

        return jsonify(data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@predictions_blueprint.route('/api/multi-axis-chart-data', methods=['GET'])
def multi_axis_chart_data():
    try:
        db = client['predictions']['dataset']

        # Aggregation pipeline to group by ParentEduc and compute average Overall_Score
        pipeline = [
            {
                "$group": {
                    "_id": "$ParentEduc",
                    "avgOverallScore": {"$avg": "$Overall_Score"}
                }
            },
            {"$sort": {"_id": 1}}  # Sorting by ParentEduc
        ]

        result = db.aggregate(pipeline)
        parent_educ_scores = list(result)

        # Preparing data for the multi-axis chart
        labels = [doc['_id'] for doc in parent_educ_scores]
        overall_scores = [doc['avgOverallScore'] for doc in parent_educ_scores]

        multi_axis_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Overall Score',
                    'data': overall_scores,
                    'yAxisID': 'y-axis-1',
                    'type': 'line',  # Line chart for Overall Scores
                    'fill': False,
                    'borderColor': BASE_COLORS['blue'],
                    'pointBackgroundColor': BASE_COLORS['green'],                    'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                    'pointBorderColor': BASE_COLORS['orange'],
                    'pointBorderWidth': 2,
                    'pointHoverRadius': 5,
                    'pointHoverBackgroundColor': BASE_COLORS['orange'],
                    'pointHoverBorderColor':  BASE_COLORS['green'] ,
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 3,
                    'pointHitRadius': 10
                }
            ]
        }

        return jsonify(multi_axis_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@predictions_blueprint.route('/api/stacked-scores-by-ethnicity', methods=['GET'])
def stacked_scores_by_ethnicity():
    try:
        db = client['predictions']['dataset']
        pipeline = [
            {
                "$group": {
                    "_id": "$EthnicGroup",
                    "MathScores": {"$avg": "$MathScore"},
                    "ReadingScores": {"$avg": "$ReadingScore"},
                    "WritingScores": {"$avg": "$WritingScore"}
                }
            },
            {"$sort": {"_id": 1}}
        ]

        query_result = db.aggregate(pipeline)

        ethnic_groups = []
        math_scores = []
        reading_scores = []
        writing_scores = []

        for doc in query_result:
            ethnic_groups.append(doc['_id'])
            math_scores.append(doc['MathScores'])
            reading_scores.append(doc['ReadingScores'])
            writing_scores.append(doc['WritingScores'])

        chart_data = {
            'labels': ethnic_groups,
            'datasets': [
                {
                    'label': 'Math Score',
                    'data': math_scores,
                    'backgroundColor': BASE_COLORS['blue']
                },
                {
                    'label': 'Reading Score',
                    'data': reading_scores,
                    'backgroundColor': BASE_COLORS['green']
                },
                {
                    'label': 'Writing Score',
                    'data': writing_scores,
                    'backgroundColor': BASE_COLORS['orange']
                }
            ]
        }

        return jsonify(chart_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500


def normalize_data(data):
    min_val = min(data.values())
    max_val = max(data.values())
    return {k: (v - min_val) / (max_val - min_val) if max_val - min_val else 0 for k, v in data.items()}





@predictions_blueprint.route('/api/ethnic-grade-distribution', methods=['GET'])
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




def get_feature_importance_data():
    try:
        # Load the trained Gradient Boosting model
        model = joblib.load(model_path)

        # Extract feature importances
        importances = model.feature_importances_

        required_features = [
            "ParentEduc", "PracticeSport", "IsFirstChild", "NrSiblings", "WklyStudyHours",
            "MathScore", "ReadingScore", "WritingScore",
            "Gender_male", "EthnicGroup_group A", "EthnicGroup_group B", "EthnicGroup_group C",
            "EthnicGroup_group D", "EthnicGroup_group E", "LunchType_standard", "TestPrep_completed",
            "TestPrep_none", "ParentMaritalStatus_divorced", "ParentMaritalStatus_married",
            "ParentMaritalStatus_single", "ParentMaritalStatus_widowed", "TransportMeans_private",
            "TransportMeans_school_bus"
        ]

        # Map feature names to their importances and sort by importance
        importance_dict = dict(zip(required_features, importances))
        sorted_importances = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

        return sorted_importances

    except Exception as e:
        print(f"Error in getting feature importance data: {e}")
        return None


@predictions_blueprint.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    feature_importance_data = get_feature_importance_data()
    if feature_importance_data:
        return jsonify({'feature_importance': feature_importance_data})
    else:
        return jsonify({'error': 'Unable to retrieve feature importance data'}), 500


def counterfactual_analysis(model, current_features, desired_prediction, max_increase_hours, required_features):
    weekly_study_hours_index = required_features.index("WklyStudyHours")
    original_hours = current_features[weekly_study_hours_index]
    max_hours = original_hours + max_increase_hours

    # Convert current_features list to DataFrame
    current_features_df = pd.DataFrame([current_features], columns=required_features)

    while current_features[weekly_study_hours_index] < max_hours:
        # Use the DataFrame for prediction
        current_pred = model.predict(current_features_df)[0]
        if current_pred >= desired_prediction:
            break

        current_features[weekly_study_hours_index] += 1  # Increment weekly study hours
        # Update the DataFrame with the new value
        current_features_df.at[0, "WklyStudyHours"] = current_features[weekly_study_hours_index]

    return current_features


@predictions_blueprint.route('/api/counterfactual-analysis', methods=['POST'])
def perform_counterfactual_analysis():
    try:
        print("debugging...")
        content = request.json
        current_features_dict = content['current_features']
        desired_prediction = float(content['desired_prediction'])
        max_increase_hours = content.get('max_increase_hours', 10)  # Default to 10 hours if not specified

        required_features = [
            "ParentEduc", "PracticeSport", "IsFirstChild", "NrSiblings", "WklyStudyHours",
            "Gender_male", "EthnicGroup_group A", "EthnicGroup_group B", "EthnicGroup_group C",
            "EthnicGroup_group D", "EthnicGroup_group E", "LunchType_standard", "TestPrep_completed",
            "TestPrep_none", "ParentMaritalStatus_divorced", "ParentMaritalStatus_married",
            "ParentMaritalStatus_single", "ParentMaritalStatus_widowed", "TransportMeans_private",
            "TransportMeans_school_bus"
        ]
        current_features = [float(current_features_dict[feature]) for feature in required_features]

        counterfactual = counterfactual_analysis(model, current_features, desired_prediction, max_increase_hours,
                                                 required_features)

        return jsonify({'counterfactual': counterfactual})

    except Exception as e:
        print(f"Error: {e}")
        print(format_exc())  # This will print the stack trace
        return jsonify({'error': str(e)}), 500




@predictions_blueprint.route('/api/study-hours-distribution', methods=['GET'])
def study_hours_distribution():
    try:
        collection = client['predictions']['dataset']

        # Aggregating counts of weekly study hours
        pipeline = [
            {"$group": {"_id": "$WklyStudyHours", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}  # Sorting by weekly study hours
        ]

        query_result = collection.aggregate(pipeline)

        # Preparing data for the bar chart
        study_hours_data = defaultdict(int)
        for record in query_result:
            study_hours = record['_id']
            count = record['count']
            study_hours_data[study_hours] = count

        return jsonify(study_hours_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500






@predictions_blueprint.route('/api/parent-education-distribution', methods=['GET'])
def parent_education_distribution():
    try:
        collection = client['predictions']['dataset']

        # Aggregating the count of each ParentEduc value
        pipeline = [
            {"$group": {"_id": "$ParentEduc", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}  # Sorting by ParentEduc value
        ]
        result = collection.aggregate(pipeline)

        # Preparing the data for the response
        distribution = {str(doc['_id']): doc['count'] for doc in result}

        return jsonify(distribution)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



