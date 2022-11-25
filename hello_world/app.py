import json
import utilities.utility_functions as utilities
import stat_ingestion.cfbd_api_ingestion as cfbd_api_ingestion
import sys
import runtime_configs



def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    api_configs = runtime_configs.api_type
    for api_type in api_configs['ingestion_configs']['api_type']:
        print(f"api_type: {api_type}")
        api_configs = utilities.clean_api_configs(api_configs['ingestion_configs']['api_type'][api_type])

        # pull data
        api_key = open('C:/Users/mattf/cfbd_analytics/other/api_key.txt', 'r').read()
        api_auth_config = cfbd_api_ingestion.init_config(
            api_key=api_key)
        api_class = api_configs['api_class']['name']
        for method in api_configs['api_class']['api_methods']:
            filter_configs = api_configs['api_class']['api_methods'][method]['filter_config']
            print(method)

            api_response = cfbd_api_ingestion.get_cfbd_data(api_class=getattr(sys.modules['cfbd'], api_class),
                                                            api_method=method,
                                                            auth_configuration=api_auth_config,
                                                            filter_configs=filter_configs)
            utilities.dataframe_to_s3(api_response, 'cfbd-data-archive', f"{api_type}/{method}/data_extract/cfbd_{method}_api_extract.txt")
            #api_response.to_csv(
            #    f"C:/Users/mattf/cfbd_analytics/file_stage/{api_type}_{method}_data_extract_{datetime.datetime.now().strftime('%Y%m%d%H')}.txt",
            #    sep='|')

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
