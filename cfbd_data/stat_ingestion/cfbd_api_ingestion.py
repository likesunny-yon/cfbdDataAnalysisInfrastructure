from __future__ import print_function
import cfbd
import pandas as pd
from cfbd.rest import ApiException


def init_config(api_key):
    # Configure API key authorization: ApiKeyAuth
    auth_configuration = cfbd.Configuration()
    auth_configuration.api_key['Authorization'] = api_key
    auth_configuration.api_key_prefix['Authorization'] = 'Bearer'
    return auth_configuration


def get_cfbd_data(api_class, api_method, auth_configuration, filter_configs):
    api_instance = api_class(cfbd.ApiClient(auth_configuration))

    config_list = []
    for key in filter_configs:
        if type(filter_configs[key]) is list:
            for item in filter_configs[key]:
                config_list.append({**{k:v for k, v in filter_configs.items() if k != key}, **{key:item}})

    if len(config_list) == 0:
        config_list = [filter_configs]

    print(config_list)
    try:
        api_responses = []
        for config in config_list:
            # Coaching records and history
            print(f"fetching config: {config}\napi_instance: {api_instance}\napi_method: {api_method}")
            response = getattr(api_instance, api_method)(**config)
            #print(response)
            api_responses.append(response)

    except ApiException as e:
        raise Exception(e)
    converted_dict = {}
    for k in api_responses[0][0].to_dict():
        converted_dict[k] = []

    for response in api_responses:
        for row in response:
            for k, v in row.to_dict().items():
                converted_dict[k].append(v)

    return pd.DataFrame(converted_dict)


def get_team_game_stats_transformation(input_df):
    game_list = []
    transformed_game_list_dict = {}
    game_list_dict = input_df.to_dict()

    for index in input_df.to_dict()['id']:
        transformed_game_list_dict[game_list_dict['id'][index]] = game_list_dict['teams'][index]

    for game_id in transformed_game_list_dict:
        game_stats = pd.json_normalize(transformed_game_list_dict[game_id], ['stats'],
                                       ['school', 'conference', 'home_away', 'points'], errors='ignore')
        game_stats['game_id'] = game_id
        game_list.append(game_stats)

    games_data = pd.concat(game_list, axis=0)
    pivoted_games_data = games_data.pivot(index=['game_id', 'conference', 'school', 'home_away', 'points'],
                                          columns=['category'], values=['stat'])
    pivoted_games_data.columns = pivoted_games_data.columns.get_level_values(
        0) + '_' + pivoted_games_data.columns.get_level_values(1)
    pivoted_games_data.reset_index(inplace=True)
    return pivoted_games_data


def get_advanced_team_game_stats_transformation(input_df):
    df_advanced_game_team_stats_dict = input_df[['offense', 'defense']].to_dict()

    games_list = []
    for index in df_advanced_game_team_stats_dict['offense']:
        defense_df = pd.json_normalize(df_advanced_game_team_stats_dict['defense'][index], errors='ignore')
        offense_df = pd.json_normalize(df_advanced_game_team_stats_dict['offense'][index], errors='ignore')
        attribute_df = pd.DataFrame(input_df.loc[
                                        index, [col for col in input_df.columns if
                                                col not in ['offense', 'defense']]]).transpose().reset_index()

        for col in defense_df.columns:
            defense_df = defense_df.rename(columns={col: 'defense_' + col})

        for col in offense_df.columns:
            offense_df = offense_df.rename(columns={col: 'offense_' + col})

        game_stats_df = pd.concat([attribute_df, defense_df, offense_df], axis=1)
        games_list.append(game_stats_df)

    games_data = pd.concat(games_list, axis=0)
    return games_data


def get_fbs_teams_transformation(input_df):
    trimmed_df_team_attributes = input_df[
        ['id', 'school', 'mascot', 'abbreviation', 'conference', 'division', 'logos', 'location']]

    trimmed_df_team_attributes['location'].apply(pd.Series)

    expanded_team_attribute_df = pd.concat([trimmed_df_team_attributes.drop(['location'], axis=1),
                                            trimmed_df_team_attributes['location'].apply(pd.Series)], axis=1)

    expanded_team_attribute_df[['logo_primary', 'logo_alt']] = pd.DataFrame(
        expanded_team_attribute_df['logos'].tolist(), index=expanded_team_attribute_df.index)

    transformed_team_attribute_df = expanded_team_attribute_df.drop(['logos'], axis=1)
    return transformed_team_attribute_df



def pre_storage_transformations(input_df, api_method):
    if api_method in ['get_team_game_stats', 'get_advanced_team_game_stats', 'get_fbs_teams']:
        return eval(f"{api_method}_transformation(input_df)")
    else:
        return input_df


