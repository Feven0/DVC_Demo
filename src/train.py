import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the cleaned data produced by the preprocessing stage
df = pd.read_csv('clean_data.csv')

# ------------------------------------------------------------
# Define features and target – adjust column names if they differ
# ------------------------------------------------------------
features = ['Age', 'Gender', 'Province', 'VehicleType', 'AnnualIncome',
            'RiskScore', 'AnnualPremium', 'Deductible', 'NCD', 'PastClaims']
X = df[features]
y = df['Claimed']

# Train a simple RandomForest classifier
model = RandomForestClassifier(n_estimators=100,
                               max_depth=8,
                               random_state=42)
model.fit(X, y)

# Save the trained model artefact for downstream stages or deployment
joblib.dump(model, 'model.pkl')
print(' model.pkl saved')
