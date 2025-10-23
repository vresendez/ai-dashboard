import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------
st.set_page_config(
    page_title="AI Politicization Dashboard (Netherlands 2023–2025)",
    layout="wide",
)

st.title("🇳🇱 Disccussion of AI in Dutch Party Programs (2023–2025)")

st.markdown("""
This dashboard builds on **Morosoli et al. (2025)** and extends it with
a longitudinal analysis of Dutch political manifestos (2023 → 2025).
It tracks how prominent is the discussion over related terms to Artificial Intelligence (AI) in party programs.  
""")

# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data/ai_sentences_with_dimensions.xlsx")
    wc = pd.read_excel("data/df_wordcount.xlsx")
    df["Year"] = df["Year"].astype(int)
    wc["Year"] = wc["Year"].astype(int)
    return df, wc

df, df_wc = load_data()

# ---------------------------------------------
# NORMALIZATION
# ---------------------------------------------
ai_summary = df.groupby(["Party","Year"]).size().reset_index(name="AI_Sentences")
merged = pd.merge(ai_summary, df_wc, on=["Party","Year"], how="left")
merged["AI_per_10k_words"] = (merged["AI_Sentences"] / merged["Total_Words"]) * 10000

# Identify governing vs opposition
governing = ["PVV","VVD","NSC", "BBB"]
merged["Status"] = merged["Party"].apply(lambda p: "2023 Tweede Kamer" if p in governing else "Other parties")

# ---------------------------------------------
# FILTER SETTINGS (no sidebar)
# ---------------------------------------------
parties = sorted(merged["Party"].unique())
selected_parties = parties  # show all by default
show_norm = True            # always normalize
selected_dimensions = sorted(df["Dimension"].unique())  # all dimensions


# ---------------------------------------------
# FILTERED DATA
# ---------------------------------------------
df_filtered = df[df["Party"].isin(selected_parties) & df["Dimension"].isin(selected_dimensions)]
merged_filtered = merged[merged["Party"].isin(selected_parties)]

# ---------------------------------------------
# SECTION 1 — NORMALIZED POLITICIZATION
# ---------------------------------------------
st.subheader("Salience of AI across parties (2023 vs.2025)")

# Keep only 2023 and 2025
# Ensure Year is a string so Plotly uses categorical x-axis
merged_filtered["Year"] = merged_filtered["Year"].astype(str)


# Decide which metric to show (normalized or absolute)
y_axis = "AI_per_10k_words" if show_norm else "AI_Sentences"

fig_trend = px.line(
    merged_filtered,
    x="Year",
    y=y_axis,
    color="Party",
    markers=True,
    facet_col="Status",       # split into Governing / Opposition panels
    category_orders={"Year": [2023, 2025]},
    title="AI Mentions in Party Programs (2023 vs 2025)"
)

fig_trend.update_layout(
    yaxis_title="AI Mentions per 10,000 words" if show_norm else "AI-related Sentences",
    xaxis_title="Year",
    legend_title_text="Party",
    template="simple_white"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("""
**Note:**  
The line connects the frequency of AI terms mentioned in the party programs (2023 to 2025).  
- A downward slope = **less discussion**  of AI.  
- An upward slope = **more discussion** of AI.
""")

# ---------------------------------------------
# SECTION 2 — FRAMING EVOLUTION
# ---------------------------------------------
st.subheader("Ways AI is discussed: Policy, Ethics, Security, Economy, Labour and Social Context")
base_dimensions = [
    "Ethical", "Societal", "Policy / Regulation",
    "Security", "Labour", "Economic", "Uncategorized"
]
df_summary = pd.read_excel("data/ai_dimension_summary_multicol.xlsx")

fig = px.bar(
    df_summary.melt(id_vars=["Party", "Year"], value_vars=base_dimensions),
    x="Party", y="value", color="variable",
    barmode="stack", facet_col="Year",
    title="AI discussion by dimension (Multi-label)"
)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------
# SECTION 3 — EXAMPLE STATEMENTS
# ---------------------------------------------
# ---------------------------------------------
# SECTION 3 — EXAMPLE STATEMENTS (Improved)
# ---------------------------------------------
st.subheader("💬 Example of statements")

# -- Sidebar-like filters inline --
col1, col2, col3 = st.columns(3)
with col1:
    party_pick = st.selectbox("Party", sorted(df["Party"].unique()))
with col2:
    year_pick = st.selectbox("Year", sorted(df["Year"].unique()))
with col3:
    dim_pick = st.selectbox("Dimension", sorted(set(sum([d.split(",") for d in df["Dimension"].dropna().unique()], []))))

# -- Flexible match: any dimension containing the selected one
mask = (
    (df["Party"] == party_pick)
    & (df["Year"] == year_pick)
    & (df["Dimension"].str.contains(dim_pick, case=False, na=False))
)

examples = df.loc[mask, ["Translated_Sentence", "Sentiment", "Dimension"]].head(5)

# -- Display results
if examples.empty:
    st.info("No examples found for this combination.")
else:
    for i, row in examples.iterrows():
        st.markdown(
            f"""
            <div style="background-color:#f9f9f9;border-radius:10px;padding:10px;margin-bottom:10px;">
            <b>🗂 Dimension:</b> {row['Dimension']}  
            <b>🧭 Sentiment:</b> {row['Sentiment']}  
            <blockquote style="margin-top:5px;">{row['Translated_Sentence']}</blockquote>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------
# SECTION 4 — SUMMARY STATS
# ---------------------------------------------
st.subheader("📊 Change overview (2023 → 2025)")

st.markdown("""
This table shows how much each **political party’s attention to Artificial Intelligence (AI)**
has changed between the **2023** and **2025** manifestos.

The metric are ** keywords related to AI mentions per 10 000 words**, so differences in document length are normalized.
The last column (**Δ**) represents the change from 2023 → 2025:
- **Positive Δ (+)** → the party discusses AI *more often* in 2025.  
- **Negative Δ (–)** → the party discusses AI *less often*.
""")

# --- Create pivot table (Year columns are strings)
change_df = (
    merged_filtered
    .pivot(index="Party", columns="Year", values="AI_per_10k_words")
    .fillna(0)
)

# --- Fix Δ calculation safely
if "2023" in change_df.columns and "2025" in change_df.columns:
    change_df["Δ"] = change_df["2025"] - change_df["2023"]
else:
    st.warning("⚠️ Missing data for one of the years (2023 or 2025). Δ could not be computed.")
    change_df["Δ"] = 0

# --- Sort and display
change_df = change_df.sort_values("Δ", ascending=False)

st.dataframe(
    change_df.style.format({
        "2023": "{:.2f}",
        "2025": "{:.2f}",
        "Δ": "{:+.2f}"
    }),
    use_container_width=True
)

st.markdown("""
*Note:**  
Governments showing **negative Δ** (decrease) illustrate **institutionalization or issue saturation**,
meaning AI has become part of routine governance.
In contrast, **increases among opposition parties** suggest **renewed politicization** or
the strategic use of AI in framing new policy debates.
""")


st.markdown("---")
st.caption("VR · Data: Party programs 2023–2025 · Built with Streamlit & Plotly")
