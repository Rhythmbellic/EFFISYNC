import streamlit as st
import pandas as pd
import time
from job_func import add_job_tocsv , Show_n_delete
from Scheduling_Back import schedule_jobs


pg_title='<p style="color:#68b6ef ; font-size:50px;text-align:center ; font-family:Courier New">Job Scheduling</p>'
st.markdown(pg_title, unsafe_allow_html=True)

st.divider()

if st.button("Schedule Jobs🗓️"):

    job_input_csv = r"Job_list.csv"
    job_resource_csv = r"job_resources.csv"
    change_state_csv = r"change_state.csv"

    scheduled_jobs_df = schedule_jobs(job_input_csv, job_resource_csv, change_state_csv)
    #st.dataframe(scheduled_jobs_df, hide_index=True,width=700)
    st.data_editor(scheduled_jobs_df,
                   column_config={"Wait Time": st.column_config.BarChartColumn("Wait Time", help="Job's Queue Time",y_min=0,y_max=7)},
                   hide_index=True
                   )
    
if st.button(f"Mark As Done✅",help="Removes the Top Job Queue"):
    jdf = pd.read_csv(r'scheduled_jobs_output.csv')
    jdf = jdf.drop(index=0)
    jdf.to_csv('scheduled_jobs_output.csv')
    dataframe = pd.read_csv('Job_list.csv')
    dataframe = dataframe.drop(index=0)
    dataframe.to_csv('Job_list.csv',index=False)

st.divider()
col1, col2, col3 = st.columns(3)
# Display existing jobs with options to mark as done, delete, etc.
# Example list of jobs (replace with database call)
try:
    jobs = pd.read_csv('Job_list.csv')
    if jobs.empty == False:
        # Dividing into columns
        for index, row in jobs.iterrows():
            if index % 3 == 0:
                with col1:
                    Show_n_delete(jobs,index,row)
            elif index % 3 == 1:
                with col2:
                    Show_n_delete(jobs,index,row)
            else:
                with col3:
                    Show_n_delete(jobs,index,row)
    else:
        st.text("No Jobs")
except:
    st.text("No Jobs")

st.button("Refresh ↻")

st.divider()

# Dialoge box to create a new job
@st.dialog("ADD JOB")
def add_job():
    brand = st.selectbox("Select Brand", ("Lamborghini", "Skoda", "Porsche","Bentley","Audi"),index=None,placeholder="Choose the Brand")
    product = st.selectbox("Select Product",("Headlight","Tail light","Fog light","Parking light","Indicators","Overhead light","Reading light"),index=None,placeholder="Choose a Product")
    quantity = st.number_input("Enter Product Quantity", min_value=1)
    profit = st.number_input("Total Profit from Order", min_value=0)
    
    with st.empty():
        if st.button('Submit'):
            if brand == None or product == None:
                st.error("Details Missing",icon="❌")
            else:
                with st.container():
                    add_job_tocsv('Job_list.csv',brand, product, quantity, profit)
                    st.success("JOB CREATED",icon="✅")
                    time.sleep(1.5)
                st.rerun()
if st.button("➕ADD JOB"):
    add_job()
    
