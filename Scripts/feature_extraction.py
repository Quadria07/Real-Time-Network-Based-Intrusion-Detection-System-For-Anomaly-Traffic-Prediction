import pandas as pd
import logging

def extract_features(cleaned_data):
    cleaned_data['src_ip_bytes'] = cleaned_data['src_ip'].apply(len)
    cleaned_data['dst_ip_bytes'] = cleaned_data['dst_ip'].apply(len)
    return cleaned_data

def main(cleaned_data_file, features_file):
    logging.basicConfig(filename='feature_extraction.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    try:
        cleaned_data = pd.read_csv(cleaned_data_file)
        logging.info("Successfully read cleaned data from CSV file.")
    except Exception as e:
        logging.error(f"Error reading cleaned data from CSV file: {e}")
        return
    try:
        features_df = extract_features(cleaned_data)
        logging.info("Successfully extracted features from cleaned data.")
    except Exception as e:
        logging.error(f"Error extracting features from cleaned data: {e}")
        return
    try:
        features_df.to_csv(features_file, index=False)
        logging.info(f"Successfully saved extracted features to {features_file}.")
        print(f"Feature extraction complete and saved to {features_file}")
    except Exception as e:
        logging.error(f"Error saving extracted features to CSV file: {e}")

if __name__ == "__main__":
    cleaned_data_file = "Data/cleaned_new_data.csv"
    features_file = "Data/extracted_new_features.csv"
    main(cleaned_data_file, features_file)
