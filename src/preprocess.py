import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the raw CSV tracked by DVC
df = pd.read_csv('insurance_data.csv')

# ------------------------------------------------------------
# Encode categorical columns (adjust list as needed)
# ------------------------------------------------------------
categorical_cols = ['Gender', 'Province', 'VehicleType']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Write the cleaned data that downstream stages will consume
df.to_csv('clean_data.csv', index=False)
print(' clean_data.csv created')
