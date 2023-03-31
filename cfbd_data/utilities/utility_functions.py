import datetime
import pandas as pd
from io import StringIO, BytesIO # python3; python2: BytesIO
import cfbd_data.utilities.constants as constants
import glob
from  cfbd_data.utilities.constants import *
import boto3
from botocore.exceptions import ClientError

def dataframe_to_s3(dataframe: pd.DataFrame, bucket: str, file_name: str):
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer, index=False, sep='|')
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, file_name).put(Body=csv_buffer.getvalue())

def filter_config_map(api_method, inputs):
    print(f"api_method: {api_method}")
    config_structure = constants.cfbd_api_input_map[api_method]
    print(f"config_structure: {config_structure}")

    for key in config_structure:
        config_structure[key] = inputs[key]

    print(f"config_structure: {config_structure}")
    return config_structure

def api_filter_prefix_string(input_dict):
    output_str = ""
    for key, value in input_dict.items():
        output_str += f"{key}_{value}"

    print(f"output_str: {output_str}")
    return output_str

def ingest_file_prefix_string(year, season_type, week):
    output_str = ""
    if year:
        output_str += f"year_{year}/"
    else:
        raise Exception("year input needs to be specified")
    if season_type:
        output_str += f"season_{season_type}/"
    else:
        if week:
            raise Exception("need to specify season type if specifying week")
        output_str += ""
    if week:
        output_str += f"week_{week}/"
    else:
        output_str += ""

    print(f"output_str: {output_str}")
    return output_str

def clean_api_configs(config):
    for method in config['api_class']['api_methods']:
        method_filter = config['api_class']['api_methods'][method]['filter_config']
        method_filter_configs = {} if method_filter is None else {k: v for k, v in method_filter.items() if (v is not None or k in ['year'])}
        try:
            if method_filter_configs['year'] is None:
                    current_year = int(datetime.datetime.now().strftime('%Y'))
                    method_filter_configs['year'] = list(range(2013, current_year)) + [current_year]
                    print(method_filter_configs['year'])
            '''else 'week' in method_filter_configs & method_filter_configs['week'] is None:
                method_filter_configs['week'] = range(0, 14) + [14]
            else 'team' in method_filter_configs & method_filter_configs['team'] is None:
                api_auth_config = cfbd_api_ingestion.init_config(
                    api_key='XbfBgZjizImMF81QPIho2e68olGYRSRCmZJzFU6DbwPPJj+BoGM1CflXMZjTQ7TS')
                team_df = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], 'TeamsApi'),
                                                                api_method='get_fbs_teams',
                                                                auth_configuration=api_auth_config,
                                                                filter_configs={'year': int(datetime.datetime.now().strftime('%Y'))})
                teams_list = team_df['school'].values.to_list()
                method_filter_configs['teams'] = teams_list
            '''
        except KeyError:
            print("list key does not exist in config")

        config['api_class']['api_methods'][method]['filter_config'] = method_filter_configs
    return config


def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return get_secret_value_response['SecretString']

def dataframe_from_s3(path, s3_bucket, columns=None):
    s3 = boto3.resource('s3')
    print(f"dataframe_from_s3 path: {path}")
    bucket = s3.Bucket(s3_bucket)
    prefix_objs = bucket.objects.filter(Prefix=path)
    df_list = []
    for obj in prefix_objs:
        print(obj.key)
        body = obj.get()['Body'].read()
        temp_df = pd.read_csv(BytesIO(body), sep='|', encoding='utf8', usecols=columns, engine="pyarrow")
        df_list.append(temp_df)
    concat_df = pd.concat(df_list)
    print(f"concat_df: {concat_df}")
    return concat_df

def divide_string(x):
    num = int(x.split('-')[0])
    denom = int(x.split('-')[1])
    if denom == 0:
      return None
    else:
      return num / denom

def output_df_by_index(output_df, s3_bucket, prefix_path, year, week=None, season_type=None):
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if (week is None) and (season_type is None):
        weeks = output_df['week'].unique()
        season_types = output_df['season_type'].unique()
        for season_type in season_types:
            for week in weeks:
                print(f"week: {week}, season_type: {season_type}")
                output_df_final = output_df.loc[(output_df.week == week) & (output_df.season_type == season_type)]
                path = f"{cfbd_prefix}{prefix_path}year_{str(year)}/season_{season_type}/week_{str(int(week))}"
                dataframe_to_s3(output_df_final,
                                          s3_bucket,
                                          f"{path}/{extract_prefix}_{current_timestamp}.txt")
    else:
        path = f"{cfbd_prefix}{prefix_path}year_{str(year)}/season_{season_type}/week_{str(int(week))}"
        dataframe_to_s3(output_df, s3_bucket, f"{path}/{extract_prefix}_{current_timestamp}.txt")