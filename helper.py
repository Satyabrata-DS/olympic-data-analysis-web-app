
import pandas as pd
import numpy as np
import streamlit as st


# Fetch Medal Tally
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['NOC'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['NOC'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

# List of countries and years
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(df['NOC'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

# Data over time
def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':col}, inplace=True)
    return nations_over_time





def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN (athletes who didn't win any medals)
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if it's not 'overall'
    if sport.lower() != 'overall':
        temp_df = temp_df[temp_df['Sport'].str.lower() == sport.lower()]  # Filter for specific sport

    # Get the count of medals by athlete
    result = temp_df['Name'].value_counts().reset_index()
    result.columns = ['Name', 'count']

    # Merge to get additional columns (Sport, NOC)
    result = result.merge(df[['Name', 'Sport', 'NOC']], on='Name', how='left')

    # Select only the desired columns
    result = result[['Name', 'count', 'Sport', 'NOC']].drop_duplicates('Name').head(20)

    return result


# Yearwise medal tally
def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['NOC'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


# Country event heatmap
def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['NOC'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


# Most successful athletes country-wise
def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['NOC'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')

    return x
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'NOC'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


def sport_distribution(df):
    """
    This function calculates the number of unique athletes per sport.
    Args:
    - df (pd.DataFrame): DataFrame containing Olympic data.

    Returns:
    - pd.DataFrame: A DataFrame with sports and their respective number of athletes.
    """
    sport_distribution = df.groupby('Sport')['Name'].nunique().reset_index()
    sport_distribution.columns = ['Sport', 'Number of Athletes']

    return sport_distribution







