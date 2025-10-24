import numpy as np
import pandas as pd

# Generate synthetic data
n_samples = 1000  # Number of normal samples
n_features = 5  # Number of features (src_port, dst_port, length, src_ip_bytes, dst_ip_bytes)

# Normal data
X_normal = np.random.normal(loc=0.0, scale=1.0, size=(n_samples, n_features))

# Anomalous data
n_anomalies = 50  # Number of anomalous samples
X_anomalies = np.random.normal(loc=5.0, scale=1.0, size=(n_anomalies, n_features))

# Combine and create labels
X = np.vstack((X_normal, X_anomalies))
y = np.hstack((np.zeros(n_samples), np.ones(n_anomalies)))

# Create a DataFrame with specific feature names
df = pd.DataFrame(X, columns=['src_port', 'dst_port', 'length', 'src_ip_bytes', 'dst_ip_bytes'])
df['label'] = y

# Save to CSV
df.to_csv('synthetic_labeled_data.csv', index=False)
