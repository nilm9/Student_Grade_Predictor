import joblib
import numpy as np
from flask import Flask, jsonify

def get_feature_importance_data():
    try:
        # Load the trained Gradient Boosting model
        model = joblib.load('final_model.joblib')

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

app = Flask(__name__)

@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    feature_importance_data = get_feature_importance_data()
    if feature_importance_data:
        return jsonify({'feature_importance': feature_importance_data})
    else:
        return jsonify({'error': 'Unable to retrieve feature importance data'}), 500

if __name__ == '__main__':
    app.run(debug=True)
