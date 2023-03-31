from cfbd_data.utilities.constants import *
def modify_game_line_output(enriched_games_filtered_df, betting_lines_df):
    prediction_output_data_set_home = enriched_games_filtered_df.loc[
        enriched_games_filtered_df.home_away == 'home', prediction_output_data_set_home_columns] \
        .rename(columns=prediction_output_data_set_home_rename_dict)

    prediction_output_data_set_away = enriched_games_filtered_df.loc[
        enriched_games_filtered_df.home_away == 'away', prediction_output_data_set_away_columns] \
        .rename(
        columns=prediction_output_data_set_away_rename_dict)

    game_lines_output_pre_spread = prediction_output_data_set_home.merge(prediction_output_data_set_away, how='inner',
                                                                         on=['game_id', 'week'])
    print(f"game_lines_output_pre_spread: {game_lines_output_pre_spread}")

    betting_lines_df['formatted_spread'] = betting_lines_df['lines'].apply(
        lambda x: eval(x)[-1]['formatted_spread'] if len(eval(x)) > 0 else 'Unkown')
    betting_lines_df['over_under'] = betting_lines_df['lines'].apply(
        lambda x: eval(x)[-1]['over_under'] if len(eval(x)) > 0 else 'Unkown')
    df_betting_lines_adjusted = betting_lines_df.drop(columns='lines')
    filtered_betting_lines = df_betting_lines_adjusted[['id', 'week', 'formatted_spread', 'over_under']]
    print(f"filtered_betting_lines: {filtered_betting_lines}")

    game_lines_output = game_lines_output_pre_spread.merge(filtered_betting_lines, how='left',
                                                           left_on=['game_id', 'week'], right_on=['id', 'week'])
    # TODO: fix join logic above, game_id is null in some cases
    print(f"game_lines_output: {game_lines_output}")

    game_lines_output['home_pred_points'] = game_lines_output['home_pred_points'].apply(lambda x: round(x))
    game_lines_output['away_pred_points'] = game_lines_output['away_pred_points'].apply(lambda x: round(x))

    prediction_output_df = game_lines_output[prediction_output_df_columns].rename(
        columns=prediction_output_df_rename_dict)

    print(f"prediction_output_df: {prediction_output_df}")
    return prediction_output_df