import streamlit as st
from PIL import Image
import base64

# Page BG color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-color: #0E0B20
}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)

# Logo Image
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Logo image path (replace with the correct path to your image)
logo_path = r"Logo.jpg"
logo_base64 = load_image(logo_path)

st.logo(logo_path,size="large")


st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Creating Pages
pages = {
    "Effisync": [
        st.Page("home.py", title="🏠︎ Home"),
        st.Page("Job_UI.py", title="🗓️ Production Scheduling"),
        st.Page("Demand_Report_UI.py", title="📑 Demand Report"),
        st.Page("Health_UI.py",title="🥼 Machine Health"),
        st.Page("Inventory_Analysis_UI.py",title="🛠️ Inventory Analysis")
    ]
}

pg = st.navigation(pages)
pg.run()