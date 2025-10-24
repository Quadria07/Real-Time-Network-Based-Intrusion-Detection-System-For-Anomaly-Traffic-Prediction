import joblib
import pandas as pd

def main():
    
    model = joblib.load('Models/isolation_forest_model.pkl')

   
    new_data_preprocessed = pd.read_csv('Data/extracted_new_features.csv')

    
    training_features = ['src_port', 'dst_port', 'length', 'src_ip_bytes', 'dst_ip_bytes']
    new_data_preprocessed = new_data_preprocessed[training_features]

    # Predict anomalies
    predicted_anomalies = model.predict(new_data_preprocessed)

    # Create a DataFrame with predicted anomalies and original data
    predicted_data = new_data_preprocessed.copy()
    predicted_data['predicted_anomaly'] = predicted_anomalies

    
    predicted_data.to_csv('Data/predicted_data_with_anomalies.csv', index=False)

   
    if predicted_anomalies.sum() == 0:
        print("No anomalies predicted in the new data.")
    else:
        print("Predicted anomalies in the new data:")
        print(predicted_data[predicted_data['predicted_anomaly'] == -1])

if __name__ == "__main__":
    main()
