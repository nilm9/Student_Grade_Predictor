from flask import Blueprint
from ..services.predictions import (
    predict,
    ethnic_group_data,
    get_data_feature,
    line_scores_chart_data,
    get_data,
    grade_distribution,
    radar_chart_data,
    prep_data,
    multi_axis_chart_data,
    stacked_scores_by_ethnicity,
    ethnic_grade_distribution,
    feature_importance,
    perform_counterfactual_analysis,
    study_hours_distribution,
    parent_education_distribution
)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/predict', methods=['POST'])
def predict_route():
    return predict()

@api_blueprint.route('/ethnic-group-data', methods=['GET'])
def ethnic_group_data_route():
    return ethnic_group_data()

@api_blueprint.route('/line-scores', methods=['GET'])
def line_scores_chart_data_route():
    return line_scores_chart_data()

@api_blueprint.route('/get_data', methods=['GET'])
def get_data_route():
    return get_data()

@api_blueprint.route('/grade-distribution', methods=['GET'])
def grade_distribution_route():
    return grade_distribution()

@api_blueprint.route('/radar-chart-data', methods=['GET'])
def radar_chart_data_route():
    return radar_chart_data()

@api_blueprint.route('/data_feature', methods=['GET'])
def get_data_feature_route():
    return get_data_feature()

@api_blueprint.route('/prep-data', methods=['GET'])
def prep_data_route():
    return prep_data()

@api_blueprint.route('/multi-axis-chart-data', methods=['GET'])
def multi_axis_chart_data_route():
    return multi_axis_chart_data()

@api_blueprint.route('/stacked-scores-by-ethnicity', methods=['GET'])
def stacked_scores_by_ethnicity_route():
    return stacked_scores_by_ethnicity()

@api_blueprint.route('/ethnic-grade-distribution', methods=['GET'])
def ethnic_grade_distribution_route():
    return ethnic_grade_distribution()

@api_blueprint.route('/feature-importance', methods=['GET'])
def feature_importance_route():
    return feature_importance()

@api_blueprint.route('/counterfactual-analysis', methods=['POST'])
def perform_counterfactual_analysis_route():
    return perform_counterfactual_analysis()

@api_blueprint.route('/study-hours-distribution', methods=['GET'])
def study_hours_distribution_route():
    return study_hours_distribution()

@api_blueprint.route('/parent-education-distribution', methods=['GET'])
def parent_education_distribution_route():
    return parent_education_distribution()

# ... add the remaining routes ...
