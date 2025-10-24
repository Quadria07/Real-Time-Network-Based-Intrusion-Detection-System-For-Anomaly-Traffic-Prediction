import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, roc_curve, auc
import matplotlib.pyplot as plt
import joblib

# Load the synthetic labeled dataset
labeled_data = pd.read_csv('synthetic_labeled_data.csv')

# Split features and labels
X = labeled_data.drop(columns=['label'])  # Features
y_true = labeled_data['label']  # True labels

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Retrain the Isolation Forest model with appropriate contamination
contamination_rate = y_true.mean()  # Proportion of anomalies
model = IsolationForest(n_estimators=100, contamination=contamination_rate, random_state=42)
model.fit(X_scaled)

# Save the retrained model
joblib.dump(model, 'Models/isolation_forest_model_retrained.pkl')

# Predict anomalies
y_pred = model.predict(X_scaled)
y_pred = [0 if y == 1 else 1 for y in y_pred]

# Evaluate the model
conf_matrix = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:\n", conf_matrix)

precision = precision_score(y_true, y_pred, average='binary')
recall = recall_score(y_true, y_pred, average='binary')
f1 = f1_score(y_true, y_pred, average='binary')
accuracy = accuracy_score(y_true, y_pred)
fpr, tpr, _ = roc_curve(y_true, y_pred)
roc_auc = auc(fpr, tpr)

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"Accuracy: {accuracy:.2f}")
print(f"AUC: {roc_auc:.2f}")

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
