import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

# Load the weather data
weather = pd.read_csv('C:\\Users\\ossri\\Downloads\\Bengaluru 2010-2022.csv')

# Ensure columns are lowercase for uniformity
weather.columns = weather.columns.str.lower()

# Check for missing values
print("Missing values in each column:")
print(weather.isnull().sum())

# Convert 'time' column to datetime format and extract components
weather['time'] = pd.to_datetime(weather['time'])
weather['year'] = weather['time'].dt.year
weather['month'] = weather['time'].dt.month
weather['day'] = weather['time'].dt.day

# Fill missing rows with the values from the previous row
weather.fillna(method='ffill', inplace=True)

# Remove duplicate rows
weather.drop_duplicates(inplace=True)

weather.to_csv('C:\\Users\\ossri\\Downloads\\Bengaluru_weather.csv', index=False)

# Create lag features (e.g., previous year's rainfall)
weather['prcp_lag1'] = weather['prcp'].shift(365)  # Lag of one year (365 days)

# Drop rows with missing lag values
weather.dropna(inplace=True)

# Define features (X) and target (y)
X = weather[['tavg', 'tmin', 'tmax', 'month', 'day', 'prcp_lag1']]
y = weather['prcp']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Ridge Regression model
model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Predict rainfall for the next year
# Generate future data for prediction
next_year_data = weather[weather['year'] == weather['year'].max()].copy()
next_year_data['year'] = next_year_data['year'] + 1  # Increment year

# Ensure lag values match the length of next_year_data
available_lag_length = len(next_year_data)
next_year_data['prcp_lag1'] = weather['prcp'].iloc[-available_lag_length:].values  # Adjust to available length

# Select necessary features for prediction
next_year_data = next_year_data[['tavg', 'tmin', 'tmax', 'month', 'day', 'prcp_lag1']]

# Predict rainfall for the next year
predicted_rainfall = model.predict(next_year_data)
next_year_data['predicted_prcp'] = predicted_rainfall

# Aggregate daily predictions to monthly totals
monthly_rainfall = next_year_data.groupby('month')['predicted_prcp'].sum().reset_index()

# Display monthly results
print("\nPredicted Monthly Rainfall for Next Year:")
print(monthly_rainfall)

# Plot the predicted monthly rainfall as a line graph
plt.figure(figsize=(10, 6))
plt.plot(monthly_rainfall['month'], monthly_rainfall['predicted_prcp'], marker='o', label='Predicted Rainfall')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.title('Predicted Monthly Rainfall for Next Year')
plt.legend()
plt.grid(True)
plt.show()
print(weather.groupby('year')['month'].nunique())