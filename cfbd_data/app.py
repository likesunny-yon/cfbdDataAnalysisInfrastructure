import json
import utilities.utility_functions as utilities
import stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import transformations.pre_pred_transformations as pre_pred_transformations
import cfbd_configs as configs
import sys
import boto3
import os
import datetime
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
lambda_client = boto3.client('lambda')
s3_client = boto3.client('s3')


def cfbd_data_ingestion(event, context):
    # pull data
    secret_name = os.environ["secret_name"]
    region_name = os.environ["secret_region"]

    api_key = utilities.get_secret(secret_name=secret_name, region_name=region_name)
    api_auth_config = cfbd_api_ingestion.init_config(
        api_key=api_key)
    api_class = event.get('api_class', None)
    method = event.get('api_method', None)
    filter_configs = event.get('filter_configs', None)

    api_response_df = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], api_class),
                                                       api_method=method,
                                                       auth_configuration=api_auth_config,
                                                       filter_configs=filter_configs)

    # perform basic transformations to prep for future analysis
    output_df = cfbd_api_ingestion.pre_storage_transformations(api_response_df, method)
    # save to s3
    s3_destination = os.environ['s3_destination']
    print(f"s3_destination: {s3_destination}")

    utilities.dataframe_to_s3(output_df, s3_destination,
                              f"CFBD_Analysis/{api_class}_{method}_data_extract.txt")
    utilities.dataframe_to_s3(output_df, s3_destination,
                              f"archive/CFBD_Analysis/{api_class}/{method}/{api_class}_{method}_data_extract_{datetime.datetime.now().strftime('%Y%m%d%H')}.txt")

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
            filter_configs = ingestion_configs['api_type'][api][method]['filter_configs']
            input_params = {'api_class': api_class,
                            'api_method': api_method,
                            'filter_configs': filter_configs}
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


def prediction_output(event, context):
    week_param = event["queryStringParameters"]['week']

    print(f"week_param: {week_param}\nparam_type: {type(week_param)}")
    logger.info(f"week_param: {week_param}\nparam_type: {type(week_param)}")

    s3_bucket = os.environ['s3_source_bucket']
    prediction_output_file = os.environ['output_prediction_file']

    prediction_output_df = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=prediction_output_file).get("Body"), sep='|')
    prepped_jason = json.dumps(prediction_output_df.loc[prediction_output_df.week == week_param].to_dict(orient='records'))

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'}, #TODO replace with hostname of frontend (CloudFront)
        "body": prepped_jason
    }


def apply_prediction(event, context):
    s3_bucket = os.environ['s3_source_bucket']
    betting_lines_file = os.environ['betting_lines_file']
    games_data_file = os.environ['games_data_file']
    team_game_stats_file = os.environ['team_game_stats_file']
    player_season_stats_file = os.environ['player_season_stats_file']
    transfer_portal_file = os.environ['transfer_portal_file']
    recruiting_groups_file = os.environ['recruiting_groups_file']
    recruiting_players_file = os.environ['recruiting_players_file']
    advanced_team_game_stats_file = os.environ['advanced_team_game_stats_file']
    fbs_teams_file = os.environ['fbs_teams_file']
    roster_data_file = os.environ['roster_data_file']
    output_file = os.environ['output_file']

    df_get_games = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=games_data_file).get("Body"), sep='|')
    pivoted_games_data = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=team_game_stats_file).get("Body"),
                                     sep='|')
    df_advanced_game_team_stats = pd.read_csv(
        s3_client.get_object(Bucket=s3_bucket, Key=advanced_team_game_stats_file).get("Body"), sep='|')
    df_player_stats = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=player_season_stats_file).get("Body"),
                                  sep='|')
    df_roster = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=roster_data_file).get("Body"), sep='|')
    df_recruits = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=recruiting_players_file).get("Body"), sep='|')
    df_transfer_portal = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=transfer_portal_file).get("Body"),
                                     sep='|')
    transformed_team_attribute_df = pd.read_csv(s3_client.get_object(Bucket=s3_bucket, Key=fbs_teams_file).get("Body"),
                                                sep='|')
    df_get_recruiting_groups = pd.read_csv(
        s3_client.get_object(Bucket=s3_bucket, Key=recruiting_groups_file).get("Body"), sep='|')
    betting_lines_df = pd.read_csv(
        s3_client.get_object(Bucket=s3_bucket, Key=betting_lines_file).get("Body"), sep='|')

    df_get_games_all = pre_pred_transformations.transform_game_details(df_get_games)
    total_recruiting_stats = pre_pred_transformations.transform_recruiting_stats(df_get_recruiting_groups, df_roster,
                                                                                 df_recruits, df_transfer_portal,
                                                                                 df_player_stats)
    advanced_team_enriched_games_data = pre_pred_transformations.merge_game_stats_recruiting(df_get_games_all,
                                                                                             pivoted_games_data,
                                                                                             df_advanced_game_team_stats,
                                                                                             transformed_team_attribute_df,
                                                                                             total_recruiting_stats)
    enriched_games_filtered = pre_pred_transformations.apply_3w_lookback(advanced_team_enriched_games_data)

    mult_regression_coefficients = [2.09901846e+01, 1.32890107e-02,  2.43494927e-02, - 1.00281423e+00,
                                    2.26506730e-02, 1.38403592e-01]
    mult_regression_y_intercept = 14.499081883536103

    prediction_output_data_set = pre_pred_transformations.apply_multiple_linear_regression(enriched_games_filtered,
                                                                                           mult_regression_coefficients,
                                                                                           mult_regression_y_intercept)

    game_line_output_df = pre_pred_transformations.modify_game_line_output(prediction_output_data_set,
                                                                           betting_lines_df)

    utilities.dataframe_to_s3(game_line_output_df, s3_bucket, output_file)

    return
