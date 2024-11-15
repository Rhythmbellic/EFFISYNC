import pandas as pd

def resource_check_with_time(requirements_csv, availability_csv, demands_csv, output_csv):
    # Constants
    hours_per_day = 12
    working_days_per_month = 28
    
    # Read the CSV files into DataFrames
    requirements = pd.read_csv(requirements_csv,encoding='cp1252')
    availability = pd.read_csv(availability_csv,encoding='cp1252')
    demands = pd.read_csv(demands_csv,encoding='cp1252')

    # Initialize a dictionary to hold total resource demands
    total_demands = {col: 0 for col in availability.columns}

    # Loop through each row in the requirements CSV to calculate the resource demand per product
    for idx, req_row in requirements.iterrows():
        brand = req_row['brand']
        product = req_row['product']
        time_required_per_unit = req_row['time']  # Time required per unit of the product
        
        # Find the corresponding demand from the demand CSV
        product_demand = demands[(demands['brand'] == brand) & (demands['product'] == product)]['demand'].values
        if len(product_demand) == 0:
            continue  # Skip if no demand found for this product
        product_demand = product_demand[0]  # Get the demand value

        # Calculate the total resource demand for this product considering the unit time
        for resource in availability.columns:
            # Multiply the resource requirement by the product demand and the time factor (hours per day * days per month)
            resource_per_product = req_row[resource] * product_demand
            resource_per_product_time = resource_per_product * time_required_per_unit * hours_per_day * working_days_per_month
            total_demands[resource] += resource_per_product_time

    # Now, compare the calculated total demands with available resources
    results = []
    for resource in availability.columns:
        available = availability[resource].iloc[0]  # Get the available quantity
        total_demand = total_demands[resource]  # Get the total demand for this resource
        resource_difference = available - total_demand  # Calculate the difference (positive: extra, negative: shortage)
        results.append([resource, available, total_demand, resource_difference])

    # Convert the results into a DataFrame
    result_df = pd.DataFrame(results, columns=["Resource", "Available", "Total Demand", "Difference"])

    # Write the result to a CSV file
    result_df.to_csv(output_csv, index=False)

# Example usage
requirements_csv = r"job_resources.csv"  # Path to resource requirements CSV
availability_csv = r"Avaialible_resource.csv"  # Path to current resource availability CSV
demands_csv = r"demand.csv"          # Path to object demands CSV
output_csv = r"out.csv" # Output file path

resource_check_with_time(requirements_csv, availability_csv, demands_csv, output_csv)