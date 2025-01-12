import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import pandas as pd
from pinotdb import connect
import plotly.express as px

# Connect to Pinot
conn = connect(host='54.179.19.243', port=8099, path='/query/sql', scheme='http')

# Query the data
curs = conn.cursor()




# Set page configuration with dark/light mode toggle
st.set_page_config(page_title="Engagement User Dashboard", layout="wide")
st.title("💹Engagement User Dashboard📊")

# Add a sidebar for theme selection
theme = st.sidebar.radio("Select Theme", ("Light", "Dark"))

# Set dark/light mode styling
if theme == "Dark":
    st.markdown(
        """
        <style>
        .main { background-color: #2E2E2E; color: white; }
        h1 { color: #F0E68C; } /* Contrasting title color */
        .chart-title { color: #F0E68C; } /* Chart title color */
        </style>
        """, unsafe_allow_html=True
    )
    plotly_template = "plotly_dark"
    title_color = "#FFFFFF"  # Light yellow for dark mode
else:
    st.markdown(
        """
        <style>
        .main { background-color: #FFFFFF; color: black; }
        h1 { color: #2E2E2E; } /* Contrasting title color */
        .chart-title { color: #2E2E2E; } /* Chart title color */
        </style>
        """, unsafe_allow_html=True
    )
    plotly_template = "plotly_white"
    title_color = "#2E2E2E"  # Dark gray for light mode

# Auto-refresh every 5 seconds (5000 ms)
st_autorefresh(interval=20000, key="auto_refresh")



# Generate filters for SQL query
curs_PAGE = conn.cursor()
curs_PAGE.execute("SELECT DISTINCT PAGE FROM ACTION_TUMLING_T6")
PAGE = [row[0] for row in curs_PAGE]

# Sidebar filter for Pages
page_select = st.sidebar.multiselect(
    "Filter by Pages", 
    options=PAGE, 
    default=PAGE
)

# Fetch distinct genders from the database
curs_LEVEL = conn.cursor()
curs_LEVEL.execute("SELECT DISTINCT LEVEL FROM ACTION_TUMLING_T6")
level = [row[0] for row in curs_LEVEL]

# Sidebar filter for Genders
level_select = st.sidebar.multiselect(
    "Filter by Level", 
    options=level, 
    default=level
)
 
page_filter = "'" + "', '".join(page_select) + "'"
level_filter = "'" + "', '".join(level_select) + "'"

# Layout with 2 columns and 4 rows (4 charts)
col1, col2 = st.columns(2)

# Chart 1
with col1:
    ##st.markdown(f'<h3 class="chart-title" style="color: {title_color};">Line Chart</h3>', unsafe_allow_html=True)
    query1 = f"""
                SELECT
                    PAGE,
                    ACTION,
                    COUNT( ACTION) AS SESSION
                FROM
                    ACTION_TUMLING_T6
                WHERE
                    LEVEL IN ({level_filter})  
                    AND PAGE IN ({page_filter})                   
                GROUP BY PAGE, ACTION ; """
    curs.execute(query1)
    df_1 = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    fig1 = px.bar(
        df_1,
        x='PAGE',
        y='SESSION',
        color='ACTION',
        labels={'SESSION': 'Unique Session Count'},
        height=400,
        title="📲 Popular Visit Page by Action",
        text_auto=True,
        template=plotly_template
    )
    st.plotly_chart(fig1, use_container_width=True)

# # Chart 2
with col2:
    ##st.markdown(f'<h3 class="chart-title" style="color: {title_color};">Bar Plot</h3>', unsafe_allow_html=True)
    query2 = f"""
                SELECT 
                    COUNTRY,
                    COUNT( COUNTRY) AS SESSION
                FROM
                    ACTION_TUMLING_T6
                WHERE
                    LEVEL IN ({level_filter})  
                    AND PAGE IN ({page_filter})                   
                GROUP BY COUNTRY
                ORDER BY SESSION ASC
                LIMIT 10 ; """
    curs.execute(query2)
    df_2 = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    fig2 = px.bar(
        df_2,
        x='SESSION',
        y='COUNTRY',
        color='SESSION',
        color_continuous_scale='Blues',  # Gradient color scale from light to dark
        labels={'SESSION': 'Visit Count', 'COUNTRY': 'Country'},
        height=400,
        text_auto=True,
        template=plotly_template
    )

    fig2.update_layout(
        title="🎊 Top 10 Countries by Visit Count",
        xaxis_title="Visit Count",
        yaxis_title="Country",
        coloraxis_colorbar=dict(title="Visit Count"),
    )

    st.plotly_chart(fig2, use_container_width=True)

# # Chart 3
with col1:
    ##st.markdown(f'<h3 class="chart-title" style="color: {title_color};">Bar Chart</h3>', unsafe_allow_html=True)
    query3 = f"""
                SELECT 
                    ACTION,
                    LEVEL,
                    COUNT( LEVEL) AS SESSION
                FROM
                    ACTION_TUMLING_T6
                WHERE
                    LEVEL IN ({level_filter})  
                    AND PAGE IN ({page_filter})                   
                GROUP BY ACTION ,LEVEL ; """
    curs.execute(query3)
    df_3 = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

    fig3 = px.bar(
        df_3,
        x="ACTION",
        y="SESSION",
        color="LEVEL",
        title=" Session Count Level by Action",
        text_auto=True,
        template=plotly_template
    )
    fig3.update_layout(
        title=" 🚀  Visit Level by Action ",
        xaxis_title="Action",
        yaxis_title="Unique Session Count"
    )   
    st.plotly_chart(fig3, use_container_width=True)

# # Chart 4    
#     #fig4 = px.histogram(filtered_data, x="Values", color="Category", template=plotly_template)
with col2:
    ##st.markdown(f'<h3 class="chart-title" style="color: {title_color};">Histogram</h3>', unsafe_allow_html=True)
    ##st.markdown(f'<h3 class="chart-title" style="color: {title_color};">Pie Chart</h3>', unsafe_allow_html=True)
    query4 = f"""
                SELECT 
                    CHANNEL,
                    COUNT( LEVEL) AS SESSION
                FROM
                    ACTION_TUMLING_T6
                WHERE
                    LEVEL IN ({level_filter})  
                    AND PAGE IN ({page_filter})                   
                GROUP BY CHANNEL ; """
    curs.execute(query4)
    df_4 = pd.DataFrame(curs, columns=[item[0] for item in curs.description])


    if not df_4.empty and 'CHANNEL' in df_4.columns and 'SESSION' in df_4.columns:
        fig4 = px.pie(
            df_4,
            names='CHANNEL',
            values='SESSION',
            title="🕎 Distribution of Session by Channel",
            template=plotly_template,
            hole=0.3  # Creates a donut chart
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.write("No data available to display pie chart.")


    #st.plotly_chart(fig4, use_container_width=True)

# Instructions
st.sidebar.write("### Instructions")
st.sidebar.write("- Use the **Category Page** to select specific data categories.")
st.sidebar.write("- Use the **Category Gender** to select specific data categories.")
st.sidebar.write("- **Toggle Theme** to switch between dark and light mode.")
st.sidebar.write("- The dashboard **auto-refreshes every 20 seconds**.")
