import os
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper


@st.cache_data
def load_data():
    # deploy ke liye compressed file (.gz), local par normal csv bhi chalegi
    path = 'athlete_events.csv.gz' if os.path.exists('athlete_events.csv.gz') else 'athlete_events.csv'
    df = pd.read_csv(path, encoding='latin1')
    region_df = pd.read_csv('noc_regions.csv', encoding='latin1')
    return preprocessor.preprocess(df, region_df)


df = load_data()

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    "Select an option",
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.dataframe(tally, use_container_width=True)

elif user_menu == 'Overall Analysis':
    st.title("Top Statistics")
    stats = helper.top_stats(df)

    cols = st.columns(3)
    for i, (name, value) in enumerate(stats.items()):
        cols[i % 3].metric(name, f"{value:,}")

    st.divider()
    nations = helper.data_over_time(df, 'region')
    fig = px.line(nations, x='Year', y='Count', title="Participating Nations over the years")
    st.plotly_chart(fig, use_container_width=True)

    events = helper.data_over_time(df, 'Event')
    fig = px.line(events, x='Year', y='Count', title="Events over the years")
    st.plotly_chart(fig, use_container_width=True)

    athletes = helper.data_over_time(df, 'Name')
    fig = px.line(athletes, x='Year', y='Count', title="Athletes over the years")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("No. of Events over time (Every Sport)")
    heat = helper.events_heatmap_data(df)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(heat, annot=True, fmt='d', cbar=False, ax=ax)
    st.pyplot(fig)

    st.divider()
    st.subheader("Most successful Athletes")
    selected_sport = st.selectbox("Select a Sport", helper.sport_list(df))
    st.dataframe(helper.most_successful(df, selected_sport), use_container_width=True)

elif user_menu == 'Country-wise Analysis':
    st.sidebar.header("Country-wise Analysis")
    country = st.sidebar.selectbox("Select a Country", helper.country_list(df))

    st.title(f"{country} Medal Tally over the years")
    yearwise = helper.yearwise_medal_tally(df, country)
    if yearwise.empty:
        st.info(f"{country} ne is data mein koi medal nahi jeeta.")
    else:
        fig = px.line(yearwise, x='Year', y='Medals', markers=True)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.subheader(f"{country} excels in the following sports")
        heat = helper.country_event_heatmap(df, country)
        fig, ax = plt.subplots(figsize=(20, max(6, len(heat) * 0.6)))
        sns.heatmap(heat, annot=True, fmt='d', cbar=False, ax=ax)
        st.pyplot(fig)

        st.divider()
        st.subheader(f"Top 10 athletes of {country}")
        st.dataframe(helper.most_successful_countrywise(df, country), use_container_width=True)

elif user_menu == 'Athlete-wise Analysis':
    st.title("Age Distribution of Athletes")
    ages = helper.age_distribution(df)
    fig = px.histogram(ages, x='Age', color='Group', barmode='overlay',
                       histnorm='probability density', opacity=0.6, nbins=40)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Height vs Weight")
    sports = helper.sport_list(df)[1:]
    default = sports.index('Athletics') if 'Athletics' in sports else 0
    selected_sport = st.selectbox("Select a Sport", sports, index=default)
    hw = helper.weight_v_height(df, selected_sport)
    if hw.empty:
        st.info("Is sport ke liye height/weight ka data nahi hai.")
    else:
        st.caption("Zyada athletes hone par 5000 random points dikhaye jaate hain.")
        fig = px.scatter(hw, x='Weight', y='Height', color='Medal', symbol='Sex',
                         hover_name='Name', opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Men vs Women Participation over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(yaxis_title='Athletes')
    st.plotly_chart(fig, use_container_width=True)
