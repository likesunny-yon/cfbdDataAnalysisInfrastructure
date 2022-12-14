import pandas as pd

def transform_game_details(df):
    df_get_games_trimmed = df[
        ['id', 'season', 'week', 'season_type', 'start_date', 'completed', 'neutral_site', 'conference_game',
         'attendance', 'venue_id', 'venue', 'home_id', 'home_team', 'home_conference', 'home_division', 'home_points',
         'home_pregame_elo', 'away_id', 'away_team', 'away_conference', 'away_division', 'away_points',
         'away_pregame_elo', 'excitement_index']]

    df_get_games_away = df_get_games_trimmed[['id', 'season', 'week', 'season_type', 'start_date', 'completed',
                                              'neutral_site', 'conference_game', 'attendance', 'venue_id', 'venue',
                                              'home_id', 'home_team', 'away_team', 'home_conference', 'home_division',
                                              'home_points', 'away_points', 'home_pregame_elo', 'away_pregame_elo',
                                              'excitement_index']].rename(
        columns={'home_id': 'team_id', 'home_team': 'team', 'home_conference': 'conference',
                 'home_division': 'division',
                 'home_points': 'points', 'home_pregame_elo': 'pregame_elo', 'away_team': 'opponent',
                 'away_points': 'opponent_points', 'away_pregame_elo': 'opponent_pregame_elo'})

    df_get_games_home = df_get_games_trimmed[['id', 'season', 'week', 'season_type', 'start_date', 'completed',
                                              'neutral_site', 'conference_game', 'attendance', 'venue_id', 'venue',
                                              'away_id', 'away_team', 'home_team',
                                              'away_conference', 'away_division', 'away_points', 'home_points',
                                              'away_pregame_elo', 'home_pregame_elo', 'excitement_index']].rename(
        columns={'away_id': 'team_id', 'away_team': 'team', 'away_conference': 'conference',
                 'away_division': 'division',
                 'away_points': 'points', 'away_pregame_elo': 'pregame_elo', 'home_team': 'opponent',
                 'home_points': 'opponent_points', 'home_pregame_elo': 'opponent_pregame_elo'})

    return pd.concat([df_get_games_home, df_get_games_away], axis=0).reset_index()


def transform_recruiting_stats(df_get_recruiting_groups, df_roster, df_recruits, df_transfer_portal, df_player_stats):
    team_recruiting_avgs = df_get_recruiting_groups.loc[df_get_recruiting_groups['position_group'] == 'All Positions',
                                                        ['team', 'conference', 'position_group', 'average_rating',
                                                         'total_rating', 'commits', 'average_stars']]

    team_recruiting_avgs.rename(columns={'average_rating': 'group_average_rating',
                                         'total_rating': 'group_total_rating',
                                         'commits': 'group_commits',
                                         'average_stars': 'group_average_stars'}, inplace=True)

    df_roster['first_recruit_id'] = df_roster['recruit_ids'].apply(
        lambda x: x[1:-1].split(',')[0] if (len(x[1:-1].split(',')) > 1) else x[1:-1])

    df_recruits['last_name'] = df_recruits['name'].str.split(' ', expand=True)[1]
    df_recruits['id'] = df_recruits['id'].apply(str)

    df_recruits = df_recruits[['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'year',
                               'ranking', 'stars', 'rating', 'committed_to', 'state_province']]

    df_transfer_portal['id'] = None
    df_transfer_portal['athlete_id'] = None
    df_transfer_portal['recruit_type'] = None
    df_transfer_portal['ranking'] = None
    df_transfer_portal['state_province'] = None

    df_transfer_portal['name'] = df_transfer_portal['first_name'] + " " + df_transfer_portal['last_name']
    df_transfer_portal = df_transfer_portal[['name', 'last_name', 'id', 'athlete_id', 'recruit_type', 'season',
                                             'ranking', 'stars', 'rating', 'destination', 'state_province']]
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

    recruited_players_w_stats = combined_recruiting_rosters_df_new.loc[
        combined_recruiting_rosters_df_new.id_x.isin(df_player_stats.player_id.values.tolist())]

    recruited_players_w_stats_sum = recruited_players_w_stats[
        ['team', 'position', 'stars', 'rating', 'ranking']].groupby(['team']).mean()

    total_recruiting_stats = recruited_players_w_stats_sum.merge(team_recruiting_avgs, on=['team'])
    total_recruiting_stats['year'] = '2022'

    return total_recruiting_stats


def merge_game_stats_recruiting(df_get_games_all, pivoted_games_data, df_advanced_game_team_stats,
                                transformed_team_attribute_df, total_recruiting_stats):
    fbs_games = df_get_games_all.loc[df_get_games_all.division == 'fbs']

    basic_enriched_games_data = fbs_games.merge(pivoted_games_data, how='inner', left_on=['id', 'team'],
                                                right_on=['game_id', 'school'])
    advanced_enriched_games_data = basic_enriched_games_data.merge(df_advanced_game_team_stats, how='inner',
                                                                   left_on=['id', 'team'],
                                                                   right_on=['game_id', 'team'])

    recruiting_enriched_team_attributes = transformed_team_attribute_df.merge(total_recruiting_stats, how='inner',
                                                                              left_on=['school'], right_on=['team'])

    advanced_team_enriched_games_data = advanced_enriched_games_data.merge(recruiting_enriched_team_attributes,
                                                                           how='inner', left_on=['school'],
                                                                           right_on=['team']).merge(
        recruiting_enriched_team_attributes[
            ['team', 'group_average_rating', 'group_average_stars', 'stars', 'rating']], how='inner',
        left_on=['opponent_x'], right_on=['team'], suffixes=['_team', '_opponent'])

    advanced_team_enriched_games_data = advanced_team_enriched_games_data[
        ['game_id_x', 'season_x', 'week_x', 'season_type', 'completed', 'team_id', 'team_x', 'conference_x_x',
         'division_x', 'points_x', 'opponent_points', 'pregame_elo',
         'home_away', 'opponent_x', 'stars_team', 'rating_team', 'position_group',
         'group_average_rating_team', 'opponent_pregame_elo', 'logo_primary','logo_alt',
         'group_average_stars_team', 'stars_opponent', 'rating_opponent', 'group_average_rating_opponent',
         'group_average_stars_opponent', 'stat_completionAttempts', 'stat_defensiveTDs', 'stat_firstDowns',
         'stat_fourthDownEff', 'stat_fumblesLost', 'stat_fumblesRecovered',
         'stat_interceptionTDs', 'stat_interceptionYards', 'stat_interceptions',
         'stat_kickReturnTDs', 'stat_kickReturnYards', 'stat_kickReturns',
         'stat_kickingPoints', 'stat_netPassingYards', 'stat_passesDeflected',
         'stat_passesIntercepted', 'stat_passingTDs', 'stat_possessionTime',
         'stat_puntReturnTDs', 'stat_puntReturnYards', 'stat_puntReturns',
         'stat_qbHurries', 'stat_rushingAttempts', 'stat_rushingTDs',
         'stat_rushingYards', 'stat_sacks', 'stat_tackles',
         'stat_tacklesForLoss', 'stat_thirdDownEff', 'stat_totalFumbles',
         'stat_totalPenaltiesYards', 'stat_totalYards', 'stat_turnovers',
         'stat_yardsPerPass', 'stat_yardsPerRushAttempt']].rename(
        columns={'game_id_x': 'game_id', 'season_x': 'season',
                 'week_x': 'week', 'division_x': 'division',
                 'team_x': 'team', 'conference_x_x': 'conference',
                 'points_x': 'points', 'stars_team': 'team_stat_earning_ply_stars',
                 'rating_team': 'team_stat_earning_ply_rating', 'opponent_x': 'opponent'})

    return advanced_team_enriched_games_data


def apply_3w_lookback(advanced_team_enriched_games_data):
    test_advanced_team_enriched_games_data = advanced_team_enriched_games_data.reset_index()
    test_advanced_team_enriched_games_data = test_advanced_team_enriched_games_data.assign(
        total_offense_yards=lambda x: x.stat_netPassingYards + x.stat_rushingYards)

    test_advanced_team_enriched_games_data['third_down_pct'] = test_advanced_team_enriched_games_data[
        'stat_thirdDownEff'].apply(lambda x: int((x.split('-')[0])) / int((x.split('-')[1])))

    test_advanced_team_enriched_games_data = test_advanced_team_enriched_games_data[['game_id','team','week','home_away',
                                                                                     'logo_primary','logo_alt','opponent',
                                                                                     'team_stat_earning_ply_rating','stat_firstDowns',
                                                                                     'rating_opponent','pregame_elo','opponent_pregame_elo',
                                                                                     'total_offense_yards','third_down_pct','points']
                                                                                    ].sort_values(by=['week','team'])

    test_advanced_team_enriched_games_data_lookback = test_advanced_team_enriched_games_data[
        ['team','week','total_offense_yards','third_down_pct','stat_firstDowns','points']].groupby(['team']).transform(
        lambda x: x.rolling(3, 1, closed='left').mean()).rename(
        columns={'total_offense_yards': '3M_lookback_offyards','stat_firstDowns': '3M_lookback_firstDowns',
                 'third_down_pct': '3M_lookback_third_down_pct','points': '3M_lookback_points_scored'})

    test_advanced_team_enriched_games_data[['3M_lookback_offyards','3M_lookback_third_down_pct',
                                            '3M_lookback_points_scored','3M_lookback_firstDowns']] = \
        test_advanced_team_enriched_games_data_lookback[['3M_lookback_offyards','3M_lookback_third_down_pct',
                                                         '3M_lookback_points_scored','3M_lookback_firstDowns']]

    enriched_games_filtered = test_advanced_team_enriched_games_data.dropna().loc[test_advanced_team_enriched_games_data.week > 3]

    enriched_games_filtered = enriched_games_filtered\
        .assign(talent_rating_differential=lambda x: x.team_stat_earning_ply_rating - x.rating_opponent)\
        .assign(elo_differential=lambda x: x.pregame_elo - x.opponent_pregame_elo)

    return enriched_games_filtered


def apply_multiple_linear_regression(enriched_games_filtered, coef_list, y_int):
    enriched_games_filtered_reset = enriched_games_filtered.reset_index()
    enriched_games_filtered_reset = enriched_games_filtered_reset.rename(columns={'3M_lookback_offyards': 'lookback_offyards',
                                                                                  '3M_lookback_third_down_pct': 'lookback_third_down_pct',
                                                                                  '3M_lookback_points_scored': 'lookback_points_scored',
                                                                                  '3M_lookback_firstDowns': 'lookback_firstDowns'})
    #prediction_data_set = enriched_games_filtered_reset[
    #    ['points', 'talent_rating_differential', 'elo_differential', '3M_lookback_offyards',
    #     '3M_lookback_third_down_pct', '3M_lookback_points_scored', '3M_lookback_firstDowns']]

    #x = prediction_data_set.drop(columns='points')
    #y = prediction_data_set['points']

    #lr = LinearRegression()
    #lr.fit(x, y)

    #print(f"y intercept: {lr.intercept_}")
    #print(f"independent variable coefficients: {lr.coef_}")

    #y_pred_train = lr.predict(x)

    #print(f"training_r2_score: {r2_score(y, y_pred_train)}")

    prediction_output_data_set = enriched_games_filtered_reset.assign(predicted_score = lambda x: x.talent_rating_differential*coef_list[0] +
                                                                                                       x.elo_differential*coef_list[1] +
                                                                                                       x.lookback_offyards*coef_list[2] +
                                                                                                       x.lookback_third_down_pct*coef_list[3] +
                                                                                                       x.lookback_points_scored*coef_list[4] +
                                                                                                       x.lookback_firstDowns*coef_list[5]
                                                                                                       + y_int)
    #prediction_output_data_set = enriched_games_filtered_reset
    #prediction_output_data_set['predicted_score'] = pd.Series(y_pred_train)

    return prediction_output_data_set

def modify_game_line_output(prediction_output_data_set, betting_lines_df):
    prediction_output_data_set_home = prediction_output_data_set.loc[
        prediction_output_data_set.home_away == 'home', ['game_id', 'week', 'team', 'logo_primary', 'pregame_elo',
                                                         'team_stat_earning_ply_rating', 'predicted_score']]\
        .rename(columns={'team': 'home','logo_primary': 'home_logo','pregame_elo': 'home_elo',
                 'team_stat_earning_ply_rating': 'home_talent_rating','predicted_score': 'home_pred_points'})

    prediction_output_data_set_away = prediction_output_data_set.loc[
        prediction_output_data_set.home_away == 'away', ['game_id', 'week', 'team', 'logo_primary', 'pregame_elo',
                                                         'team_stat_earning_ply_rating', 'predicted_score']]\
        .rename(columns={'team': 'away','logo_primary': 'away_logo','pregame_elo': 'away_elo',
                 'team_stat_earning_ply_rating': 'away_talent_rating','predicted_score': 'away_pred_points'})

    game_lines_output_pre_spread = prediction_output_data_set_home.merge(prediction_output_data_set_away, how='inner',
                                                                         on=['game_id', 'week'])

    betting_lines_df['formatted_spread'] = betting_lines_df['lines'].apply(
        lambda x: eval(x)[-1]['formatted_spread'] if len(eval(x)) > 0 else 'Unkown')
    betting_lines_df['over_under'] = betting_lines_df['lines'].apply(
        lambda x: eval(x)[-1]['over_under'] if len(eval(x)) > 0 else 'Unkown')
    df_betting_lines_adjusted = betting_lines_df.drop(columns='lines')
    filtered_betting_lines = df_betting_lines_adjusted[['id', 'week', 'formatted_spread', 'over_under']]

    game_lines = game_lines_output_pre_spread.merge(filtered_betting_lines, how='inner',
                                                           left_on=['game_id', 'week'], right_on=['id', 'week'])

    game_lines_output = game_lines[
        ['game_id', 'week', 'home', 'away', 'home_logo', 'away_logo', 'home_elo', 'away_elo', 'home_talent_rating',
         'away_talent_rating', 'home_pred_points', 'away_pred_points', 'formatted_spread', 'over_under']].rename(
        columns={'formatted_spread': 'betting_spread', 'over_under': 'betting_o_u'})

    return game_lines_output
