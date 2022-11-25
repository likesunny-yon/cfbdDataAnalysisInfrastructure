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
            response = getattr(api_instance, api_method)(**config)
            api_responses.append(response)

    except ApiException as e:
        raise Exception
    converted_dict = {}
    #TODO: update to enable iterating when list object is a custom class e.g. https://github.com/CFBD/cfbd-python/blob/master/docs/BoxScore.md
    for k in api_responses[0][0].to_dict():
        converted_dict[k] = []

    for response in api_responses:
        for row in response:
            for k, v in row.to_dict().items():
                converted_dict[k].append(v)


    return pd.DataFrame(converted_dict)