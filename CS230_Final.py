# Eric Figueroa | Professor Xu | CS230-4 | Final Project
"""
Name:   Eric Figueroa
CS230:  Section 4
Data: Fortune_500_hq
URL:
Description: This program includes a variety of data and visualizations that highlight the companies that are
part of the Fortune 500. Included in this site are maps, tables, charts, and graphs that display the data about
these companies' headquarters locations such as where they are located, which states have the most companies
headquartered there, and other cool things you might not have previously known about the most valuable
companies in the world.


"""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk


path = "C:/Users/ericf/OneDrive - Bentley University/pythonProject/pythonProject1/"

df_hqstates = pd.read_csv(path + 'fortune_500_hq.csv')

# FUNCTION THAT RETURNS MORE THAN ONE VALUE [PY1]
def states_with_most_hqs(df, n=10):
    state_counts = df["STATE"].value_counts().reset_index()
    state_counts.columns = ["State", "Number of Companies"]
    top_states = state_counts.head(n)
    return top_states


st.sidebar.title("Page Navigation")
page = st.sidebar.radio("Select how you want to see the data:", ["Home", "Tables", "Map", "State Search", "Interactive County HQs"])

# HOME page
if page == "Home":
    st.title("Fortune 500 Companies Dashboard by Eric Figueroa\n")

    # IMAGE ON INTRODUCTION PAGE [ST4]
    st.image("https://fortune.com/img-assets/wp-content/uploads/2023/10/500_logo.jpg", caption="Fortune 500 Companies", use_container_width=True)

    st.header(" Hello, and welcome to my page on Fortune 500 companies! Here, you can explore data and insights about some of the largest companies in the world.")

    st.write("""
    Use the navigation on the left to get started and explore different sections of this website.
    Data in this page includes: 
    \n- States with the most Fortune 500 Company Headquarters
    \n- New England States that have Fortune 500 Company Headquarters
    \n- A pivot table where you can see which companies have the most employees
    \n- A map of the United States with the locations of the Fortune 500 Company Headquarters
    \n- A state search text box where you can type any state and the program will show you which companies are headquartered in that state
    \n- An interactive bar chart where you can select a state and the program will return a bar chart that shows the distribution of HQs in each county
    """)

elif page == "Tables":
    st.title("Fortune 500 Company Tables")

    # USER INPUT FOR TOP STATES TO DISPLAY
    st.subheader("Company Headuarters by State")        # [VIZ1] TABLE WITH COMPANY HQ BY STATE
    num_states = st.text_input("Enter the number of states you want to see:", value="10")

    try:         # [PY3] ERROR CHECKING WITH TRY/EXCEPT - APPEARANCE OF TABLE AND TRY/EXCEPT VALIDATION BASED ON CODE FROM CHATGPT
        num_states = int(num_states)
        if num_states < 1 or num_states > 38:
            st.error("Invalid input. Please enter a number between 1-38.")
        else:
            top_states = states_with_most_hqs(df_hqstates, n=num_states)
            st.table(top_states)
    except ValueError:
        st.error("Invalid input. Please enter a number between 1-38.")

    # [PY5] DICTIONARY OF NEW ENGLAND STATES
    new_england_states = {"ME": "Maine", "NH": "New Hampshire", "VT": "Vermont",
                          "MA": "Massachusetts", "RI": "Rhode Island", "CT": "Connecticut"}

    st.write("Dictionary of New England States and their Abbreviations:")
    for abbr, name in new_england_states.items():
        st.write(f"{abbr}: {name}")

    # Filter and count the number of companies headquartered in New England states
    new_england_counts = df_hqstates["STATE"].value_counts().reset_index()
    new_england_counts.columns = ["State", "Number of Companies"]
    new_england_counts = new_england_counts[new_england_counts["State"].isin(new_england_states.keys())]

    # [VIZ2] TABLE OF NEW ENGLAND STATES AND THE COMPANIES WITH HQ THERE
    st.subheader("Fortune 500 Companies Count in New England States")
    st.table(new_england_counts)


# [DA6] INTERACTIVE PIVOT TABLE
    st.subheader("Interactive Employee Pivot Table")

    max_employees = df_hqstates["EMPLOYEES"].max()

    # [ST1] SLIDER TO SET MINIMUM NUMBER OF EMPLOYEES IN PIVOT TABLE - SLIDER BASED ON CODE FROM CHATGPT
    employee_filter = st.slider(
        "Filter companies by minimum number of employees:",
        min_value=0,
        max_value=int(max_employees),
        value=0,  # Default value
        step=10000
    )

    # [DA2] SORT DATA IN ASCENDING/DESCENDING ORDER
    sort_order = st.radio("Select order to display the table:", ("Ascending", "Descending"))

    # [DA9] PERFORM CALCULATIONS ON THE EMPLOYEE COLUMN AND ONLY SHOW THE STATES WITH SPECIFIED # OF EMPLOYEES
    filtered_df = df_hqstates[df_hqstates["EMPLOYEES"] >= employee_filter]
    ascending = sort_order == "Ascending"
    sorted_df = filtered_df.sort_values(by="EMPLOYEES", ascending=ascending)

    # [DA7] ADD/DROP COLUMN DATA
    pivot_table = sorted_df[["EMPLOYEES", "NAME", "CITY", "STATE"]]
    st.table(pivot_table)


# [MAP] REQUIREMENT - Pydeck and Tooltip were based on code from ChatGPT
elif page == "Map":
    st.title("Interactive Map of Fortune 500 Company Headquarters")

    # [DA1] CLEAN/MANIPULATE DATA TO EXTRACT LAT/LON FOR MAP
    if "LATITUDE" in df_hqstates.columns and "LONGITUDE" in df_hqstates.columns:
        map_data = df_hqstates[["LATITUDE", "LONGITUDE", "NAME"]].dropna()

        # Define the PyDeck layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position=["LONGITUDE", "LATITUDE"],
            get_radius=10000,  # Radius of the markers
            get_fill_color=[255, 0, 0, 160],  # Red color with transparency
            pickable=True,)  # Enable hover interactions


        # Define the initial view state
        view_state = pdk.ViewState(
            latitude=map_data["LATITUDE"].mean(),
            longitude=map_data["LONGITUDE"].mean(),
            zoom=4,
            pitch=0,)

        # Tooltip for interactivity
        tooltip = {
            "html": "<b>Company:</b> {NAME}",
            "style": {"color": "white", "backgroundColor": "black", "padding": "5px"}
        }

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))

    else:
        st.error("The dataset does not contain 'LATITUDE' and 'LONGITUDE' columns for mapping!")

# STATE SEARCH PAGE
elif page == "State Search":
    st.title("Search for Companies by State")

    # [ST2] TEXT BOX FOR USER TO INSERT STATE
    state_input = st.text_input("Enter the state abbreviation (e.g., CA, NY, TX):").upper()

    if state_input:
        # Filter the dataset for companies headquartered in the input state [DA4]
        state_companies = df_hqstates[df_hqstates["STATE"] == state_input]

        if not state_companies.empty:
            # Display the companies
            st.write(f"Companies headquartered in {state_input}:")
            st.table(state_companies[["NAME", "CITY", "ADDRESS"]])
        else:
            # Show a message if no companies are found
            st.write(f"No Fortune 500 companies are headquartered in {state_input}.")

# BAR CHART PAGE
elif page == "Interactive County HQs":
    st.title("Interactive Bar Chart: Companies by County")

    state_options = sorted(df_hqstates["STATE"].unique())

    # [ST3] DROP DOWN BOX FOR USER TO SELECT STATE
    state_input = st.selectbox("Select a state:", options=state_options)

    state_data = df_hqstates[df_hqstates["STATE"] == state_input]

    if not state_data.empty:
        # Count the number of companies in each county
        county_counts = state_data["COUNTY"].value_counts()

        num_counties = len(county_counts)
        colors = plt.cm.tab20.colors  # Use a colormap with 20 distinct colors
        bar_colors = [colors[i % len(colors)] for i in range(num_counties)] # <<<<< [PY4] LIST COMPREHENSION

# [VIZ3] BAR CHART - BAR CHART COLORS AND APPEARANCE BASED ON CODE FROM CHATGPT
        fig, ax = plt.subplots(figsize=(10, 6))
        county_counts.plot(kind='bar', ax=ax, color=bar_colors)
        ax.set_title(f"Number of Companies Headquartered in Each County of {state_input}", fontsize=16)
        ax.set_xlabel("County", fontsize=12)
        ax.set_ylabel("Number of Companies", fontsize=12)
        plt.xticks(rotation=45, ha='right')

        st.pyplot(fig)
    else:
        st.error(f"No data available for state: {state_input}.")

