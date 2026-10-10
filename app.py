import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Food Delivery Time Dashboard",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    data = pd.read_csv("delivery_data.csv")

    numeric_columns = [
        "Delivery_person_Age",
        "Delivery_person_Ratings",
        "Restaurant_latitude",
        "Restaurant_longitude",
        "Delivery_location_latitude",
        "Delivery_location_longitude",
        "Time_taken(min)"
    ]
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna(subset=[
        "Delivery_person_Age", "Delivery_person_Ratings",
        "Type_of_order", "Type_of_vehicle", "Time_taken(min)"
    ])

    data["Type_of_order"] = data["Type_of_order"].astype(str)
    data["Type_of_vehicle"] = data["Type_of_vehicle"].astype(str)
    return data

df = load_data()

# ---------- Sidebar: global filters ----------
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Selections here update every chart and KPI.")

order_options = sorted(df["Type_of_order"].dropna().unique().tolist())
vehicle_options = sorted(df["Type_of_vehicle"].dropna().unique().tolist())

selected_orders = st.sidebar.multiselect(
    "Order type", options=order_options, default=order_options
)
selected_vehicles = st.sidebar.multiselect(
    "Vehicle type", options=vehicle_options, default=vehicle_options
)

age_min, age_max = int(df["Delivery_person_Age"].min()), int(df["Delivery_person_Age"].max())
age_range = st.sidebar.slider(
    "Delivery person age", min_value=age_min, max_value=age_max,
    value=(age_min, age_max)
)

rating_min = float(df["Delivery_person_Ratings"].min())
rating_max = float(df["Delivery_person_Ratings"].max())
rating_range = st.sidebar.slider(
    "Delivery person rating",
    min_value=rating_min, max_value=rating_max,
    value=(rating_min, rating_max), step=0.1
)

time_min, time_max = int(df["Time_taken(min)"].min()), int(df["Time_taken(min)"].max())
time_range = st.sidebar.slider(
    "Delivery time (minutes)", min_value=time_min, max_value=time_max,
    value=(time_min, time_max)
)

if st.sidebar.button("Reset all filters", use_container_width=True):
    st.rerun()

# Apply the same filters once, then use filtered_df for every chart.
filtered_df = df[
    df["Type_of_order"].isin(selected_orders)
    & df["Type_of_vehicle"].isin(selected_vehicles)
    & df["Delivery_person_Age"].between(age_range[0], age_range[1])
    & df["Delivery_person_Ratings"].between(rating_range[0], rating_range[1])
    & df["Time_taken(min)"].between(time_range[0], time_range[1])
].copy()

# ---------- Dashboard heading ----------
st.title("🛵 Food Delivery Time Analysis Dashboard")
st.markdown(
    "Explore delivery times, vehicle types, order categories, and delivery-person "
    "ratings. **Use the sidebar filters to update all KPIs and charts together.**"
)

if filtered_df.empty:
    st.warning("No records match the selected filters. Widen or reset the sidebar filters.")
    st.stop()

# ---------- KPI cards ----------
avg_time = filtered_df["Time_taken(min)"].mean()
median_time = filtered_df["Time_taken(min)"].median()
avg_rating = filtered_df["Delivery_person_Ratings"].mean()
total_orders = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Filtered deliveries", f"{total_orders:,}")
k2.metric("Average delivery time", f"{avg_time:.1f} min")
k3.metric("Median delivery time", f"{median_time:.1f} min")
k4.metric("Average delivery-person rating", f"{avg_rating:.2f} / 5")

st.divider()

# Consistent colors and readable charts
color_sequence = px.colors.qualitative.Set2

# ---------- Row 1 ----------
left, right = st.columns(2)

with left:
    st.subheader("1. Delivery Time Distribution")
    fig = px.histogram(
        filtered_df, x="Time_taken(min)", nbins=25,
        labels={"Time_taken(min)": "Delivery time (minutes)", "count": "Number of deliveries"},
        color_discrete_sequence=[color_sequence[0]],
        title="How long deliveries take"
    )
    fig.update_layout(bargap=0.08, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("2. Average Delivery Time by Vehicle")
    vehicle_summary = (
        filtered_df.groupby("Type_of_vehicle", as_index=False)["Time_taken(min)"]
        .mean().sort_values("Time_taken(min)", ascending=False)
    )
    fig = px.bar(
        vehicle_summary, x="Type_of_vehicle", y="Time_taken(min)",
        color="Type_of_vehicle", text_auto=".1f",
        labels={"Type_of_vehicle": "Vehicle type", "Time_taken(min)": "Average time (minutes)"},
        title="Compare average time across vehicles",
        color_discrete_sequence=color_sequence
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 2 ----------
left, right = st.columns(2)

with left:
    st.subheader("3. Average Delivery Time by Order Type")
    order_summary = (
        filtered_df.groupby("Type_of_order", as_index=False)["Time_taken(min)"]
        .mean().sort_values("Time_taken(min)", ascending=False)
    )
    fig = px.bar(
        order_summary, x="Type_of_order", y="Time_taken(min)",
        color="Type_of_order", text_auto=".1f",
        labels={"Type_of_order": "Order type", "Time_taken(min)": "Average time (minutes)"},
        title="Compare order categories",
        color_discrete_sequence=color_sequence
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("4. Delivery Person Age vs Delivery Time")
    # Sample only for a responsive scatter plot when the filters return many rows.
    scatter_df = filtered_df.sample(n=min(5000, len(filtered_df)), random_state=42)
    fig = px.scatter(
        scatter_df, x="Delivery_person_Age", y="Time_taken(min)",
        color="Type_of_vehicle", opacity=0.6,
        labels={
            "Delivery_person_Age": "Delivery person age",
            "Time_taken(min)": "Delivery time (minutes)",
            "Type_of_vehicle": "Vehicle"
        },
        title="Age and delivery time relationship",
        color_discrete_sequence=color_sequence
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 3 ----------
left, right = st.columns(2)

with left:
    st.subheader("5. Rating vs Delivery Time")
    fig = px.scatter(
        filtered_df, x="Delivery_person_Ratings", y="Time_taken(min)",
        color="Type_of_order", opacity=0.65,
        labels={
            "Delivery_person_Ratings": "Delivery person rating",
            "Time_taken(min)": "Delivery time (minutes)",
            "Type_of_order": "Order type"
        },
        title="Ratings compared with delivery time",
        color_discrete_sequence=color_sequence
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("6. Correlation Heatmap")
    numeric_cols = [
        "Delivery_person_Age", "Delivery_person_Ratings",
        "Restaurant_latitude", "Restaurant_longitude",
        "Delivery_location_latitude", "Delivery_location_longitude",
        "Time_taken(min)"
    ]
    corr = filtered_df[numeric_cols].corr(numeric_only=True)
    fig = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
        title="Correlation between numeric variables"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Data preview and download ----------
st.divider()
with st.expander("View filtered data"):
    st.dataframe(filtered_df, use_container_width=True, height=320)

csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered data as CSV",
    data=csv_bytes,
    file_name="filtered_delivery_data.csv",
    mime="text/csv"
)

st.caption(
    "Dataset fields are used as provided. Correlation indicates association, "
    "not proof that one variable causes another."
)
