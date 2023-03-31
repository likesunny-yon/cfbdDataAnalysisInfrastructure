import json
import sys
import boto3
import os
import datetime
import pandas as pd
import logging
import cfbd_data.utilities.utility_functions as utilities
from cfbd_data.utilities.constants import *
import cfbd_data.stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import cfbd_data.transformations.pre_pred_transformations as pre_pred_transformations
import cfbd_data.transformations.post_pred_transformations as post_pred_transformations
import cfbd_data.cfbd_configs as configs
import cfbd_data.forecasting.linear_regression_forecasting as lin_reg_forecast


logger = logging.getLogger()
logger.setLevel(logging.INFO)
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')


def cfbd_data_ingestion(event, context):
    # pull data
    secret_name = os.environ["secret_name"]
    region_name = os.environ["secret_region"]

    secret_response = json.loads(utilities.get_secret(secret_name=secret_name, region_name=region_name))
    api_key = secret_response['cfbd_api_key']
    print(f"api_key: {api_key}")
    api_auth_config = cfbd_api_ingestion.init_config(api_key=api_key)
    api_class = event.get('api_class', None)
    method = event.get('api_method', None)
    weeks = event.get('weeks', None)
    season_types = event.get('season_types', None)
    years = event.get('years', None)
    print(f"method: {method}")
    print(f"weeks: {weeks}")
    print(f"season_types: {season_types}")
    print(f"years: {years}")

    for year in years:
        for season_type in season_types:
            if season_type == 'postseason' and week > 1:
                continue
            for week in weeks:
                filter_configs = utilities.filter_config_map(api_method=method, inputs={'year': year,
                                                             'season_type': season_type, 'week': week})

                api_response_df = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'],
                                                                                     api_class),
                                                                   api_method=method,
                                                                   auth_configuration=api_auth_config,
                                                                   filter_configs=filter_configs)

    # perform basic transformations to prep for future analysis
    output_df = cfbd_api_ingestion.pre_storage_transformations(api_response_df, method)
    # save to s3
    s3_destination = os.environ['s3_destination']
    print(f"s3_destination: {s3_destination}")

    filter_dict = {'year': year, 'season_type': season_type, 'week': week}
    filter_prefix_string = utilities.api_filter_prefix_string({k: v for k, v in filter_dict.items() if v})

    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    utilities.dataframe_to_s3(output_df, s3_destination,
                              f"{cfbd_prefix}{api_class}_{method}/{filter_prefix_string}{extract_prefix}{txt_ext}")
    utilities.dataframe_to_s3(output_df, s3_destination,
                              f"{cfbd_archive}{api_class}_{method}/{filter_prefix_string}{extract_prefix}_{current_timestamp}{txt_ext}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "API ingestion completed",
            }
        ),
    }


def cfbd_ingestion_wrapper(event, context):
    dynamic_configs = event.get('configs', None)
    if not dynamic_configs:
        ingestion_configs = configs.default_ingestion_configs
    else:
        ingestion_configs = dynamic_configs

    for api in ingestion_configs['api_type']:
        api_class = api
        for method in ingestion_configs['api_type'][api]:
            api_method = method
            method_params = ingestion_configs['api_type'][api][method]
            #TODO: Need to test if None Type can be passed in lambda event input
            years = method_params['years'] if method_params['years'] != "" else None
            season_types = method_params['season_types'] if method_params['season_types'] != "" else None
            weeks = method_params['weeks'] if method_params['weeks'] != "" else None
            input_params = {'api_class': api_class,
                            'api_method': api_method,
                            'years': years,
                            'season_types': season_types,
                            'weeks': weeks}
            print(f"input_params: {input_params}")
            target_function = os.environ['CfbdFunction']

            response = lambda_client.invoke(FunctionName=target_function,
                                            InvocationType='Event',
                                            Payload=json.dumps(input_params))
            parsed_response = response['Payload']

            print(f"parsed_response: {parsed_response}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }

def apply_ppa_attribution(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    output_file = event.get('output_prefix', adjusted_ppa_path)
    year_input = event.get('year', None)
    year = year_input if year_input else datetime.datetime.now().strftime('%Y')
    season_type = event.get('season_type', None)
    week = event.get('week', None)

    # pull source data
    ingest_file_prefix = utilities.ingest_file_prefix_string(year, season_type, week)

    df_team = utilities.dataframe_from_s3(
        f"{cfbd_prefix}TeamsApi_get_fbs_teams/year_{year}/", s3_bucket)
    df_game = utilities.dataframe_from_s3(
        f"{cfbd_prefix}GamesApi_get_games/{ingest_file_prefix}", s3_bucket)
    df_pbp = utilities.dataframe_from_s3(
        f"{cfbd_prefix}PlaysApi_get_plays/{ingest_file_prefix}", s3_bucket, columns=get_plays_columns)

    #apply regression
    ppa_regression = lin_reg_forecast.opponent_adjustment_regression_wrapper(df_team, df_game, df_pbp, year)
    print(f"ppa_regression: {ppa_regression}")

    #output regression df
    utilities.output_df_by_index(ppa_regression, s3_bucket, output_file, year, week, season_type)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }

def stack_game_tranformation(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    output_prefix = event.get('output_prefix', stacked_game_path)
    year_input = event.get('year', None)
    year = year_input if year_input else datetime.datetime.now().strftime('%Y')
    season_type = event.get('season_type', None)
    week = event.get('week', None)

    #update games dataset into stacked model
    ingest_file_prefix = utilities.ingest_file_prefix_string(year, season_type, week)

    df_get_games = utilities.dataframe_from_s3(
        f"{cfbd_prefix}GamesApi_get_games/{ingest_file_prefix}", s3_bucket)

    stacked_game_df = pre_pred_transformations.transform_game_details(df_get_games)

    #output df
    utilities.output_df_by_index(stacked_game_df, s3_bucket, output_prefix, year, week=None, season_type=None)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }

def recruiting_tranformation(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    output_prefix = event.get('output_prefix', transformed_recruiting_prefix)
    year_input = event.get('year', None)
    year = year_input if year_input else datetime.datetime.now().strftime('%Y')
    season_type = event.get('season_type', None)
    week = event.get('week', None)

    # perform_recruiting_transformations
    ingest_file_prefix = utilities.ingest_file_prefix_string(year, season_type, week)

    df_player_stats = utilities.dataframe_from_s3(
        f'{cfbd_prefix}PlayersApi_get_player_season_stats/{ingest_file_prefix}',
        s3_bucket,
        columns=player_season_stats_columns)

    df_roster = utilities.dataframe_from_s3(
        f'{cfbd_prefix}TeamsApi_get_roster/year_{str(year)}/',
        s3_bucket)

    df_recruits = utilities.dataframe_from_s3(
        f'{cfbd_prefix}RecruitingApi_get_recruiting_players/year_{str(year)}/',
        s3_bucket)

    df_transfer_portal = utilities.dataframe_from_s3(
        f'{cfbd_prefix}PlayersApi_get_transfer_portal/year_{str(year)}/',
        s3_bucket)

    df_get_recruiting_groups = utilities.dataframe_from_s3(
        f'{cfbd_prefix}RecruitingApi_get_recruiting_groups/year_{str(year)}/',
        s3_bucket)

    recruiting_df = pre_pred_transformations.recruiting_transformation(df_player_stats, df_roster,
                                                                      df_recruits, df_transfer_portal,
                                                                      df_get_recruiting_groups, year)
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    path = f"{cfbd_prefix}{output_prefix}year_{str(year)}"
    utilities.dataframe_to_s3(recruiting_df,
                              s3_bucket,
                              f"{path}/{extract_prefix}_{current_timestamp}.txt")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }

def pre_forecasting_transformation(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    output_prefix = event.get('output_file', default_forecasting_path)
    year_input = event.get('year', None)
    year = year_input if year_input else datetime.datetime.now().strftime('%Y')
    season_type = event.get('season_type', None)
    week = event.get('week', None)

    #extract dependency datasets
    ingest_file_prefix = utilities.ingest_file_prefix_string(year, season_type, week)

    pivoted_games_data = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{team_game_stats_prefix}{ingest_file_prefix}", s3_bucket)
    total_recruiting_stats = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{transformed_recruiting_prefix}year_{str(year)}/", s3_bucket)
    df_advanced_game_team_stats = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{advanced_team_game_stats_prefix}{ingest_file_prefix}", s3_bucket)
    df_get_games_all = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{stacked_game_path}{ingest_file_prefix}", s3_bucket)
    weekly_adjusted_ppa_df = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{adjusted_ppa_path}{ingest_file_prefix}", s3_bucket)
    df_team = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{fbs_teams_path}year_{year}/", s3_bucket)

    # apply pre-forecasting transformations
    prep_forecasting_df = pre_pred_transformations.prep_default_forecasting_dataset(pivoted_games_data, total_recruiting_stats,
                                                                                     df_advanced_game_team_stats, df_get_games_all,
                                                                                     weekly_adjusted_ppa_df, df_team)
    print(f"prep_forecasting_df: {prep_forecasting_df}")

    # output to s3
    utilities.output_df_by_index(prep_forecasting_df, s3_bucket, output_prefix,
                                 year, week, season_type)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }
def apply_prediction(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    output_prefix = event.get('output_file', forecast_output_path)
    year_input = event.get('year', None)
    year = year_input if year_input else datetime.datetime.now().strftime('%Y')
    season_type = event.get('season_type', None)
    week = event.get('week', None)

    #apply pre-forecasting transformations
    ingest_prefix = utilities.ingest_file_prefix_string(year, season_type, week)

    #pull forecast dependencies
    enriched_games_filtered_df = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{default_forecasting_path}year_{year}/", s3_bucket).reset_index()
    betting_lines_df = utilities.dataframe_from_s3(
        f"{cfbd_prefix}{betting_line_path}{ingest_prefix}", s3_bucket)

    #run linear regression for points prediction
    raw_prediction_df = lin_reg_forecast.apply_multiple_linear_regression(enriched_games_filtered_df, week, season_type)

    #modify output to build external dataset
    game_line_output_df = post_pred_transformations.modify_game_line_output(raw_prediction_df, betting_lines_df)

    # output to s3
    utilities.output_df_by_index(game_line_output_df, s3_bucket, output_prefix,
                                 year, week, season_type)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Request completed successfully",
            }
        ),
    }

def prediction_output(event, context):
    #TODO Pick up here
    week_param = event.get("queryStringParameters", None)['week']

    print(f"week_param: {week_param}\nparam_type: {type(week_param)}")
    logger.info(f"week_param: {week_param}\nparam_type: {type(week_param)}")

    s3_bucket = os.environ['s3_source_bucket']
    prediction_output_file = os.environ['output_prediction_file']

    prediction_output_df = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=prediction_output_file).get("Body"), sep='|')
    print(f"prediction_output_df: {prediction_output_df}")
    prepped_jason = json.dumps(prediction_output_df.loc[prediction_output_df.week == int(week_param)].to_dict(orient='records'))
    print(f"prepped_jason: {prepped_jason}")
    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'}, #TODO replace with hostname of frontend (CloudFront)
        "body": prepped_jason
    }