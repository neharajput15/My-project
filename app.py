import streamlit as st
import pandas as pd


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Internship Recommendation System",
    page_icon="📌",
    layout="wide"
)


# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("internships.csv")

df.columns = df.columns.str.strip()



# -----------------------------
# Professional CSS
# -----------------------------
st.markdown("""
<style>

/* Force Light Theme */

.stApp{
    background:#f5f9ff !important;
    color:#000000 !important;
}


/* Header */

.header{

    background:linear-gradient(135deg,#1565C0,#42A5F5);

    padding:35px;

    border-radius:20px;

    text-align:center;

    color:white !important;

    margin-bottom:30px;

}


.header h1{

    color:white !important;

    font-size:42px;

}


.header p{

    color:white !important;

}



/* Sidebar */

[data-testid="stSidebar"]{

    background:white !important;

}


[data-testid="stSidebar"] *{

    color:#000000 !important;

}



/* Metrics */

div[data-testid="metric-container"]{

    background:white !important;

    padding:20px;

    border-radius:15px;

    box-shadow:0 5px 15px rgba(0,0,0,0.1);

}


div[data-testid="metric-container"] *{

    color:#000000 !important;

}



/* Cards */

.card{

    background:white !important;

    color:#000000 !important;

    padding:25px;

    border-radius:18px;

    margin:20px 0;

    box-shadow:0 8px 20px rgba(0,0,0,0.12);

    border-left:6px solid #1565C0;

}


.card h2{

    color:#1565C0 !important;

}


.card p,
.card b{

    color:#000000 !important;

}



/* Tags */

.tag{

    background:#E3F2FD !important;

    color:#1565C0 !important;

    padding:6px 12px;

    border-radius:20px;

    margin:4px;

    display:inline-block;

}



/* Score */

.score{

    background:#E8F5E9 !important;

    color:#2E7D32 !important;

    padding:12px;

    border-radius:10px;

    font-weight:bold;

}



/* Button */

.stButton>button{

    background:#1565C0 !important;

    color:white !important;

    border-radius:10px;

    height:45px;

    font-weight:bold;

}


.stButton>button:hover{

    background:#0D47A1 !important;

}



/* Text */

p, label, span{

    color:#000000 !important;

}


</style>

""", unsafe_allow_html=True)




# -----------------------------
# Header
# -----------------------------
st.markdown("""

<div class="header">

<h1>📌 Internship Recommendation System</h1>

<p>
AI-based platform to discover suitable internship opportunities
</p>

</div>

""", unsafe_allow_html=True)




# -----------------------------
# Dashboard
# -----------------------------
c1,c2,c3 = st.columns(3)


c1.metric(
    "📋 Internship Roles",
    df["internship_role"].nunique()
)


c2.metric(
    "📚 Total Opportunities",
    len(df)
)


c3.metric(
    "📍 Available Locations",
    df["location"].nunique()
)



st.write("---")




# -----------------------------
# Student Profile
# -----------------------------
st.sidebar.title("👤 Student Profile")


branch = st.sidebar.selectbox(
    "🎓 Academic Branch",
    sorted(df["branch"].unique())
)


interest = st.sidebar.selectbox(
    "📌 Area of Interest",
    sorted(df["interest"].unique())
)


mode = st.sidebar.selectbox(
    "🌐 Work Mode",
    sorted(df["mode"].unique())
)


location = st.sidebar.selectbox(
    "📍 Preferred Location",
    sorted(df["location"].unique())
)



cgpa = st.sidebar.slider(
    "📊 CGPA",
    float(df["min_cgpa"].min()),
    float(df["min_cgpa"].max()),
    7.0,
    0.1
)




# -----------------------------
# Recommendation System
# -----------------------------
if st.sidebar.button("🔍 Get Recommendations"):

    data = df.copy()

    # Match Score
    data["Match Score"] = 0

    # Branch Match
    data.loc[data["branch"] == branch, "Match Score"] += 30

    # Interest Match
    data.loc[data["interest"] == interest, "Match Score"] += 30

    # Mode Match
    data.loc[data["mode"] == mode, "Match Score"] += 15

    # Location Match
    data.loc[data["location"] == location, "Match Score"] += 15

    # CGPA Match
    data.loc[data["min_cgpa"] <= cgpa, "Match Score"] += 10

    # Sort by highest score
    result = data.sort_values(
        by="Match Score",
        ascending=False
    )

    # Show only Top 5
    top_results = result.head(5)

    st.subheader("📋 Top Internship Recommendations")

    if top_results.empty:

        st.warning(
            "No suitable internship found."
        )

    else:

        st.success(
            "Showing Top 5 Best Matching Internships"
        )

        for _, row in top_results.iterrows():

            st.markdown(f"""
            <div class="card">

            <h2>📋 {row['internship_role']}</h2>

            <span class="tag">🎓 {row['branch']}</span>
            <span class="tag">📌 {row['interest']}</span>
            <span class="tag">🌐 {row['mode']}</span>
            <span class="tag">📍 {row['location']}</span>

            <br><br>

            ⚙️ <b>Required Skills:</b>

            <p>{row['required_skills']}</p>

            📊 <b>Minimum CGPA:</b> {row['min_cgpa']}

            <br><br>

            <div class="score">

            ⭐ Match Score: {row['Match Score']}%

            </div>

            </div>

            """, unsafe_allow_html=True)
