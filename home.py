import streamlit as st
import base64

def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Logo image path (replace with the correct path to your image)
title_path = r"Title.png"
title_base64 = load_image(title_path)

st.logo(title_path,size="large")


st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{title_base64}">
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

caption='<p style="color:#68b6ef ; font-size:35px;text-align:center ; font-family:Courier New ;">AI Resource & Workload Planner</p>'
st.markdown(caption, unsafe_allow_html=True)

