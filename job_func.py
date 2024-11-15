import pandas as pd
import streamlit as st
from Scheduling_Back import change_state

def add_job_tocsv(filename, brand, product, quantity, profit):
    # Read the existing DataFrame
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['brand', 'product', 'profit' , 'quantity'])

    # Create a new row
    new_row = pd.DataFrame({'brand': brand, 'product': product, 'profit': profit, 'quantity': quantity}, index=[0])

    # Append the new row to the DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    # Write the DataFrame back to the CSV file
    df.to_csv(filename, index=False)

    change_state('ADD')



def Show_n_delete(dataframe,index,row):
    st.write(f"Job: {row['brand']} : {row['product']}")
    if st.button(f"Delete Job🗑️",key = index):
        dataframe = dataframe.drop(index)
        dataframe.to_csv('Job_list.csv',index=False)
        change_state('Delete')
