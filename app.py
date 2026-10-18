
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AWS Sentinel | Anomaly Monitor",
    page_icon="🌩️",
    layout="wide",
)

# -----------------------------
# Dashboard styling
# -----------------------------

# -----------------------------
# Dashboard styling
# -----------------------------
st.markdown(
    """
    <style>
    /* Main dashboard background and text */
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    /* Make normal text readable */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span {
        color: #e2e8f0;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #151f32;
        border: 1px solid #33445f;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111b2d;
    }

    /* Section headings */
    h1, h2, h3 {
        color: #f8fafc !important;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #cbd5e1 !important;
    }

    /* Give charts and tables rounded corners */
    [data-testid="stPlotlyChart"],
    [data-testid="stDataFrame"] {
        border-radius: 10px;
    }



    
/* Professional sidebar and filter styling */
[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

/* Selected filter chips */
[data-baseweb="tag"] {
    background-color: #263449 !important;
    border: 1px solid #40536b !important;
    border-radius: 6px !important;
    color: #e2e8f0 !important;
}

/* Chip text */
[data-baseweb="tag"] span {
    color: #e2e8f0 !important;
}

/* Chip remove icon */
[data-baseweb="tag"] svg {
    fill: #94a3b8 !important;
}

/* Dropdown options */
[data-baseweb="popover"] ul {
    background-color: #111827 !important;
}

[data-baseweb="menu"] {
    background-color: #111827 !important;
}

[role="option"] {
    color: #e2e8f0 !important;
}

/* Subtle hover instead of bright red */
[role="option"]:hover {
    background-color: #263449 !important;
}

/* Filter labels */
[data-testid="stWidgetLabel"] p {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}

)

/* AWS Sentinel download button */
div.stDownloadButton > button {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* Hover effect */
div.stDownloadButton > button:hover {
    background-color: #334155 !important;
    color: #ffffff !important;
    border-color: #64748b !important;
}

/* Keyboard focus */
div.stDownloadButton > button:focus {
    box-shadow: 0 0 0 2px #64748b !important;
}

/* Force the download button into the dark theme */
.stDownloadButton button,
.stDownloadButton button[kind="secondary"],
.stDownloadButton button[kind="primary"] {
    background: #1e293b !important;
    background-color: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
    opacity: 1 !important;
    box-shadow: none !important;
}

/* Keep the text and icon readable */
.stDownloadButton button p,
.stDownloadButton button span,
.stDownloadButton button svg {
    color: #f1f5f9 !important;
    fill: #f1f5f9 !important;
}

/* Hover */
.stDownloadButton button:hover {
    background: #334155 !important;
    background-color: #334155 !important;
    border-color: #64748b !important;
}

/* ===== AWS SENTINEL: MIDNIGHT GLASS THEME ===== */

:root {
    color-scheme: dark;
}

/* Main dashboard background */
.stApp {
    background:
        radial-gradient(
            ellipse at 85% 5%,
            rgba(59, 130, 246, 0.12),
            transparent 38%
        ),
        linear-gradient(135deg, #080d1b 0%, #0c1428 55%, #10152b 100%);
    color: #e8f0ff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1224, #101a30);
    border-right: 1px solid #243653;
}

section[data-testid="stSidebar"] * {
    color: #dce8ff;
}

/* Headings */
h1, h2, h3, h4 {
    color: #f1f6ff !important;
    letter-spacing: 0.2px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(24, 39, 68, 0.95),
        rgba(17, 27, 49, 0.95)
    );
    border: 1px solid #2c4265;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
}

div[data-testid="stMetricLabel"] {
    color: #a9c4ed !important;
}

div[data-testid="stMetricValue"] {
    color: #f4f8ff !important;
}

/* Date picker, select boxes and multiselect controls */
div[data-testid="stDateInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
    background-color: #131f35 !important;
    color: #eaf2ff !important;
    border-color: #344b70 !important;
    border-radius: 9px !important;
}

/* Selected filter chips */
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #203b62 !important;
    border: 1px solid #416da5 !important;
    border-radius: 6px !important;
}

/* Dropdown menus */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: #111d32 !important;
    border: 1px solid #344b70 !important;
}

div[role="option"] {
    color: #eaf2ff !important;
}

/* Data table containers */
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    background: #101b30 !important;
    border: 1px solid #2b4162 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Download button */
div.stDownloadButton button {
    background: linear-gradient(135deg, #17345b, #244a78) !important;
    color: #f1f7ff !important;
    border: 1px solid #4775ad !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

div.stDownloadButton button:hover {
    background: linear-gradient(135deg, #24518a, #3269a6) !important;
    border-color: #68a8ff !important;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.2) !important;
}

/* Links and interactive accents */
a {
    color: #75b8ff !important;
}

/* Smooth visual consistency */
div[data-testid="stPlotlyChart"] {
    border-radius: 12px;
}


/* AWS Sentinel - dark table styling */
div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    background-color: #111c30 !important;
    border: 1px solid #334b70 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Table headers and cells */
div[data-testid="stDataFrame"] [role="columnheader"],
div[data-testid="stDataFrame"] [role="gridcell"],
div[data-testid="stTable"] th,
div[data-testid="stTable"] td {
    background-color: #111c30 !important;
    color: #e2e8f0 !important;
    border-color: #263852 !important;
}

/* Download button */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}


    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Load our existing report
# -----------------------------
st.title("🌩️ AWS SENTINEL")
st.caption("Weather Anomaly Monitoring | Historical Dataset · 2025")

report_path = (
    Path(__file__).resolve().parent
    / "reports"
    / "unified_anomaly_report.csv"
)

if not report_path.exists():
    st.error(f"Could not find the report: {report_path}")
    st.stop()

@st.cache_data
def load_report(path, modified_time):
    data = pd.read_csv(path, parse_dates=["DATE"])
    return data

df = load_report(str(report_path), report_path.stat().st_mtime)

# -----------------------------
# Basic data validation
# -----------------------------
required_columns = [
    "DATE",
    "HourlyDryBulbTemperature",
    "ml_anomaly",
    "contextual_anomaly",
    "isolated_temperature_candidate",
    "statistical_anomaly",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing expected columns: {', '.join(missing_columns)}")
    st.stop()

df = df.sort_values("DATE")

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("Control Panel")
st.sidebar.caption("Explore historical observations")

min_date = df["DATE"].min().date()
max_date = df["DATE"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

available_methods = {
    "Machine learning": "ml_anomaly",
    "Contextual change": "contextual_anomaly",
    "Isolated temperature": "isolated_temperature_candidate",
    "Statistical": "statistical_anomaly",
}

selected_methods = st.sidebar.multiselect(
    "Detection methods",
    options=list(available_methods.keys()),
    default=list(available_methods.keys()),
)

st.subheader("Investigation Priority")

selected_priorities = st.multiselect(
    "Show priority levels",
    options=["High", "Medium", "Review", "Normal"],
    default=["High", "Medium", "Review"],
    help="Choose which priority levels to display."
)

# -----------------------------
# Filter observations
# -----------------------------
filtered = df[
    (df["DATE"].dt.date >= start_date)
    & (df["DATE"].dt.date <= end_date)
].copy()

# Assign an investigation priority to each observation.
filtered["priority"] = "Normal"

# Count distinct detector categories, not individual flags.
filtered["statistical_signal"] = (
    filtered["statistical_anomaly"].fillna(0).astype(int)
)
filtered["ml_signal"] = (
    filtered["ml_anomaly"].fillna(0).astype(int)
)
filtered["contextual_signal"] = (
    filtered["contextual_anomaly"].fillna(0).astype(int)
    | filtered["isolated_temperature_candidate"].fillna(0).astype(int)
)

filtered["detector_categories"] = (
    filtered["statistical_signal"]
    + filtered["ml_signal"]
    + filtered["contextual_signal"]
)

# High: both contextual indicators flag the same observation.
high_priority = (
    (filtered["contextual_anomaly"] == 1)
    & (filtered["isolated_temperature_candidate"] == 1)
)

# Medium: at least two distinct detector categories flag it.
medium_priority = filtered["detector_categories"] >= 2

filtered.loc[
    filtered["detector_categories"] == 1, "priority"
] = "Review"

filtered.loc[medium_priority, "priority"] = "Medium"
filtered.loc[high_priority, "priority"] = "High"

if selected_methods:
    method_columns = [available_methods[name] for name in selected_methods]
    filtered["selected_flag"] = (
        filtered[method_columns].fillna(0).max(axis=1).astype(bool)
    )
    flagged = filtered[filtered["selected_flag"]].copy()
else:
    flagged = filtered.iloc[0:0].copy()

flagged = flagged[
    flagged["priority"].isin(selected_priorities)
].copy()

# -----------------------------
# Summary metrics
# -----------------------------
st.subheader("Monitoring Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Observations", f"{len(filtered):,}")
col2.metric("Flagged observations", f"{len(flagged):,}")
col3.metric(
    "ML flags",
    f"{int(filtered['ml_anomaly'].fillna(0).sum()):,}",
)
col4.metric(
    "Contextual flags",
    f"{int(filtered['contextual_anomaly'].fillna(0).sum()):,}",
)

st.caption(
    "Flags indicate observations worth investigating; "
    "they do not confirm sensor faults. Counts can overlap across methods."
)

# Investigation priority summary
st.subheader("Investigation Priority")

priority_cols = st.columns(4)

priority_cols[0].metric(
    "🔴 High",
    int((filtered["priority"] == "High").sum())
)

priority_cols[1].metric(
    "🟠 Medium",
    int((filtered["priority"] == "Medium").sum())
)

priority_cols[2].metric(
    "🔵 Review",
    int((filtered["priority"] == "Review").sum())
)

priority_cols[3].metric(
    "Normal",
    int((filtered["priority"] == "Normal").sum())
)

# -----------------------------
# Temperature timeline
# -----------------------------
st.subheader("Temperature Timeline")

temperature_column = "HourlyDryBulbTemperature"

chart_data = filtered.dropna(subset=[temperature_column]).copy()
chart_data["Investigation status"] = chart_data["DATE"].isin(
    flagged["DATE"]
).map({True: "Flagged by selected methods", False: "Not flagged by selected methods"})


# Interactive temperature chart with anomaly highlighting

chart_data = chart_data.copy()

chart_data["DATE"] = pd.to_datetime(chart_data["DATE"])

chart_data["Chart status"] = chart_data[
    "Investigation status"
].map({
    "Not flagged by selected methods": "Normal",
    "Flagged by selected methods": "Flagged",
})

normal_data = chart_data[
    chart_data["Chart status"] == "Normal"
]

anomaly_data = chart_data[
    chart_data["Chart status"] == "Flagged"
]

fig = px.scatter(
    normal_data,
    x="DATE",
    y=temperature_column,
    hover_data=[
        "HourlyRelativeHumidity",
        "HourlyWindSpeed",
    ] if {
        "HourlyRelativeHumidity",
        "HourlyWindSpeed",
    }.issubset(normal_data.columns) else None,
    labels={
        "DATE": "Observation time",
        temperature_column: "Temperature (°C)",
    },
)

# Keep normal readings subtle.
fig.update_traces(
    marker=dict(
        color="#64748b",
        size=5,
        opacity=0.55,
    ),
    name="Normal observations",
    showlegend=True,
    selector=dict(mode="markers"),
)

# Highlight observations flagged by selected methods.
if not anomaly_data.empty:
    fig.add_scatter(
        x=anomaly_data["DATE"],
        y=anomaly_data[temperature_column],
        mode="markers",
        name="Flagged observations",
        marker=dict(
            color="#fb7185",
            size=9,
            symbol="diamond",
            line=dict(
                color="#ffe4e6",
                width=1,
            ),
        ),
        customdata=anomaly_data[
            [
                column
                for column in [
                    "priority",
                    "ml_anomaly",
                    "contextual_anomaly",
                    "isolated_temperature_candidate",
                    "statistical_anomaly",
                ]
                if column in anomaly_data.columns
            ]
        ].to_numpy(),
        hovertemplate=(
            "<b>Flagged observation</b><br>"
            "Time: %{x|%d %b %Y, %H:%M}<br>"
            "Temperature: %{y:.1f} °C"
            "<extra></extra>"
        ),
    )

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1120",
    plot_bgcolor="#0b1120",
    height=480,
    legend_title_text="",
    hovermode="closest",
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(
        showgrid=True,
        gridcolor="#1e293b",
        zeroline=False,
    ),
    yaxis=dict(
        title="Temperature (°C)",
        showgrid=True,
        gridcolor="#1e293b",
        zeroline=False,
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displaylogo": False},
)



# -----------------------------
# Detection method breakdown
# -----------------------------
st.subheader("Detection Method Breakdown")

breakdown = pd.DataFrame(
    [
        {
            "Method": name,
            "Flagged observations": int(
                filtered[column].fillna(0).sum()
            ),
        }
        for name, column in available_methods.items()
    ]
)

breakdown_fig = px.bar(
    breakdown,
    x="Method",
    y="Flagged observations",
    color="Method",
    template="plotly_dark",
)

breakdown_fig.update_layout(
    paper_bgcolor="#0b1120",
    plot_bgcolor="#0b1120",
    showlegend=False,
)

st.plotly_chart(breakdown_fig, use_container_width=True)

# Monthly anomaly trend
st.subheader("Monthly Anomaly Trend")

monthly_data = filtered.copy()
monthly_data["DATE"] = pd.to_datetime(monthly_data["DATE"])

# Count observations flagged by the selected detection methods.

selected_detector_columns = [
    available_methods[name]
    for name in selected_methods
    if name in available_methods
]


selected_detector_columns = [
    available_methods[name]
    for name in selected_methods
    if name in available_methods
]

if selected_detector_columns:
    monthly_data["is_flagged"] = (
        monthly_data[selected_detector_columns]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .eq(1)
        .any(axis=1)
    )
else:
    monthly_data["is_flagged"] = False



monthly_data["Month"] = monthly_data["DATE"].dt.to_period("M").dt.to_timestamp()

monthly_trend = (
    monthly_data.groupby("Month")
    .agg(
        Total_observations=("DATE", "size"),
        Flagged_observations=("is_flagged", "sum"),
    )
    .reset_index()
)

monthly_trend["Anomaly_rate"] = (
    monthly_trend["Flagged_observations"]
    / monthly_trend["Total_observations"]
    * 100
).round(2)


trend_fig = px.line(
    monthly_trend,
    x="Month",
    y="Flagged_observations",
    markers=True,
    custom_data=["Total_observations", "Anomaly_rate"],
    labels={
        "Month": "Month",
        "Flagged_observations": "Flagged observations",
    },
    template="plotly_dark",
)

trend_fig.update_traces(
    line=dict(color="#60a5fa", width=3),
    marker=dict(size=8, color="#f472b6"),
    hovertemplate=(
        "<b>%{x|%B %Y}</b><br>"
        "Flagged observations: %{y}<br>"
        "Total observations: %{customdata[0]}<br>"
        "Anomaly rate: %{customdata[1]:.2f}%"
        "<extra></extra>"
    ),
)


trend_fig.update_layout(
    paper_bgcolor="#0b1120",
    plot_bgcolor="#0b1120",
    height=380,
    xaxis=dict(gridcolor="#1e293b"),
    yaxis=dict(
        title="Flagged observations",
        gridcolor="#1e293b",
    ),
)

st.plotly_chart(
    trend_fig,
    use_container_width=True,
    config={"displaylogo": False},
)

st.caption(
    "Monthly counts show observations flagged by at least one "
    "selected detection method. Multiple flags on one observation "
    "count as one flagged observation."
)

# -----------------------------
# Investigation table
# -----------------------------

# -----------------------------
# Anomaly Explanation Panel
# -----------------------------
st.markdown("### 🔎 Understand a flagged observation")

if not flagged.empty:
    flagged = flagged.copy()
    flagged["DATE"] = pd.to_datetime(flagged["DATE"])

    selected_date = st.selectbox(
        "Select an observation to investigate",
        options=flagged["DATE"].tolist(),
        format_func=lambda date: date.strftime("%d %b %Y, %H:%M"),
    )

    observation = flagged.loc[
        flagged["DATE"] == selected_date
    ].iloc[0]

    st.markdown("#### Observation details")

    detail1, detail2, detail3 = st.columns(3)

    temp = observation.get("HourlyDryBulbTemperature")
    humidity = observation.get("HourlyRelativeHumidity")
    wind = observation.get("HourlyWindSpeed")

    detail1.metric(
        "Temperature",
        f"{temp:.1f} °C" if pd.notna(temp) else "Unavailable",
    )
    detail2.metric(
        "Humidity",
        f"{humidity:.1f} %" if pd.notna(humidity) else "Unavailable",
    )
    detail3.metric(
        "Wind speed",
        f"{wind:.1f}" if pd.notna(wind) else "Unavailable",
    )

    st.markdown("#### Why was it flagged?")

    
    reasons = []

    # Explain statistical flags using the actual measurements.
    statistical_columns = [
        ("temperature_iqr_anomaly", "HourlyDryBulbTemperature",
         "Temperature", "°C"),
        ("humidity_iqr_anomaly", "HourlyRelativeHumidity",
         "Relative humidity", "%"),
        ("pressure_iqr_anomaly", "HourlySeaLevelPressure",
         "Sea-level pressure", "hPa"),
        ("wind_iqr_anomaly", "HourlyWindSpeed",
         "Wind speed", ""),
    ]

    for flag_col, value_col, label, unit in statistical_columns:
        if observation.get(flag_col, 0) == 1:
            value = observation.get(value_col)

            if pd.notna(value):
                unit_text = f" {unit}" if unit else ""
                reasons.append(
                    f"Statistical outlier — {label}: measured "
                    f"{value:.1f}{unit_text}. The IQR detector "
                    "identified this measurement as statistically unusual."
                )

    if observation.get("ml_anomaly", 0) == 1:
        reasons.append(
            "Machine learning: Isolation Forest classified the "
            "combination of available weather measurements as unusual. "
            "This flag alone does not identify the cause."
        )

    if observation.get("contextual_anomaly", 0) == 1:
        reasons.append(
            "Contextual detection: a large temperature change was "
            "detected between nearby observations. Check the timestamps "
            "and any gaps in the data."
        )

    if observation.get("isolated_temperature_candidate", 0) == 1:
        difference = observation.get("neighbor_temperature_difference")

        if pd.notna(difference):
            reasons.append(
                f"Isolated temperature candidate: the reading differs "
                f"from nearby valid temperatures by about "
                f"{difference:.1f} °C."
            )
        else:
            reasons.append(
                "Isolated temperature candidate: the reading was "
                "flagged for comparison with nearby valid temperatures."
            )

    
    if reasons:
        for reason in reasons:
            st.markdown(f"- {reason}")

        # Show the IQR thresholds for any statistical outlier.
        st.markdown("#### Statistical thresholds")

        statistical_columns = [
            ("temperature_iqr_anomaly", "HourlyDryBulbTemperature",
             "Temperature", "°C"),
            ("humidity_iqr_anomaly", "HourlyRelativeHumidity",
             "Relative humidity", "%"),
            ("pressure_iqr_anomaly", "HourlySeaLevelPressure",
             "Sea-level pressure", "hPa"),
            ("wind_iqr_anomaly", "HourlyWindSpeed",
             "Wind speed", "km/h"),
        ]

        threshold_rows = []

        for flag_col, value_col, label, unit in statistical_columns:
            if observation.get(flag_col, 0) == 1:
                values = pd.to_numeric(df[value_col], errors="coerce").dropna()

                if not values.empty:
                    q1 = values.quantile(0.25)
                    q3 = values.quantile(0.75)
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    measured = observation[value_col]

                    threshold_rows.append({
                        "Measurement": label,
                        "Measured value": round(measured, 2),
                        "Lower limit": round(lower_bound, 2),
                        "Upper limit": round(upper_bound, 2),
                        "Unit": unit,
                    })

        
    if threshold_rows:
        styled_thresholds = (
            pd.DataFrame(threshold_rows)
            .style
            .set_properties(**{
                "background-color": "#111c30",
                 "color": "#e2e8f0",
                 "border-color": "#334b70",
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#1e3a5f"),
                        ("color", "#93c5fd"),
                        ("border-color", "#334b70"),
                    ],
                }
            ])
        )

        st.dataframe(
            styled_thresholds,
            hide_index=True,
            use_container_width=True,
        )

        st.caption(
                "Limits use Q1 − 1.5 × IQR and Q3 + 1.5 × IQR. "
                "They are calculated from the loaded report data."
            )

    else:
        st.info(
            "No explanation is available from the detector flags "
            "for this observation."
        )

    st.warning(
        "Detector flags are investigation signals, not proof of a "
        "sensor fault. Statistical outliers are unusual values, but "
        "they are not automatically incorrect measurements."
    )

else:
    st.info("Select at least one detection method and a date range containing flagged observations.")


if flagged.empty:
    st.info("No observations match the selected filters.")
else:
    st.markdown("### 🔎 Anomaly Investigation Table")

    # Prepare a readable table.
    table_data = flagged.copy()

    table_data["DATE"] = pd.to_datetime(table_data["DATE"])

    table_data["Detection reasons"] = table_data.apply(
        lambda row: ", ".join(
            name
            for column, name in [
                ("ml_anomaly", "Machine learning"),
                ("contextual_anomaly", "Contextual change"),
                ("isolated_temperature_candidate", "Isolated temperature"),
                ("statistical_anomaly", "Statistical outlier"),
            ]
            if row.get(column, 0) == 1
        ) or "No recorded detector reason",
        axis=1,
    )

    # Select the columns to show.
    preferred_columns = [
        "DATE",
        "priority",
        "HourlyDryBulbTemperature",
        "HourlyRelativeHumidity",
        "HourlySeaLevelPressure",
        "HourlyWindSpeed",
        "Detection reasons",
    ]

    display_columns = [
        column for column in preferred_columns
        if column in table_data.columns
    ]

    # Friendly column names.
    table_data = table_data[display_columns].rename(
        columns={
            "DATE": "Observation time",
            "priority": "Priority",
            "HourlyDryBulbTemperature": "Temperature (°C)",
            "HourlyRelativeHumidity": "Humidity (%)",
            "HourlySeaLevelPressure": "Pressure (hPa)",
            "HourlyWindSpeed": "Wind speed",
        }
    )

    st.caption(
        f"Showing {len(table_data):,} observations matching "
        "your current filters. Select a column heading to sort."
    )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    # Download the same filtered data shown in the table.
   
    # Export the complete investigation data, including detector flags.
    export_data = flagged.copy()

    export_data["Detection reasons"] = export_data.apply(
        lambda row: ", ".join(
            name
            for column, name in [
                ("ml_anomaly", "Machine learning"),
                ("contextual_anomaly", "Contextual change"),
                ("isolated_temperature_candidate", "Isolated temperature"),
                ("temperature_iqr_anomaly", "Temperature IQR"),
                ("humidity_iqr_anomaly", "Humidity IQR"),
                ("pressure_iqr_anomaly", "Pressure IQR"),
                ("wind_iqr_anomaly", "Wind IQR"),
            ]
            if pd.notna(row.get(column))
            and row.get(column, 0) == 1
        ) or "No recorded detector reason",
        axis=1,
    )

    export_columns = [
        "DATE",
        "priority",
        "HourlyDryBulbTemperature",
        "HourlyRelativeHumidity",
        "HourlySeaLevelPressure",
        "HourlyWindSpeed",
        "ml_anomaly",
        "contextual_anomaly",
        "isolated_temperature_candidate",
        "temperature_iqr_anomaly",
        "humidity_iqr_anomaly",
        "pressure_iqr_anomaly",
        "wind_iqr_anomaly",
        "statistical_anomaly",
        "neighbor_temperature_difference",
        "Detection reasons",
    ]

    export_columns = [
        column for column in export_columns
        if column in export_data.columns
    ]

    csv_data = export_data[export_columns].to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Investigation Report (CSV)",
        data=csv_data,
        file_name="aws_sentinel_full_investigation_report.csv",
        mime="text/csv",
        use_container_width=False,
        key="download_investigation_report",
    )



st.caption(
    "AWS Sentinel prototype · Local dashboard · Historical NOAA data · 2025"
)
