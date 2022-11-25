# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  Please note that API keys should be supplied with \"Bearer \" prepended (e.g. \"Bearer your_key\"). API keys can be acquired from the CollegeFootballData.com website.  # noqa: E501

    OpenAPI spec version: 4.4.11
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cfbd.api_client import ApiClient


class DrivesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_drives(self, year, **kwargs):  # noqa: E501
        """Drive data and results  # noqa: E501

        Get game drives  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_drives(year, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Year filter (required)
        :param str season_type: Season type filter
        :param int week: Week filter
        :param str team: Team filter
        :param str offense: Offensive team filter
        :param str defense: Defensive team filter
        :param str conference: Conference filter
        :param str offense_conference: Offensive conference filter
        :param str defense_conference: Defensive conference filter
        :param str classification: Division classification filter (fbs/fcs/ii/iii)
        :return: list[Drive]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_drives_with_http_info(year, **kwargs)  # noqa: E501
        else:
            (data) = self.get_drives_with_http_info(year, **kwargs)  # noqa: E501
            return data

    def get_drives_with_http_info(self, year, **kwargs):  # noqa: E501
        """Drive data and results  # noqa: E501

        Get game drives  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_drives_with_http_info(year, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int year: Year filter (required)
        :param str season_type: Season type filter
        :param int week: Week filter
        :param str team: Team filter
        :param str offense: Offensive team filter
        :param str defense: Defensive team filter
        :param str conference: Conference filter
        :param str offense_conference: Offensive conference filter
        :param str defense_conference: Defensive conference filter
        :param str classification: Division classification filter (fbs/fcs/ii/iii)
        :return: list[Drive]
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['year', 'season_type', 'week', 'team', 'offense', 'defense', 'conference', 'offense_conference', 'defense_conference', 'classification']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_drives" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'year' is set
        if self.api_client.client_side_validation and ('year' not in params or
                                                       params['year'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `year` when calling `get_drives`")  # noqa: E501

        if self.api_client.client_side_validation and ('year' in params and params['year'] < 2001):  # noqa: E501
            raise ValueError("Invalid value for parameter `year` when calling `get_drives`, must be a value greater than or equal to `2001`")  # noqa: E501
        if self.api_client.client_side_validation and ('week' in params and params['week'] > 16):  # noqa: E501
            raise ValueError("Invalid value for parameter `week` when calling `get_drives`, must be a value less than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'season_type' in params:
            query_params.append(('seasonType', params['season_type']))  # noqa: E501
        if 'year' in params:
            query_params.append(('year', params['year']))  # noqa: E501
        if 'week' in params:
            query_params.append(('week', params['week']))  # noqa: E501
        if 'team' in params:
            query_params.append(('team', params['team']))  # noqa: E501
        if 'offense' in params:
            query_params.append(('offense', params['offense']))  # noqa: E501
        if 'defense' in params:
            query_params.append(('defense', params['defense']))  # noqa: E501
        if 'conference' in params:
            query_params.append(('conference', params['conference']))  # noqa: E501
        if 'offense_conference' in params:
            query_params.append(('offenseConference', params['offense_conference']))  # noqa: E501
        if 'defense_conference' in params:
            query_params.append(('defenseConference', params['defense_conference']))  # noqa: E501
        if 'classification' in params:
            query_params.append(('classification', params['classification']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['ApiKeyAuth']  # noqa: E501

        return self.api_client.call_api(
            '/drives', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[Drive]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)