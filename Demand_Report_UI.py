import streamlit as st
from demand_back import create_input_data_dict,inference_pipeline

pg_title='<p style="color:#68b6ef ; font-size:50px;text-align:center; font-family:Courier New;">Demand Report</p>'
st.markdown(pg_title, unsafe_allow_html=True)

st.divider()

# Brand Name Selection
brand_name = st.selectbox("Select Brand", ("Lamborghini", "Skoda", "Porsche","Bentley","Audi"),index=None,placeholder="Choose the Brand")

# Product Name Selection
product_name = st.selectbox("Select Product",("Headlight","Tail light","Fog light","Parking light","Indicators","Overhead light","Reading light"),index=None, placeholder="Choose a Product",)  

# Price Input
month = st.selectbox("Select Selling Month", options=('January','Februry',"March",'April','May','June','July','August','September','October','November','December'),index=None,placeholder="Choose a Month",)

# Discount Input
discount = st.number_input("Enter Discount", min_value=0.0, max_value=100.0, step=0.1)

st.divider()

# Example usage:
input_dict = {
    "product_id": product_name,
    "customer_brand": brand_name,
    "discount": discount,
    "current_month": month
}




# Button to Run Model and Show Output
if st.button("Generate Demand Report📑"):
    csv_path = r"brands_products.csv"  # replace with your CSV file path
    # Correct the call to the inference pipeline
    output_dict = create_input_data_dict(input_dict, csv_path)
    print(output_dict)

    a=inference_pipeline(output_dict)
    prediction_value = a.cpu().item()  # Moves the tensor to CPU and extracts the value as a Python scalar
    prediction_round = round(prediction_value)
    # Call your model here with the input parameters
    # Example: demand_output = model.run(product_name, brand_name, price, discount)
    demand_output = "Sample output"  # Replace with model output
    with st.container(border=True):
        t =f'<p style=font-size:20px "> Prediction: {prediction_round} Units </p>'
        st.markdown(t, unsafe_allow_html=True,help='Units may be demanded in the given month')