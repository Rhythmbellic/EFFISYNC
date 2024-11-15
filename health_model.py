import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle

mach_heal= pd.read_csv(r"machine_health_data.csv")

X=mach_heal.drop("machine_health",axis=1)
y=mach_heal["machine_health"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
y_scaled = y/100

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.25, random_state=42)

model_MH = LinearRegression()
model_MH.fit(X_train, y_train)

# Predict on the test set
y_pred = model_MH.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)

def preprocess_and_predict(model_path, data_path):
  # Read data
  mach_heal = pd.read_csv(data_path)

  # Separate features
  X = mach_heal.drop(["Machine"],axis=1)

  # Preprocess data
  scaler = MinMaxScaler()
  X_scaled = scaler.fit_transform(X)

  with open(model_path, 'rb') as file:
    model_MH = pickle.load(file)

  # Predict on the new data
  y_pred = model_MH.predict(X_scaled)

  return y_pred