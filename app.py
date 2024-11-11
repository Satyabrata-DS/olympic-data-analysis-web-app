import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


file_path = 'olympics_dataset.csv'  # Relative path from the project root
df = preprocessor.preprocess(file_path)


# Streamlit Sidebar
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

# Sidebar Menu
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# Medal Tally Section
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Display Title Based on Selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} Overall Performance")
    else:
        st.title(f"{selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# Overall Analysis Section
if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['NOC'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Participating Nations Over Time
    nations_over_time = helper.data_over_time(df, 'NOC')
    fig = px.line(nations_over_time, x="Edition", y="NOC")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    # Events Over Time
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events Over the Years")
    st.plotly_chart(fig)

    # Athletes Over Time
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes Over the Years")
    st.plotly_chart(fig)

    # No of Events Over Time (for Each Sport)
    st.title("Number of Events Over Time (Each Sport)")
    fig, ax = plt.subplots(figsize=(10, 17))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True
    )
    st.pyplot(fig)

    # Most Successful Athletes Analysis
    st.sidebar.header('Select Sport')
    sports = df['Sport'].unique().tolist()
    sports.append('Overall')
    selected_sport = st.sidebar.selectbox('Choose a Sport:', sports)

    results = helper.most_successful(df, selected_sport)
    st.subheader(f'Most Successful Athletes in {selected_sport}')
    st.table(results)

# Country-wise Analysis Section
if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['NOC'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally Over the Years")
    st.plotly_chart(fig)

    # Sports the Country Excels In
    st.title(f"{selected_country} Excels in the Following Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # Top 10 Athletes of the Country
    st.title(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete-wise Analysis Section
if user_menu == 'Athlete-wise Analysis':
    st.sidebar.title('Athlete-wise Analysis')

    # Men vs Women Participation Over the Years
    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # Sport-wise Distribution of Athletes (Bar Chart)
    st.header("Sport-wise Distribution of Athletes")
    unique_athletes_df = df.drop_duplicates(subset=['Name', 'Sport'])
    sportwise_athlete_count = unique_athletes_df.groupby('Sport')['Name'].nunique().reset_index()
    sportwise_athlete_count = sportwise_athlete_count.rename(columns={'Name': 'Athlete Count'})
    sportwise_athlete_count = sportwise_athlete_count.sort_values(by='Athlete Count', ascending=False)

    fig_bar = px.bar(
        sportwise_athlete_count,
        x='Sport',
        y='Athlete Count',
        title='Sport-wise Distribution of Athletes',
        color='Athlete Count'
    )
    st.plotly_chart(fig_bar)

    # Optional Pie Chart Visualization
    fig_pie = px.pie(
        sportwise_athlete_count,
        values='Athlete Count',
        names='Sport',
        title='Sport-wise Athlete Distribution',
        hole=0.3  # Donut chart
    )
    st.plotly_chart(fig_pie)

