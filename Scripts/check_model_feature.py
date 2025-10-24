import joblib


model = joblib.load('Models/isolation_forest_model.pkl')


if hasattr(model, 'feature_names_in_'):
    print("Features used during training:", model.feature_names_in_)
else:
    print("No feature names found in the model object.")
