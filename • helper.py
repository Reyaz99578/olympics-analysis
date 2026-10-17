import pandas as pd

MEDAL_KEY = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']


# ---------- Medal Tally ----------

def country_year_list(df):
    years = sorted(df['Year'].dropna().unique().astype(int).tolist())
    years.insert(0, 'Overall')

    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')
    return years, countries


def fetch_medal_tally(df, year, country):
    # team event ka ek hi medal gino
    medal_df = df.drop_duplicates(subset=MEDAL_KEY)

    country_wise = False
    if year == 'Overall' and country == 'Overall':
        temp = medal_df
    elif year == 'Overall':
        country_wise = True
        temp = medal_df[medal_df['region'] == country]
    elif country == 'Overall':
        temp = medal_df[medal_df['Year'] == int(year)]
    else:
        temp = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    medals = ['Gold', 'Silver', 'Bronze']
    if country_wise:
        x = temp.groupby('Year')[medals].sum().sort_index().reset_index()
    else:
        x = temp.groupby('region')[medals].sum().sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


# ---------- Overall Analysis ----------

def top_stats(df):
    # 1906 ke games official count mein nahi aate, isliye 1 ghataya
    editions = df['Year'].nunique() - 1
    return {
        'Editions': editions,
        'Hosts': df['City'].nunique(),
        'Sports': df['Sport'].nunique(),
        'Events': df['Event'].nunique(),
        'Athletes': df['Name'].nunique(),
        'Nations': df['region'].nunique(),
    }


def data_over_time(df, col):
    # har saal mein `col` ki kitni alag values thi
    x = df.drop_duplicates(['Year', col]).groupby('Year').size().reset_index(name='Count')
    return x.sort_values('Year')


def events_heatmap_data(df):
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pt = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
    return pt.fillna(0).astype(int)


def sport_list(df):
    sports = sorted(df['Sport'].dropna().unique().tolist())
    sports.insert(0, 'Overall')
    return sports


def most_successful(df, sport='Overall', top=15):
    temp = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp = temp[temp['Sport'] == sport]

    medals = temp.groupby('Name').size().reset_index(name='Medals')
    medals = medals.sort_values('Medals', ascending=False).head(top)

    info = df[['Name', 'Sport', 'region']].drop_duplicates('Name')
    out = medals.merge(info, on='Name', how='left')
    return out.rename(columns={'region': 'Country'}).reset_index(drop=True)


# ---------- Country-wise Analysis ----------

def country_list(df):
    return sorted(df['region'].dropna().unique().tolist())


def _country_medals(df, country):
    # team event ka ek hi medal gino, sirf us country ke
    temp = df.dropna(subset=['Medal']).drop_duplicates(subset=MEDAL_KEY)
    return temp[temp['region'] == country]


def yearwise_medal_tally(df, country):
    temp = _country_medals(df, country)
    return temp.groupby('Year').size().reset_index(name='Medals').sort_values('Year')


def country_event_heatmap(df, country):
    temp = _country_medals(df, country)
    pt = temp.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count')
    return pt.fillna(0).astype(int)


def most_successful_countrywise(df, country, top=10):
    temp = df.dropna(subset=['Medal'])
    temp = temp[temp['region'] == country]

    medals = temp.groupby('Name').size().reset_index(name='Medals')
    medals = medals.sort_values('Medals', ascending=False).head(top)

    info = temp[['Name', 'Sport']].drop_duplicates('Name')
    return medals.merge(info, on='Name', how='left').reset_index(drop=True)


# ---------- Athlete-wise Analysis ----------

def age_distribution(df):
    # har athlete ek baar gino (Name + country se)
    base = df.dropna(subset=['Age'])
    groups = {
        'Overall': base.drop_duplicates(['Name', 'region']),
        'Gold Medalist': base[base['Medal'] == 'Gold'].drop_duplicates(['Name', 'region']),
        'Silver Medalist': base[base['Medal'] == 'Silver'].drop_duplicates(['Name', 'region']),
        'Bronze Medalist': base[base['Medal'] == 'Bronze'].drop_duplicates(['Name', 'region']),
    }
    parts = [g[['Age']].assign(Group=name) for name, g in groups.items() if not g.empty]
    return pd.concat(parts, ignore_index=True)


def weight_v_height(df, sport, max_points=5000):
    # har athlete ka sabse accha medal rakho
    rank = {'Gold': 3, 'Silver': 2, 'Bronze': 1}
    temp = df[df['Sport'] == sport].copy()
    temp['_rank'] = temp['Medal'].map(rank).fillna(0)
    temp = temp.sort_values('_rank', ascending=False).drop_duplicates(['Name', 'region'])
    temp['Medal'] = temp['Medal'].fillna('No Medal')
    temp = temp.dropna(subset=['Height', 'Weight'])
    if len(temp) > max_points:
        temp = temp.sample(max_points, random_state=1)
    return temp[['Name', 'Height', 'Weight', 'Medal', 'Sex']]


def men_vs_women(df):
    # har saal mein har athlete ek baar
    temp = df.drop_duplicates(['Year', 'Name'])
    x = temp.groupby(['Year', 'Sex']).size().unstack(fill_value=0)
    x = x.reindex(columns=['M', 'F'], fill_value=0)
    x.columns = ['Male', 'Female']
    return x.reset_index().sort_values('Year')
