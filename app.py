import streamlit as st
import pandas as pd
import html  # for HTML entity unescaping
import subprocess

# -------------------------------
# 🛠️ HELPER: Fix mojibake (broken emojis) and HTML escapes
# -------------------------------
def fix_mojibake(text: str) -> str:
    try:
        # Unescape HTML entities
        txt = html.unescape(text)
        # Re-encode Latin-1 to UTF-8 to fix common mojibake
        return txt.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
    except Exception:
        return text

# -------------------------------
# ✅ PAGE CONFIG (must be first Streamlit command)
# -------------------------------
st.set_page_config(
    page_title="🚀 AutoPitchGPT – Startup Investor Pitch Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display current git commit for debugging
commit = subprocess.getoutput("git rev-parse --short HEAD")
st.sidebar.markdown(f"**App Version:** `{commit}`")

# App header
st.title("🚀 AutoPitchGPT")
st.markdown("Create persuasive, GPT-style investor pitches at scale — instantly.")

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
{name}, founded in {founded}, offers a cutting-edge, scalable solution powered by technologies like {tech_stack}. We serve over {customer_base} million users with annual revenues of {revenue}M dollars.

🌍 **Market Opportunity**  
{name} operates in the high-growth {industry} sector, with global demand projected to grow rapidly. With {followers:,} followers and presence in {country}, we’re poised for market dominance.

💸 **Business Model**  
We operate a B2B/B2C hybrid model with **{employees} employees**.  
Our valuation is **{valuation:.2f}B dollars**, and our total funding is **${funding:.2f}M** — which highlights investor confidence.  
We are expanding operations and aim to monetize this growth globally.

💰 **Funding Ask**  
Currently in the **{funding_stage}** stage, we are seeking strategic investors to join us in our next growth phase. Let's build the future of {industry} — together.
"""
        return fix_mojibake(pitch.strip())
    except Exception as e:
        return f"Error generating pitch: {e}"

# -------------------------------
# ✅ SAMPLE DATA LOADER
# -------------------------------
@st.cache_data
def load_sample():
    try:
        # Load from repo root
        df = pd.read_csv("AutoPitchGPT_with_Pitches.csv", encoding="utf-8")
    except FileNotFoundError:
        st.error("⚠️ Sample data not found at repository root: 'AutoPitchGPT_with_Pitches.csv'.")
        return pd.DataFrame(columns=["Startup_Name", "Generated_Pitch"])
    except pd.errors.EmptyDataError:
        st.error("⚠️ Sample data appears empty. Please ensure the CSV has data.")
        return pd.DataFrame(columns=["Startup_Name", "Generated_Pitch"])
    # Fix any mojibake in pre-generated pitches
    df["Generated_Pitch"] = df["Generated_Pitch"].apply(fix_mojibake)
    return df

sample_df = load_sample()
sample_startups = sample_df["Startup_Name"].tolist()

# -------------------------------
# ✅ INPUT OPTIONS
# -------------------------------
st.sidebar.header("🔍 Choose Your Input Method")
option = st.sidebar.radio("Select one:", ["Use Sample Startup", "Upload Your Own CSV"])

if option == "Use Sample Startup":
    if sample_df.empty:
        st.info("No sample data available. Please upload your own CSV.")
    else:
        selected = st.selectbox("Choose a sample startup:", sample_startups)
        row = sample_df[sample_df["Startup_Name"] == selected].iloc[0]
        st.subheader(f"🎯 Investor Pitch for {selected}")
        st.markdown(row["Generated_Pitch"])

elif option == "Upload Your Own CSV":
    st.markdown("### 🗂️ Upload Instructions")
    st.info("""
Please upload a CSV file with these columns:
- Startup_Name (string)
- Founded_Year (integer)
- Country (string)
- Industry (string)
- Funding_Stage (string)
- Total_Funding_$M (float)
- Number_of_Employees (integer)
- Annual_Revenue_$M (float)
- Valuation_$B (float)
- Customer_Base_Millions (float)
- Tech_Stack (string)
- Social_Media_Followers (integer)
""")
    uploaded_file = st.file_uploader("Upload your startup data CSV", type=["csv"])
    if uploaded_file:
        with st.spinner("Generating pitches..."):
            user_df = pd.read_csv(uploaded_file, encoding="utf-8")
            user_df["Generated_Pitch"] = user_df.apply(generate_pitch_from_data, axis=1)
        st.success("✅ Pitches generated successfully!")
        st.dataframe(user_df[["Startup_Name", "Generated_Pitch"]].head(50))
        csv = user_df.to_csv(index=False, encoding="utf-8")
        st.download_button("📥 Download Full CSV with Pitches", data=csv, file_name="Generated_Investor_Pitches.csv")

# -------------------------------
# ✅ FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Powered by GPT-Style Logic | No API Cost | 100% Scalable")
st.caption("Built by Sweety Seelam using Python & Streamlit | © AutoPitchGPT 2025")