import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Inventory_Analysis_Back import resource_check_with_time

# Function to create a gauge chart
def create_gauge(resource_name, available, demand):
    return go.Indicator(
        mode="gauge+number",
        value=available,
        title={'text': resource_name},
        gauge={'axis': {'range': [0, max(available, demand)]},
               'bar': {'color': "darkblue"}},
        number={'suffix': " units"}
    )

def color_cells(val):
    color = ''
    if val>= 0:
        color = 'background-color: #28a745; color: black'
    else:
        color = 'background-color: #b71c1c; color: black'
    return color

# Reading Inventry Analysis
resource_data = pd.read_csv('out.csv')
resource_data.drop(index=0,inplace=True)
resource_data.drop(index=1,inplace=True)
resource_data.drop(index=2,inplace=True)
resources = resource_data.to_dict('records')

# UI 
title='<p style="color:#68b6ef ; font-size:50px ; text-align:center ; font-family:Courier New">Inventory Analysis</p>'
st.markdown(title, unsafe_allow_html=True)

st.divider()

# Analyse Button 
if st.button("Analyse Inventory"):
    requirements_csv = r"job_resources.csv"  # Path to resource requirements CSV
    availability_csv = r"Avaialible_resource.csv"  # Path to current resource availability CSV
    demands_csv = r"demand.csv" # Path to object demands CSV
    output_csv = r"out.csv" # Output file path

    resource_check_with_time(requirements_csv, availability_csv, demands_csv, output_csv)

# Creating tabs
tab1, tab2 = st.tabs(["📊 Graphs", "🗃️ Data"])

tab1.subheader('Graphs')
# Set up the subplot layout
fig = make_subplots(rows=2, cols=3, specs=[[{'type': 'indicator'}]*3, [{'type': 'indicator'}]*3])
# Add each gauge chart as a subplot
for i, res in enumerate(resources, start=1):
    row = (i - 1) // 3 + 1  # Calculate row index
    col = (i - 1) % 3 + 1    # Calculate column index
    fig.add_trace(create_gauge(res["Resource"], res["Available"], res["Total Demand"]), row=row, col=col)
# Update layout to adjust subplot appearance
fig.update_layout(width = 1000,height=600, title_text="Resource Availability Gauges", showlegend=False , margin=dict(l=40, r=40),grid=dict(xgap=1, ygap=1))
# Display the figure in Streamlit
tab1.plotly_chart(fig)

# Styling Dataframe
styled_df = resource_data.style.applymap(color_cells, subset=['Difference'])

tab2.subheader('Data')
tab2.dataframe(styled_df,hide_index=True,width=500)