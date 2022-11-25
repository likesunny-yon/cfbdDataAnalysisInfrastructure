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


class TeamRecord(object):
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
        'year': 'int',
        'team': 'str',
        'conference': 'str',
        'division': 'str',
        'expected_wins': 'float',
        'total': 'TeamRecordTotal',
        'conference_games': 'TeamRecordTotal',
        'home_games': 'TeamRecordTotal',
        'away_games': 'TeamRecordTotal'
    }

    attribute_map = {
        'year': 'year',
        'team': 'team',
        'conference': 'conference',
        'division': 'division',
        'expected_wins': 'expectedWins',
        'total': 'total',
        'conference_games': 'conferenceGames',
        'home_games': 'homeGames',
        'away_games': 'awayGames'
    }

    def __init__(self, year=None, team=None, conference=None, division=None, expected_wins=None, total=None, conference_games=None, home_games=None, away_games=None, _configuration=None):  # noqa: E501
        """TeamRecord - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._year = None
        self._team = None
        self._conference = None
        self._division = None
        self._expected_wins = None
        self._total = None
        self._conference_games = None
        self._home_games = None
        self._away_games = None
        self.discriminator = None

        if year is not None:
            self.year = year
        if team is not None:
            self.team = team
        if conference is not None:
            self.conference = conference
        if division is not None:
            self.division = division
        if expected_wins is not None:
            self.expected_wins = expected_wins
        if total is not None:
            self.total = total
        if conference_games is not None:
            self.conference_games = conference_games
        if home_games is not None:
            self.home_games = home_games
        if away_games is not None:
            self.away_games = away_games

    @property
    def year(self):
        """Gets the year of this TeamRecord.  # noqa: E501


        :return: The year of this TeamRecord.  # noqa: E501
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year):
        """Sets the year of this TeamRecord.


        :param year: The year of this TeamRecord.  # noqa: E501
        :type: int
        """

        self._year = year

    @property
    def team(self):
        """Gets the team of this TeamRecord.  # noqa: E501


        :return: The team of this TeamRecord.  # noqa: E501
        :rtype: str
        """
        return self._team

    @team.setter
    def team(self, team):
        """Sets the team of this TeamRecord.


        :param team: The team of this TeamRecord.  # noqa: E501
        :type: str
        """

        self._team = team

    @property
    def conference(self):
        """Gets the conference of this TeamRecord.  # noqa: E501


        :return: The conference of this TeamRecord.  # noqa: E501
        :rtype: str
        """
        return self._conference

    @conference.setter
    def conference(self, conference):
        """Sets the conference of this TeamRecord.


        :param conference: The conference of this TeamRecord.  # noqa: E501
        :type: str
        """

        self._conference = conference

    @property
    def division(self):
        """Gets the division of this TeamRecord.  # noqa: E501


        :return: The division of this TeamRecord.  # noqa: E501
        :rtype: str
        """
        return self._division

    @division.setter
    def division(self, division):
        """Sets the division of this TeamRecord.


        :param division: The division of this TeamRecord.  # noqa: E501
        :type: str
        """

        self._division = division

    @property
    def expected_wins(self):
        """Gets the expected_wins of this TeamRecord.  # noqa: E501


        :return: The expected_wins of this TeamRecord.  # noqa: E501
        :rtype: float
        """
        return self._expected_wins

    @expected_wins.setter
    def expected_wins(self, expected_wins):
        """Sets the expected_wins of this TeamRecord.


        :param expected_wins: The expected_wins of this TeamRecord.  # noqa: E501
        :type: float
        """

        self._expected_wins = expected_wins

    @property
    def total(self):
        """Gets the total of this TeamRecord.  # noqa: E501


        :return: The total of this TeamRecord.  # noqa: E501
        :rtype: TeamRecordTotal
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this TeamRecord.


        :param total: The total of this TeamRecord.  # noqa: E501
        :type: TeamRecordTotal
        """

        self._total = total

    @property
    def conference_games(self):
        """Gets the conference_games of this TeamRecord.  # noqa: E501


        :return: The conference_games of this TeamRecord.  # noqa: E501
        :rtype: TeamRecordTotal
        """
        return self._conference_games

    @conference_games.setter
    def conference_games(self, conference_games):
        """Sets the conference_games of this TeamRecord.


        :param conference_games: The conference_games of this TeamRecord.  # noqa: E501
        :type: TeamRecordTotal
        """

        self._conference_games = conference_games

    @property
    def home_games(self):
        """Gets the home_games of this TeamRecord.  # noqa: E501


        :return: The home_games of this TeamRecord.  # noqa: E501
        :rtype: TeamRecordTotal
        """
        return self._home_games

    @home_games.setter
    def home_games(self, home_games):
        """Sets the home_games of this TeamRecord.


        :param home_games: The home_games of this TeamRecord.  # noqa: E501
        :type: TeamRecordTotal
        """

        self._home_games = home_games

    @property
    def away_games(self):
        """Gets the away_games of this TeamRecord.  # noqa: E501


        :return: The away_games of this TeamRecord.  # noqa: E501
        :rtype: TeamRecordTotal
        """
        return self._away_games

    @away_games.setter
    def away_games(self, away_games):
        """Sets the away_games of this TeamRecord.


        :param away_games: The away_games of this TeamRecord.  # noqa: E501
        :type: TeamRecordTotal
        """

        self._away_games = away_games

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
        if issubclass(TeamRecord, dict):
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
        if not isinstance(other, TeamRecord):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TeamRecord):
            return True

        return self.to_dict() != other.to_dict()