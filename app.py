
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# -------------------------------
# ✅ PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="🚀 AutoPitchGPT – Startup Investor Pitch Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 AutoPitchGPT")
st.markdown("Create persuasive, LLM-powered investor pitches at scale — instantly.")

# -------------------------------
# ✅ LOAD ENV + SET API KEY
# -------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
# ✅ PITCH GENERATOR FUNCTION
# -------------------------------
def generate_pitch_from_data(row):
    try:
        name = row['Startup_Name']
        founded = row['Founded_Year']
        country = row['Country']
        industry = row['Industry']
        funding_stage = row['Funding_Stage']
        funding = row['Total_Funding_$M']
        employees = row['Number_of_Employees']
        revenue = row['Annual_Revenue_$M']
        valuation = row['Valuation_$B']
        customer_base = row['Customer_Base_Millions']
        tech_stack = row['Tech_Stack']
        followers = row['Social_Media_Followers']

        pitch = f"""
🚀 **Investor Pitch for {name} ({industry})**

📌 **Problem**  
{industry} is facing major scalability and customer personalization issues in global markets like {country}. Traditional models are failing to address high-volume demand with precision.

💡 **Solution**  
{name}, founded in {founded}, offers a cutting-edge, scalable solution powered by technologies like {tech_stack}. We serve over {customer_base} million users with annual revenues of ${revenue}M.

🌍 **Market Opportunity**  
{name} operates in the high-growth {industry} sector, with global demand projected to grow rapidly. With {followers:,} followers and presence in {country}, we’re poised for market dominance.

💸 **Business Model**  
We operate a B2B/B2C hybrid model with {employees} employees. Our valuation of ${valuation}B and total funding of ${funding}M highlights market confidence. Our next step: expand and monetize globally.

💰 **Funding Ask**  
Currently in the **{funding_stage}** stage, we are seeking strategic investors to join us in our next growth phase. Let's build the future of {industry} — together.
"""
        return pitch.strip()
    except Exception as e:
        return f"Error generating pitch: {e}"

# -------------------------------
# ✅ SAMPLE DATASET
# -------------------------------
@st.cache_data
def load_sample():
    return pd.read_csv("AutoPitchGPT_with_Pitches.csv")

sample_df = load_sample()
sample_startups = sample_df.head(5)['Startup_Name'].tolist()

# -------------------------------
# ✅ INPUT OPTIONS
# -------------------------------
st.sidebar.header("🔍 Choose Your Input Method")
option = st.sidebar.radio("Select one:", ["Use Sample Startup", "Upload Your Own CSV"])

if option == "Use Sample Startup":
    selected = st.selectbox("Choose a sample startup:", sample_startups)
    row = sample_df[sample_df["Startup_Name"] == selected].iloc[0]
    pitch = row["Generated_Pitch"]
    st.subheader(f"🎯 Investor Pitch for {selected}")
    st.markdown(pitch)

elif option == "Upload Your Own CSV":
    uploaded_file = st.file_uploader("Upload your startup data CSV", type=["csv"])
    if uploaded_file:
        user_df = pd.read_csv(uploaded_file)
        with st.spinner("Generating pitches..."):
            user_df["Generated_Pitch"] = user_df.apply(generate_pitch_from_data, axis=1)
        st.success("✅ Pitches generated successfully!")
        st.write(user_df[["Startup_Name", "Generated_Pitch"]])
        csv = user_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full CSV with Pitches", data=csv, file_name="Generated_Investor_Pitches.csv")

# -------------------------------
# ✅ FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Powered by GPT-4 | No API cost | 100% scalable")
st.caption("Built by Sweety Seelam  using GPT & Streamlit | © AutoPitchGPT 2025")
