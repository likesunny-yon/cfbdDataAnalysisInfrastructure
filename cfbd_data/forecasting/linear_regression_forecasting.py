import pandas as pd
import datetime
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import cfbd_data.utilities.utility_functions as utilities
from cfbd_data.utilities.constants import *


def apply_multiple_linear_regression(enriched_games_filtered_df, week=None, season_type=None):

    print(enriched_games_filtered_df)
    if week:
        prediction_data_set = enriched_games_filtered_df.loc[
            (enriched_games_filtered_df.week == week) & (enriched_games_filtered_df.season_type == season_type),
            prediction_data_set_columns].dropna()
        fit_data_set = enriched_games_filtered_df.loc[
            (enriched_games_filtered_df.week != week) | (enriched_games_filtered_df.season_type != season_type),
            fit_data_set_columns].dropna()
        enriched_games_filtered_df = enriched_games_filtered_df.loc[
            (enriched_games_filtered_df.week == week) & (enriched_games_filtered_df.season_type == season_type)]
    print(f"fit_data_set: {fit_data_set.dtypes}")
    print(f"prediction_data_set: {prediction_data_set[prediction_data_set.isna().any(axis=1)]}")

    x = fit_data_set.drop(columns='points')
    y = fit_data_set['points']

    lr = LinearRegression()

    lr.fit(x, y)

    c = lr.intercept_
    print(f"y intercept: {c}")

    m = lr.coef_
    print(f"independent variable coefficients: {m}")

    r2 = r2_score(y, lr.predict(x))
    print(f"r2 score: {r2}")
    y_pred_train = lr.predict(prediction_data_set)

    enriched_games_filtered_df['predicted_score'] = pd.Series(y_pred_train)

    return enriched_games_filtered_df

def ppa_regression_prep(df_team, df_game, df_pbp):
    # Drop non-"fbs-vs-fbs" games
    print(f"df_team: {df_team}")
    print(f"df_game: {df_game}")
    print(f"df_pbp: {df_pbp}")

    df_pbp = df_pbp[df_pbp['home'].isin(df_team.school.to_list())]
    df_pbp = df_pbp[df_pbp['away'].isin(df_team.school.to_list())]
    df_pbp.reset_index(inplace=True, drop=True)
    df_game = df_game[df_game['home_team'].isin(df_team.school.to_list())]
    df_game = df_game[df_game['away_team'].isin(df_team.school.to_list())]
    df_game.reset_index(inplace=True, drop=True)

    # drop nas
    df_pbp.dropna(subset=['ppa'], inplace=True)
    df_pbp.reset_index(inplace=True, drop=True)

    # create list of neutral site games
    neutralGames = df_game['id'][df_game['neutral_site'] == True].to_list()
    df_pbp = df_pbp[['game_id', 'home', 'offense', 'defense', 'ppa']]

    # enrich play by play with game week
    enriched_dfPBP = df_pbp.merge(df_game[['id', 'week', 'season_type']], left_on=['game_id'], right_on='id')
    print(enriched_dfPBP)
    print(len(df_pbp.columns))

    # All Plays
    df = enriched_dfPBP[['week', 'season_type', 'game_id', 'home', 'offense', 'defense', 'ppa']]  # columns of interest
    df.loc['hfa'] = None  # homefield advantage
    df.loc[(df.home == df.offense), 'hfa'] = 1  # home team on offense
    df.loc[(df.home == df.defense), 'hfa'] = -1  # away team on offense
    df.loc[(df.game_id.isin(neutralGames)), 'hfa'] = 0  # neutral site games
    df = df[['week', 'season_type', 'offense', 'hfa', 'defense', 'ppa']]  # drop unneeded colums
    df.dropna(subset=['ppa'], inplace=True)  # drop nas
    df.reset_index(inplace=True, drop=True)  # reset index
    return df


def opponent_adjustment_regression(df, offStr, hfaStr, defStr, stat):
    # Create dummy variables for each Team/Opponent, plus Homefield Advantage
    dfDummies = pd.get_dummies(df[[offStr, hfaStr, defStr]])

    # Hyperparameter tuning for alpha (aka lambda, ie the penalty term)
    # for full season PBP data, the alpha will be 150-200, for smaller sample sizes it may find a higher alpha
    rdcv = linear_model.RidgeCV(alphas=[75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325], fit_intercept=True)
    rdcv.fit(dfDummies, df[stat]);
    alf = rdcv.alpha_

    # Or set Alpha directly here
    # alf = 175

    # Set up ridge regression model parameters
    reg = linear_model.Ridge(alpha=alf, fit_intercept=True)

    # Run the regression
    # X values in the regression will be dummy variables each Offense/Defense, plus Homefield Advantage
    # y values will be the raw value from each game for the specific stat we're adjusting
    reg.fit(X=dfDummies, y=df[stat])

    # Extract regression coefficients
    dfRegResults = pd.DataFrame({
        'coef_name': dfDummies.columns.values,
        'ridge_reg_coef': reg.coef_})

    # Add intercept back in to reg coef to get 'adjusted' value
    dfRegResults['ridge_reg_value'] = (dfRegResults['ridge_reg_coef'] + reg.intercept_)

    # Offense
    dfAdjOff = (dfRegResults[dfRegResults['coef_name'].str.slice(0, len(offStr)) == offStr].
                rename(columns={"ridge_reg_value": stat}).
                reset_index(drop=True))
    dfAdjOff['coef_name'] = dfAdjOff['coef_name'].str.replace(offStr + '_', '')
    dfAdjOff = dfAdjOff.drop(columns=['ridge_reg_coef'])

    # print(f"dfAdjOff: {dfAdjOff}")
    # Defense
    dfAdjDef = (dfRegResults[dfRegResults['coef_name'].str.slice(0, len(defStr)) == defStr].
                rename(columns={"ridge_reg_value": stat}).
                reset_index(drop=True))
    dfAdjDef['coef_name'] = dfAdjDef['coef_name'].str.replace(defStr + '_', '')
    dfAdjDef = dfAdjDef.drop(columns=['ridge_reg_coef'])
    return [dfAdjOff, dfAdjDef]

def post_opponent_adjustment_wrapper(df_team, df, df_adj_off, df_adj_def):
    # associate the raw and adjusted epa with each team
    df_team['rawOff'] = df_team.join(df.groupby('offense').mean().ppa, on='school').ppa # raw avg ppa
    df_team['adjOff'] = df_team.join(df_adj_off.set_index('coef_name'), on='school').ppa # adj est ppa
    df_team['rawDef'] = df_team.join(df.groupby('defense').mean().ppa, on='school').ppa
    df_team['adjDef'] = df_team.join(df_adj_def.set_index('coef_name'), on='school').ppa

    # final formatting and output
    df_team = df_team.round(3) # round adjusted value to thousandths
    return df_team

def opponent_adjustment_regression_wrapper(df_team, df_game, df_pbp,
                                           year):

    # pre regression prep
    df = ppa_regression_prep(df_team, df_game, df_pbp)

    # dataframe column names to help guide opponent adjustment function
    ppa_adjusted_df_list = []
    week_list = [w for w in list(df['week'].unique())]
    season_type_list = list(df['season_type'].unique())

    for week in week_list:
        for season_type in season_type_list:
            if ((week > 1) and (season_type == 'postseason')) | ((week < 4) and (season_type == 'regular')):
                continue
            print(f"week: {week}, season_type: {season_type}")
            prediction_week = df.loc[(df.week <= week) & (
                        df.season_type == season_type)]  # includes current week in forecasting dataset, need to fix
            adj_df_list = opponent_adjustment_regression(prediction_week, offStr, hfaStr, defStr, stat)
            df_adj_off = adj_df_list[0]
            df_adj_def = adj_df_list[1]

            # final formatting and output
            df_team = post_opponent_adjustment_wrapper(df_team, df, df_adj_off, df_adj_def)
            df_team['week'] = week
            df_team['year'] = year
            df_team['season_type'] = season_type
            ppa_adjusted_df_list.append(df_team)

    output_df = pd.concat(ppa_adjusted_df_list)

    return output_df