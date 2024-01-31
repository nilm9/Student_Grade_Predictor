from flask import Flask, request, jsonify
import numpy as np
from scipy.optimize import linprog
import joblib

app = Flask(__name__)

# Load your trained model (ensure the model is compatible with this type of analysis)
model = joblib.load('path_to_your_trained_model.joblib')

def counterfactual_analysis(model, current_features, desired_prediction):
    current_pred = model.predict([current_features])[0]
    gap = desired_prediction - current_pred

    coeffs = model.coef_
    c = np.ones_like(current_features)
    A_ub = -coeffs.reshape(1, -1)
    b_ub = -gap

    bounds = [(None, None) for _ in current_features]

    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        # Calculate the required changes
        required_changes = result.x
        return required_changes
    else:
        raise ValueError('Optimization failed')

@app.route('/api/counterfactual-analysis', methods=['POST'])
def perform_counterfactual_analysis():
    try:
        content = request.json
        current_features = np.array(content['current_features'])
        desired_prediction = content['desired_prediction']

        changes_needed = counterfactual_analysis(model, current_features, desired_prediction)
        return jsonify({'required_changes': changes_needed.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 501

if __name__ == '__main__':
    app.run(debug=True)
