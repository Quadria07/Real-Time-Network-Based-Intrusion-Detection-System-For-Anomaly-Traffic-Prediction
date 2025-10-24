import pandas as pd
from sklearn.ensemble import IsolationForest
import logging
import joblib

def train_isolation_forest(features_file, model_file):
    logging.basicConfig(filename='model_training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    try:
        features_df = pd.read_csv(features_file)
        logging.info("Successfully read features data from CSV file.")
    except Exception as e:
        logging.error(f"Error reading features data from CSV file: {e}")
        return


    features_df = features_df.drop(columns=['src_ip', 'dst_ip', 'timestamp', 'flags'])

  
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

    try:
        model.fit(features_df)
        logging.info("Isolation Forest model training complete.")
    except Exception as e:
        logging.error(f"Error training Isolation Forest model: {e}")
        return

    try:
        joblib.dump(model, model_file)
        logging.info(f"Model saved to {model_file}.")
        print(f"Isolation Forest model training complete and saved to {model_file}")
    except Exception as e:
        logging.error(f"Error saving Isolation Forest model: {e}")

if __name__ == "__main__":
    features_file = "Data/extracted_features.csv"
    model_file = "Models/isolation_forest_model.pkl"
    train_isolation_forest(features_file, model_file)
