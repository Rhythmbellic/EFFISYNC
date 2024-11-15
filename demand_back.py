import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from datetime import datetime

class TCNModel(nn.Module):
    def __init__(self, input_size):
        super(TCNModel, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=input_size, out_channels=64, kernel_size=3, padding=2, dilation=2)
        self.conv2 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=2, dilation=2)
        self.fc1 = nn.Linear(64, 50)
        self.fc2 = nn.Linear(50, 1)

    def forward(self, x):
        x = x.permute(0, 2, 1)  # Change shape to [batch, channels, sequence_length]
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.mean(dim=2)  # Global Average Pooling across the sequence length
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

def inference_pipeline(input_data_dict):
    # Model and device setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define the preprocessing function for inference
    def preprocess_for_inference(input_data_dict):
        max_values = {
            'product_id': 7,
            'price': 695,
            'customer_brand': 5,
            'season': 4,
            'discount': 50,
            'current_month': 12,
            'model_age_days': 365
        }
        
        # Set default values for missing inputs
        input_data_dict['product_id'] = input_data_dict.get('product_id', max_values['product_id'])
        input_data_dict['price'] = input_data_dict.get('price', max_values['price'])
        input_data_dict['customer_brand'] = input_data_dict.get('customer_brand', max_values['customer_brand'])
        input_data_dict['season'] = input_data_dict.get('season', max_values['season'])
        input_data_dict['discount'] = input_data_dict.get('discount', max_values['discount'])
        input_data_dict['current_month'] = input_data_dict.get('current_month', max_values['current_month'])
        
        try:
            product_launch = pd.to_datetime(input_data_dict.get('product_launch', '2024-12-31'))
        except Exception as e:
            print(f"Error parsing product launch date, using max date: {e}")
            product_launch = pd.to_datetime('2024-12-31')

        # Load mappings
        try:
            product_id_mapping = pd.read_csv(r"product_id_mapping.csv")
            customer_brand_mapping = pd.read_csv(r"customer_brand_mapping.csv")
            season_mapping = pd.read_csv(r'season_mapping.csv')
            selling_month_mapping = pd.read_csv(r'selling_month_mapping.csv')
        except Exception as e:
            print(f"Error loading mapping files: {e}")
            return None
        
        # Map categorical values
        try:
            product_id_dict = dict(zip(product_id_mapping['product_id'], product_id_mapping['mapping']))
            customer_brand_dict = dict(zip(customer_brand_mapping['customer_brand'], customer_brand_mapping['mapping']))
            season_dict = dict(zip(season_mapping['season'], season_mapping['mapping']))
            selling_month_dict = dict(zip(selling_month_mapping['selling_month'], selling_month_mapping['mapping']))
        except KeyError as e:
            print(f"Missing expected columns in mapping files: {e}")
            return None
        
        # Build the input data dictionary with mappings
        input_data = {
            'product_id': product_id_dict.get(input_data_dict['product_id'], max_values['product_id']),
            'price': input_data_dict['price'],
            'customer_brand': customer_brand_dict.get(input_data_dict['customer_brand'], max_values['customer_brand']),
            'season': season_dict.get(input_data_dict['season'], max_values['season']),
            'discount': input_data_dict['discount'],
            'current_month': selling_month_dict.get(input_data_dict['current_month'], max_values['current_month']),
            'model_age_days': max_values['model_age_days']
        }
        
        # Convert input data to DataFrame for normalization
        df = pd.DataFrame([input_data])
        
        # Normalize each column
        for column in df.columns:
            if df[column].dtype != 'object':
                max_value = max_values[column]
                df[column] = df[column] / max_value if max_value != 0 else 0
                
        return df  # Return the DataFrame

    def load_model(input_size):
        try:
            model = TCNModel(input_size=input_size).to(device)
            model.load_state_dict(torch.load(r"best_tcn_model.pth", weights_only=True))
            model.eval()
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def predict(model, X_inference_tensor):
        try:
            with torch.no_grad():
                X_inference_tensor = X_inference_tensor.unsqueeze(1)
                predictions = model(X_inference_tensor)
            return predictions.squeeze()
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None

    # Preprocess data
    df_inference = preprocess_for_inference(input_data_dict)
    if df_inference is None:
        return

    X_inference_tensor = torch.tensor(df_inference.values, dtype=torch.float32).to(device)
    
    # Load the model
    input_size = X_inference_tensor.shape[1]
    model = load_model(input_size)
    if model is None:
        return

    # Perform prediction
    predictions = predict(model, X_inference_tensor)
    if predictions is None:
        return

    # Adjust prediction scaling
    final_predictions = predictions * 200  # Adjust scale factor as needed
    print("Predictions:", final_predictions)
    return final_predictions
    
import pandas as pd

# Define the month-to-season mapping with correct seasons: winter, spring, summer, autumn
month_to_season = {
    "January": "winters", "February": "winters", "March": "spring", "April": "spring", 
    "May": "spring", "June": "summers", "July": "summers", "August": "summers", 
    "September": "autumns", "October": "autumns", "November": "autumns", "December": "winters"
}

def create_input_data_dict(input_dict, csv_path):
    # Load the CSV data
    df = pd.read_csv(csv_path)

    # Fetch product-specific details
    product = input_dict["product_id"]
    brand = input_dict["customer_brand"]
    
    # Filter based on product_id and customer_brand
    product_row = df[(df['product'] == product) & (df['brand'] == brand)]
    
    if product_row.empty:
        raise ValueError("No matching product or brand found in CSV file.")
    
    # Extract price and launch date from the CSV row
    price = product_row.iloc[0]['price']
    product_launch = product_row.iloc[0]['launch_date']

    # Prepare the input data dictionary with additional fields
    input_data_dict = {
        "product_id": product,
        "price": price,
        "customer_brand": brand,
        "season": month_to_season[input_dict["current_month"]],
        "discount": input_dict["discount"],
        "current_month": input_dict["current_month"],
        "product_launch": product_launch
    }
    
    return input_data_dict

# Example usage:
input_dict = {
    "product_id": 'Reading light',
    "customer_brand": 'Porsche',
    "discount": 10,
    "current_month": "May"
}

csv_path = r"brands_products.csv"  # replace with your CSV file path
# Correct the call to the inference pipeline
output_dict = create_input_data_dict(input_dict, csv_path)
print(output_dict)

# Assuming 'a' is your tensor in CUDA
a=inference_pipeline(output_dict)
prediction_value = a.cpu().item()  # Moves the tensor to CPU and extracts the value as a Python scalar
prediction_float = round(prediction_value)
print(prediction_float)

