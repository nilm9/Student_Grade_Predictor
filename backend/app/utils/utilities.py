import pandas as pd


def normalize_data(data):
    min_val = min(data.values())
    max_val = max(data.values())
    return {k: (v - min_val) / (max_val - min_val) if max_val - min_val else 0 for k, v in data.items()}


def process_data(df, feature):
    # Process the data based on the feature
    # This is a placeholder logic; implement according to your dataset
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
