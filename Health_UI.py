import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from health_model import preprocess_and_predict as pred
import pandas as pd
from matplotlib.patches import Patch


model = r"MH_model.pkl"
data = r"MACHINE_HEALTH_TEST.csv"
predictions = pred(model,data)

df = pd.read_csv(data)
df["Health"]= predictions*100

pg_title='<p style="color:#68b6ef ; font-size:50px;text-align:center ; font-family:Courier New">Machine Health</p>'
st.markdown(pg_title, unsafe_allow_html=True)

st.divider()

# Colour schemes styling for graphs and dataframe
def color_cells(val):
    color = ''
    if val<=100 and val >=90:
        color = 'background-color: #28a745; color: black'
    elif val<=89 and val >=70:
        color = 'background-color: #8bc34a; color: black'
    elif val<=69 and val >=50:
        color = 'background-color: #ffeb3b; color: black'
    elif val<=49 and val >=30:
        color = 'background-color: #ff9800; color: black'
    elif val<=29 and val >=10:
        color = 'background-color: #f44336; color: black'
    elif val<=9 and val>=0:
        color = 'background-color: #b71c1c; color: black'
    else:
        color = 'background-color: black; color: black'
    return color

colors = ['#28a745' if val<=100 and val >=90 else
          '#8bc34a' if val<=89 and val >=70 else
          '#ffeb3b' if val<=69 and val >=50 else
          '#ff9800' if val<=49 and val >=30 else
          '#f44336' if val<=29 and val >=10 else
          '#b71c1c' if val<=9 and val>=0 else
          'black'
          for val in df['Health']]

# Styling Dataframe
styled_df = df.style.applymap(color_cells, subset=['Health'])

legend_elements = [Patch(facecolor='#28a745', edgecolor='#000000',label='Excellent'),
                   Patch(facecolor='#8bc34a', edgecolor='#000000',label='Good'),
                   Patch(facecolor='#ffeb3b', edgecolor='#000000',label='Moderate'),
                   Patch(facecolor='#ff9800', edgecolor='#000000',label='Poor'),
                   Patch(facecolor='#f44336', edgecolor='#000000',label='Critical'),
                   Patch(facecolor='#b71c1c', edgecolor='#000000',label='Failure/Near Failure')
                   ]

# Creating Graphs using matplotlib
fig, ax = plt.subplots()
plt.style.use('Solarize_Light2')
bar = ax.barh(df['Machine'], df['Health'], color=colors) 
ax.set_title("Machine Health Status")
ax.set_ylabel("Machines")
ax.set_xlabel("Health Scores")
ax.set_facecolor('#0E0B20')
ax.bar_label(bar,labels=[f'{score:.2f}%' for score in df['Health']],color='w')
ax.set_xlim(right=110)  
ax.legend(handles=legend_elements,fontsize='small')
plt.grid(False)

# Creating tabs
tab1, tab2 = st.tabs(["📊 Graphs", "🗃️ Data"])

tab1.subheader('Graphs')
tab1.pyplot(fig)

tab2.subheader('Data')
tab2.dataframe(styled_df,hide_index=True)




