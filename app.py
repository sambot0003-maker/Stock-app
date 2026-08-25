import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Wingo Stats Analyzer", layout="wide")
st.title("🎯 Wingo Colour Analysis Dashboard")
st.caption("Hackathon Project — Statistical Analysis of Game Outcomes")

# --- Simulate Past Results (replace with real CSV) ---
np.random.seed(42)
n_rounds = 500
colors = np.random.choice(["Red", "Green", "Violet"], n_rounds, p=[0.45, 0.45, 0.10])
numbers = np.random.randint(0, 10, n_rounds)

df = pd.DataFrame({
    "Round": range(1, n_rounds + 1),
    "Color": colors,
    "Number": numbers
})

# --- Sidebar ---
st.sidebar.header("⚙️ Settings")
window = st.sidebar.slider("Analysis Window (last N rounds)", 50, 500, 200)
df_view = df.tail(window)

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
col1.metric("🔴 Red %", f"{(df_view['Color']=='Red').mean()*100:.1f}%")
col2.metric("🟢 Green %", f"{(df_view['Color']=='Green').mean()*100:.1f}%")
col3.metric("🟣 Violet %", f"{(df_view['Color']=='Violet').mean()*100:.1f}%")

st.divider()

# --- Charts ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🎨 Colour Distribution")
    fig1 = px.pie(df_view, names="Color",
                  color_discrete_map={"Red":"#e74c3c","Green":"#2ecc71","Violet":"#9b59b6"})
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🔢 Number Frequency")
    fig2 = px.histogram(df_view, x="Number", nbins=10,
                        color_discrete_sequence=["#3498db"])
    fig2.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig2, use_container_width=True)

# --- Streak Analysis ---
st.subheader("🔥 Current Streaks")
streak = 1
for i in range(len(df_view)-2, -1, -1):
    if df_view.iloc[i]["Color"] == df_view.iloc[-1]["Color"]:
        streak += 1
    else:
        break
st.info(f"Last color **{df_view.iloc[-1]['Color']}** has a streak of **{streak}** rounds")

# --- Randomness Test ---
st.subheader("🧪 Chi-Square Randomness Test")
expected = {"Red": 0.45, "Green": 0.45, "Violet": 0.10}
observed = df_view["Color"].value_counts(normalize=True)
chi2 = sum((observed.get(c,0) - e)**2 / e for c, e in expected.items())
st.write(f"Chi-Square Statistic: **{chi2:.4f}**")
if chi2 < 5.99:
    st.success("✅ Results are consistent with RANDOM distribution")
else:
    st.warning("⚠️ Slight deviation detected (still likely random)")

st.divider()
st.caption("📌 This tool is for educational & statistical analysis only.")
