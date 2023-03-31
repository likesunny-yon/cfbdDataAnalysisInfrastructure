import pandas as pd
import cfbd_data.utilities.utility_functions as utilities
from cfbd_data.utilities.constants import *


def transform_game_details(input_df):

        df_get_games_trimmed = input_df[df_get_games_trimmed_columns]

        df_get_games_away = df_get_games_trimmed[df_get_games_away_columns]\
                                .rename( columns=df_get_games_away_rename_dict)\
                                .assign(home_away='away')
        df_get_games_home = df_get_games_trimmed[df_get_games_home_columns]\
                                .rename(columns=df_get_games_home_rename_dict)\
                                .assign(home_away='home')

        df_get_games_all = pd.concat([df_get_games_home, df_get_games_away], axis=0).reset_index()
        return df_get_games_all

def recruiting_transformation(df_player_stats, df_roster,
                              df_recruits, df_transfer_portal,
                              df_get_recruiting_groups, year):

    team_recruiting_avgs = df_get_recruiting_groups.loc[
        df_get_recruiting_groups['position_group'] == 'All Positions', ['team', 'conference', 'position_group',
                                                                        'average_rating', 'total_rating', 'commits',
                                                                        'average_stars']]
    team_recruiting_avgs.rename(columns={'average_rating': 'group_average_rating',
                                         'total_rating': 'group_total_rating',
                                         'commits': 'group_commits',
                                         'average_stars': 'group_average_stars'}, inplace=True)

    df_roster['first_recruit_id'] = df_roster['recruit_ids'].apply(
        lambda x: x[1:-1].split(',')[0] if (len(x[1:-1].split(',')) > 1) else x[1:-1])

    df_recruits['last_name'] = df_recruits['name'].str.split(' ', expand=True)[1]
    df_recruits['id'] = df_recruits['id'].apply(str)

    df_recruits = df_recruits[
        ['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'year', 'ranking', 'stars', 'rating', 'committed_to',
         'state_province']]

    df_transfer_portal['id'] = None
    df_transfer_portal['athlete_id'] = None
    df_transfer_portal['recruit_type'] = None
    df_transfer_portal['ranking'] = None
    df_transfer_portal['state_province'] = None

    df_transfer_portal['name'] = df_transfer_portal['first_name'] + " " + df_transfer_portal['last_name']
    df_transfer_portal = df_transfer_portal[
        ['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'season', 'ranking', 'stars', 'rating', 'destination',
         'state_province']]
    df_transfer_portal.rename({'season': 'year', 'destination': 'committed_to'}, inplace=True)

    df_recruits_expanded = pd.concat([df_recruits, df_transfer_portal], ignore_index=True)

    roster_missing_id = df_roster.loc[df_roster['first_recruit_id'] == '']
    roster_including_id = df_roster.loc[df_roster['first_recruit_id'] != '']

    main_recruiting_rosters_df = roster_including_id.merge(df_recruits_expanded, 'inner',
                                                           left_on=['team', 'first_recruit_id'],
                                                           right_on=['committed_to', 'id'])

    secondary_recruiting_rosters_df = roster_missing_id.merge(df_recruits_expanded, 'inner',
                                                              left_on=['team', 'last_name', 'home_state'],
                                                              right_on=['committed_to', 'last_name', 'state_province'])

    combined_recruiting_rosters_df_new = pd.concat([main_recruiting_rosters_df, secondary_recruiting_rosters_df],
                                                   ignore_index=True)

    print(df_player_stats.columns)
    recruited_players_w_stats = combined_recruiting_rosters_df_new.loc[
        combined_recruiting_rosters_df_new.id_x.isin(df_player_stats.playerId.values.tolist())]

    recruited_players_w_stats_sum = recruited_players_w_stats[
        ['team', 'position', 'stars', 'rating', 'ranking']].groupby(['team']).mean()

    total_recruiting_stats = recruited_players_w_stats_sum.merge(team_recruiting_avgs, on=['team'])
    total_recruiting_stats['year'] = year

    return total_recruiting_stats

def apply_rolling_lookback(input_df, group_by_col, return_cols,
                           sort_col=None, rename_dict=None, lookback_periods=3):
    input_df_lookback = input_df[
        advanced_team_enriched_games_data_lookback_columns].sort_values(
        by=sort_col).groupby([group_by_col]).transform(lambda x: x.rolling(3, 1, closed='left').mean()) \
        .rename(columns=rename_dict)
    # TODO need to test that the above lookback works as expected
    return input_df_lookback[return_cols]

def prep_default_forecasting_dataset(pivoted_games_data, total_recruiting_stats,
                                     df_advanced_game_team_stats, df_get_games_all,
                                     weekly_adjusted_ppa_df, df_team):
    #TODO enable lookback to work effectively

    # merge game details, team game stats, and recruiting team data
    print(f"df_get_games_all: {df_get_games_all.loc[df_get_games_all.team == 'Washington']}")
    print(f"pivoted_games_data: {pivoted_games_data.loc[pivoted_games_data.school == 'Washington']}")
    basic_enriched_games_data = df_get_games_all.merge(pivoted_games_data, how='left', left_on=['id', 'team'],
                                                       right_on=['game_id', 'school'])

    print(f"basic_enriched_games_data: {basic_enriched_games_data.loc[basic_enriched_games_data.team == 'Washington']}")
    print(
        f"df_advanced_game_team_stats: {df_advanced_game_team_stats.loc[df_advanced_game_team_stats.team == 'Washington']}")
    advanced_enriched_games_data = basic_enriched_games_data.merge(df_advanced_game_team_stats, how='left',
                                                                   left_on=['id', 'team'], right_on=['game_id', 'team'])
    print(
        f"advanced_enriched_games_data: {advanced_enriched_games_data.loc[advanced_enriched_games_data.team == 'Washington']}")

    recruiting_enriched_team_attributes = df_team.merge(total_recruiting_stats, how='left',
                                                                              left_on=['school'], right_on=['team'])
    print(
        f"advanced_enriched_games_data: {advanced_enriched_games_data.loc[advanced_enriched_games_data.team == 'Washington']}")
    print(
        f"recruiting_enriched_team_attributes: {recruiting_enriched_team_attributes.loc[recruiting_enriched_team_attributes.team == 'Washington']}")

    advanced_team_enriched_games_data = advanced_enriched_games_data.merge(recruiting_enriched_team_attributes,
                                                                           how='left', left_on=['team'],
                                                                           right_on=['team']) \
        .merge(
        recruiting_enriched_team_attributes[['team', 'group_average_rating', 'group_average_stars', 'stars', 'rating']],
        how='left', left_on=['opponent_x'], right_on=['team'], suffixes=['_team', '_opponent'])

    advanced_team_enriched_games_data = advanced_team_enriched_games_data[advanced_team_enriched_games_data_columns]\
                                        .rename(columns=advanced_team_enriched_games_data_rename_dict)

    print(f"advanced_team_enriched_games_data.loc[advanced_team_enriched_games_data.team == 'Washington']: {advanced_team_enriched_games_data.loc[advanced_team_enriched_games_data.team == 'Washington']}")
    advanced_team_enriched_games_data = advanced_team_enriched_games_data.assign(
        total_offense_yards=lambda x: x.stat_netPassingYards + x.stat_rushingYards)

    advanced_team_enriched_games_data['third_down_pct'] = None

    advanced_team_enriched_games_data.loc[(advanced_team_enriched_games_data.completed == True) & (
        ~advanced_team_enriched_games_data.stat_thirdDownEff.isnull()), 'third_down_pct'] \
        = advanced_team_enriched_games_data.loc[(advanced_team_enriched_games_data.completed == True) & (
        ~advanced_team_enriched_games_data.stat_thirdDownEff.isnull()), 'stat_thirdDownEff'] \
        .apply(lambda x: utilities.divide_string(x))

    advanced_team_enriched_games_data = advanced_team_enriched_games_data[
        ['game_id', 'completed', 'team', 'week', 'season_type', 'home_away', 'logo_primary', 'logo_alt', 'opponent',
         'team_stat_earning_ply_rating', 'stat_firstDowns', 'rating_opponent', 'pregame_elo', 'opponent_pregame_elo',
         'total_offense_yards', 'third_down_pct', 'points']].sort_values(by=['week', 'team'])

    max_week = int(max(advanced_team_enriched_games_data['week']))
    advanced_team_enriched_games_data['adjusted_week'] = advanced_team_enriched_games_data['week']
    advanced_team_enriched_games_data.loc[
        advanced_team_enriched_games_data.season_type == 'postseason', ['adjusted_week']] += max_week

    advanced_team_enriched_games_data[lookback_enrichment_columns] = apply_rolling_lookback(advanced_team_enriched_games_data,
                                                                                            'team',
                                                                                            lookback_enrichment_columns,
                                                                                            'adjusted_week',
                                                                                            advanced_team_enriched_games_data_lookback_rename_dict)

    enriched_games_filtered = advanced_team_enriched_games_data.loc[advanced_team_enriched_games_data.adjusted_week > 3]
    print(
        f"enriched_games_filtered.loc[enriched_games_filtered.team == 'Washington']: {enriched_games_filtered.loc[enriched_games_filtered.team == 'Washington']}")

    enriched_games_filtered = enriched_games_filtered.assign(
        talent_rating_differential=lambda x: x.team_stat_earning_ply_rating - x.rating_opponent).assign(
        elo_differential=lambda x: x.pregame_elo - x.opponent_pregame_elo)
    fbs_enriched_games_filtered = enriched_games_filtered.loc[
        (enriched_games_filtered.team.isin(df_team.school.to_list())) & (
            enriched_games_filtered.opponent.isin(df_team.school.to_list()))]

    fbs_enriched_games_filtered = fbs_enriched_games_filtered.merge(
        weekly_adjusted_ppa_df[['school', 'week', 'adjOff']], how='left', left_on=['team', 'week'],
        right_on=['school', 'week'])
    fbs_enriched_games_filtered = fbs_enriched_games_filtered.merge(
        weekly_adjusted_ppa_df[['school', 'week', 'adjDef']], how='left', left_on=['opponent', 'week'],
        right_on=['school', 'week']).drop(columns=['school_x', 'school_y'])
    fbs_enriched_games_filtered.dropna(subset=['talent_rating_differential'], inplace=True)

    return fbs_enriched_games_filtered



# def apply_3w_lookback(advanced_team_enriched_games_data):
#     test_advanced_team_enriched_games_data = advanced_team_enriched_games_data.reset_index()
#     test_advanced_team_enriched_games_data = test_advanced_team_enriched_games_data.assign(
#         total_offense_yards=lambda x: x.stat_netPassingYards + x.stat_rushingYards)
#
#     test_advanced_team_enriched_games_data['third_down_pct'] = test_advanced_team_enriched_games_data[
#         'stat_thirdDownEff'].apply(lambda x: int((x.split('-')[0])) / int((x.split('-')[1])))
#
#     test_advanced_team_enriched_games_data = test_advanced_team_enriched_games_data[['game_id','team','week','home_away',
#                                                                                      'logo_primary','logo_alt','opponent',
#                                                                                      'team_stat_earning_ply_rating','stat_firstDowns',
#                                                                                      'rating_opponent','pregame_elo','opponent_pregame_elo',
#                                                                                      'total_offense_yards','third_down_pct','points']
#                                                                                     ].sort_values(by=['week','team'])
#
#     test_advanced_team_enriched_games_data_lookback = test_advanced_team_enriched_games_data[
#         ['team','week','total_offense_yards','third_down_pct','stat_firstDowns','points']].groupby(['team']).transform(
#         lambda x: x.rolling(3, 1, closed='left').mean()).rename(
#         columns={'total_offense_yards': '3M_lookback_offyards','stat_firstDowns': '3M_lookback_firstDowns',
#                  'third_down_pct': '3M_lookback_third_down_pct','points': '3M_lookback_points_scored'})
#
#     test_advanced_team_enriched_games_data[['3M_lookback_offyards','3M_lookback_third_down_pct',
#                                             '3M_lookback_points_scored','3M_lookback_firstDowns']] = \
#         test_advanced_team_enriched_games_data_lookback[['3M_lookback_offyards','3M_lookback_third_down_pct',
#                                                          '3M_lookback_points_scored','3M_lookback_firstDowns']]
#
#     enriched_games_filtered = test_advanced_team_enriched_games_data.dropna().loc[test_advanced_team_enriched_games_data.week > 3]
#
#     enriched_games_filtered = enriched_games_filtered\
#         .assign(talent_rating_differential=lambda x: x.team_stat_earning_ply_rating - x.rating_opponent)\
#         .assign(elo_differential=lambda x: x.pregame_elo - x.opponent_pregame_elo)
#
#     return enriched_games_filtered



