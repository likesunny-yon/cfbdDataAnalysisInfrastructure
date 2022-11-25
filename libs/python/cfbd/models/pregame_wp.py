# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  Please note that API keys should be supplied with \"Bearer \" prepended (e.g. \"Bearer your_key\"). API keys can be acquired from the CollegeFootballData.com website.  # noqa: E501

    OpenAPI spec version: 4.4.11
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from cfbd.configuration import Configuration


class PregameWP(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'season': 'int',
        'season_type': 'str',
        'week': 'int',
        'game_id': 'int',
        'home_team': 'str',
        'away_team': 'str',
        'spread': 'float',
        'home_win_prob': 'float'
    }

    attribute_map = {
        'season': 'season',
        'season_type': 'seasonType',
        'week': 'week',
        'game_id': 'gameId',
        'home_team': 'homeTeam',
        'away_team': 'awayTeam',
        'spread': 'spread',
        'home_win_prob': 'homeWinProb'
    }

    def __init__(self, season=None, season_type=None, week=None, game_id=None, home_team=None, away_team=None, spread=None, home_win_prob=None, _configuration=None):  # noqa: E501
        """PregameWP - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._season = None
        self._season_type = None
        self._week = None
        self._game_id = None
        self._home_team = None
        self._away_team = None
        self._spread = None
        self._home_win_prob = None
        self.discriminator = None

        if season is not None:
            self.season = season
        if season_type is not None:
            self.season_type = season_type
        if week is not None:
            self.week = week
        if game_id is not None:
            self.game_id = game_id
        if home_team is not None:
            self.home_team = home_team
        if away_team is not None:
            self.away_team = away_team
        if spread is not None:
            self.spread = spread
        if home_win_prob is not None:
            self.home_win_prob = home_win_prob

    @property
    def season(self):
        """Gets the season of this PregameWP.  # noqa: E501


        :return: The season of this PregameWP.  # noqa: E501
        :rtype: int
        """
        return self._season

    @season.setter
    def season(self, season):
        """Sets the season of this PregameWP.


        :param season: The season of this PregameWP.  # noqa: E501
        :type: int
        """

        self._season = season

    @property
    def season_type(self):
        """Gets the season_type of this PregameWP.  # noqa: E501


        :return: The season_type of this PregameWP.  # noqa: E501
        :rtype: str
        """
        return self._season_type

    @season_type.setter
    def season_type(self, season_type):
        """Sets the season_type of this PregameWP.


        :param season_type: The season_type of this PregameWP.  # noqa: E501
        :type: str
        """

        self._season_type = season_type

    @property
    def week(self):
        """Gets the week of this PregameWP.  # noqa: E501


        :return: The week of this PregameWP.  # noqa: E501
        :rtype: int
        """
        return self._week

    @week.setter
    def week(self, week):
        """Sets the week of this PregameWP.


        :param week: The week of this PregameWP.  # noqa: E501
        :type: int
        """

        self._week = week

    @property
    def game_id(self):
        """Gets the game_id of this PregameWP.  # noqa: E501


        :return: The game_id of this PregameWP.  # noqa: E501
        :rtype: int
        """
        return self._game_id

    @game_id.setter
    def game_id(self, game_id):
        """Sets the game_id of this PregameWP.


        :param game_id: The game_id of this PregameWP.  # noqa: E501
        :type: int
        """

        self._game_id = game_id

    @property
    def home_team(self):
        """Gets the home_team of this PregameWP.  # noqa: E501


        :return: The home_team of this PregameWP.  # noqa: E501
        :rtype: str
        """
        return self._home_team

    @home_team.setter
    def home_team(self, home_team):
        """Sets the home_team of this PregameWP.


        :param home_team: The home_team of this PregameWP.  # noqa: E501
        :type: str
        """

        self._home_team = home_team

    @property
    def away_team(self):
        """Gets the away_team of this PregameWP.  # noqa: E501


        :return: The away_team of this PregameWP.  # noqa: E501
        :rtype: str
        """
        return self._away_team

    @away_team.setter
    def away_team(self, away_team):
        """Sets the away_team of this PregameWP.


        :param away_team: The away_team of this PregameWP.  # noqa: E501
        :type: str
        """

        self._away_team = away_team

    @property
    def spread(self):
        """Gets the spread of this PregameWP.  # noqa: E501


        :return: The spread of this PregameWP.  # noqa: E501
        :rtype: float
        """
        return self._spread

    @spread.setter
    def spread(self, spread):
        """Sets the spread of this PregameWP.


        :param spread: The spread of this PregameWP.  # noqa: E501
        :type: float
        """

        self._spread = spread

    @property
    def home_win_prob(self):
        """Gets the home_win_prob of this PregameWP.  # noqa: E501


        :return: The home_win_prob of this PregameWP.  # noqa: E501
        :rtype: float
        """
        return self._home_win_prob

    @home_win_prob.setter
    def home_win_prob(self, home_win_prob):
        """Sets the home_win_prob of this PregameWP.


        :param home_win_prob: The home_win_prob of this PregameWP.  # noqa: E501
        :type: float
        """

        self._home_win_prob = home_win_prob

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(PregameWP, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PregameWP):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PregameWP):
            return True

        return self.to_dict() != other.to_dict()