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


class AdvancedSeasonStatOffense(object):
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
        'plays': 'int',
        'drives': 'int',
        'ppa': 'float',
        'total_ppa': 'float',
        'success_rate': 'float',
        'explosiveness': 'float',
        'power_success': 'float',
        'stuff_rate': 'float',
        'line_yards': 'float',
        'line_yards_total': 'float',
        'second_level_yards': 'float',
        'second_level_yards_total': 'int',
        'open_field_yards': 'float',
        'open_field_yards_total': 'int',
        'total_opportunies': 'int',
        'points_per_opportunity': 'float',
        'field_position': 'AdvancedSeasonStatOffenseFieldPosition',
        'havoc': 'TeamSPRatingDefenseHavoc',
        'standard_downs': 'AdvancedSeasonStatOffenseStandardDowns',
        'passing_downs': 'AdvancedSeasonStatOffenseStandardDowns',
        'rushing_plays': 'AdvancedSeasonStatOffenseRushingPlays',
        'passing_plays': 'AdvancedSeasonStatOffenseRushingPlays'
    }

    attribute_map = {
        'plays': 'plays',
        'drives': 'drives',
        'ppa': 'ppa',
        'total_ppa': 'totalPPA',
        'success_rate': 'successRate',
        'explosiveness': 'explosiveness',
        'power_success': 'powerSuccess',
        'stuff_rate': 'stuffRate',
        'line_yards': 'lineYards',
        'line_yards_total': 'lineYardsTotal',
        'second_level_yards': 'secondLevelYards',
        'second_level_yards_total': 'secondLevelYardsTotal',
        'open_field_yards': 'openFieldYards',
        'open_field_yards_total': 'openFieldYardsTotal',
        'total_opportunies': 'totalOpportunies',
        'points_per_opportunity': 'pointsPerOpportunity',
        'field_position': 'fieldPosition',
        'havoc': 'havoc',
        'standard_downs': 'standardDowns',
        'passing_downs': 'passingDowns',
        'rushing_plays': 'rushingPlays',
        'passing_plays': 'passingPlays'
    }

    def __init__(self, plays=None, drives=None, ppa=None, total_ppa=None, success_rate=None, explosiveness=None, power_success=None, stuff_rate=None, line_yards=None, line_yards_total=None, second_level_yards=None, second_level_yards_total=None, open_field_yards=None, open_field_yards_total=None, total_opportunies=None, points_per_opportunity=None, field_position=None, havoc=None, standard_downs=None, passing_downs=None, rushing_plays=None, passing_plays=None, _configuration=None):  # noqa: E501
        """AdvancedSeasonStatOffense - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._plays = None
        self._drives = None
        self._ppa = None
        self._total_ppa = None
        self._success_rate = None
        self._explosiveness = None
        self._power_success = None
        self._stuff_rate = None
        self._line_yards = None
        self._line_yards_total = None
        self._second_level_yards = None
        self._second_level_yards_total = None
        self._open_field_yards = None
        self._open_field_yards_total = None
        self._total_opportunies = None
        self._points_per_opportunity = None
        self._field_position = None
        self._havoc = None
        self._standard_downs = None
        self._passing_downs = None
        self._rushing_plays = None
        self._passing_plays = None
        self.discriminator = None

        if plays is not None:
            self.plays = plays
        if drives is not None:
            self.drives = drives
        if ppa is not None:
            self.ppa = ppa
        if total_ppa is not None:
            self.total_ppa = total_ppa
        if success_rate is not None:
            self.success_rate = success_rate
        if explosiveness is not None:
            self.explosiveness = explosiveness
        if power_success is not None:
            self.power_success = power_success
        if stuff_rate is not None:
            self.stuff_rate = stuff_rate
        if line_yards is not None:
            self.line_yards = line_yards
        if line_yards_total is not None:
            self.line_yards_total = line_yards_total
        if second_level_yards is not None:
            self.second_level_yards = second_level_yards
        if second_level_yards_total is not None:
            self.second_level_yards_total = second_level_yards_total
        if open_field_yards is not None:
            self.open_field_yards = open_field_yards
        if open_field_yards_total is not None:
            self.open_field_yards_total = open_field_yards_total
        if total_opportunies is not None:
            self.total_opportunies = total_opportunies
        if points_per_opportunity is not None:
            self.points_per_opportunity = points_per_opportunity
        if field_position is not None:
            self.field_position = field_position
        if havoc is not None:
            self.havoc = havoc
        if standard_downs is not None:
            self.standard_downs = standard_downs
        if passing_downs is not None:
            self.passing_downs = passing_downs
        if rushing_plays is not None:
            self.rushing_plays = rushing_plays
        if passing_plays is not None:
            self.passing_plays = passing_plays

    @property
    def plays(self):
        """Gets the plays of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: int
        """
        return self._plays

    @plays.setter
    def plays(self, plays):
        """Sets the plays of this AdvancedSeasonStatOffense.


        :param plays: The plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: int
        """

        self._plays = plays

    @property
    def drives(self):
        """Gets the drives of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The drives of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: int
        """
        return self._drives

    @drives.setter
    def drives(self, drives):
        """Sets the drives of this AdvancedSeasonStatOffense.


        :param drives: The drives of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: int
        """

        self._drives = drives

    @property
    def ppa(self):
        """Gets the ppa of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The ppa of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._ppa

    @ppa.setter
    def ppa(self, ppa):
        """Sets the ppa of this AdvancedSeasonStatOffense.


        :param ppa: The ppa of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._ppa = ppa

    @property
    def total_ppa(self):
        """Gets the total_ppa of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The total_ppa of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._total_ppa

    @total_ppa.setter
    def total_ppa(self, total_ppa):
        """Sets the total_ppa of this AdvancedSeasonStatOffense.


        :param total_ppa: The total_ppa of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._total_ppa = total_ppa

    @property
    def success_rate(self):
        """Gets the success_rate of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The success_rate of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._success_rate

    @success_rate.setter
    def success_rate(self, success_rate):
        """Sets the success_rate of this AdvancedSeasonStatOffense.


        :param success_rate: The success_rate of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._success_rate = success_rate

    @property
    def explosiveness(self):
        """Gets the explosiveness of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The explosiveness of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._explosiveness

    @explosiveness.setter
    def explosiveness(self, explosiveness):
        """Sets the explosiveness of this AdvancedSeasonStatOffense.


        :param explosiveness: The explosiveness of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._explosiveness = explosiveness

    @property
    def power_success(self):
        """Gets the power_success of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The power_success of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._power_success

    @power_success.setter
    def power_success(self, power_success):
        """Sets the power_success of this AdvancedSeasonStatOffense.


        :param power_success: The power_success of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._power_success = power_success

    @property
    def stuff_rate(self):
        """Gets the stuff_rate of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The stuff_rate of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._stuff_rate

    @stuff_rate.setter
    def stuff_rate(self, stuff_rate):
        """Sets the stuff_rate of this AdvancedSeasonStatOffense.


        :param stuff_rate: The stuff_rate of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._stuff_rate = stuff_rate

    @property
    def line_yards(self):
        """Gets the line_yards of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The line_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._line_yards

    @line_yards.setter
    def line_yards(self, line_yards):
        """Sets the line_yards of this AdvancedSeasonStatOffense.


        :param line_yards: The line_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._line_yards = line_yards

    @property
    def line_yards_total(self):
        """Gets the line_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The line_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._line_yards_total

    @line_yards_total.setter
    def line_yards_total(self, line_yards_total):
        """Sets the line_yards_total of this AdvancedSeasonStatOffense.


        :param line_yards_total: The line_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._line_yards_total = line_yards_total

    @property
    def second_level_yards(self):
        """Gets the second_level_yards of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The second_level_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._second_level_yards

    @second_level_yards.setter
    def second_level_yards(self, second_level_yards):
        """Sets the second_level_yards of this AdvancedSeasonStatOffense.


        :param second_level_yards: The second_level_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._second_level_yards = second_level_yards

    @property
    def second_level_yards_total(self):
        """Gets the second_level_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The second_level_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: int
        """
        return self._second_level_yards_total

    @second_level_yards_total.setter
    def second_level_yards_total(self, second_level_yards_total):
        """Sets the second_level_yards_total of this AdvancedSeasonStatOffense.


        :param second_level_yards_total: The second_level_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: int
        """

        self._second_level_yards_total = second_level_yards_total

    @property
    def open_field_yards(self):
        """Gets the open_field_yards of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The open_field_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._open_field_yards

    @open_field_yards.setter
    def open_field_yards(self, open_field_yards):
        """Sets the open_field_yards of this AdvancedSeasonStatOffense.


        :param open_field_yards: The open_field_yards of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._open_field_yards = open_field_yards

    @property
    def open_field_yards_total(self):
        """Gets the open_field_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The open_field_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: int
        """
        return self._open_field_yards_total

    @open_field_yards_total.setter
    def open_field_yards_total(self, open_field_yards_total):
        """Sets the open_field_yards_total of this AdvancedSeasonStatOffense.


        :param open_field_yards_total: The open_field_yards_total of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: int
        """

        self._open_field_yards_total = open_field_yards_total

    @property
    def total_opportunies(self):
        """Gets the total_opportunies of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The total_opportunies of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: int
        """
        return self._total_opportunies

    @total_opportunies.setter
    def total_opportunies(self, total_opportunies):
        """Sets the total_opportunies of this AdvancedSeasonStatOffense.


        :param total_opportunies: The total_opportunies of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: int
        """

        self._total_opportunies = total_opportunies

    @property
    def points_per_opportunity(self):
        """Gets the points_per_opportunity of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The points_per_opportunity of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: float
        """
        return self._points_per_opportunity

    @points_per_opportunity.setter
    def points_per_opportunity(self, points_per_opportunity):
        """Sets the points_per_opportunity of this AdvancedSeasonStatOffense.


        :param points_per_opportunity: The points_per_opportunity of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: float
        """

        self._points_per_opportunity = points_per_opportunity

    @property
    def field_position(self):
        """Gets the field_position of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The field_position of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: AdvancedSeasonStatOffenseFieldPosition
        """
        return self._field_position

    @field_position.setter
    def field_position(self, field_position):
        """Sets the field_position of this AdvancedSeasonStatOffense.


        :param field_position: The field_position of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: AdvancedSeasonStatOffenseFieldPosition
        """

        self._field_position = field_position

    @property
    def havoc(self):
        """Gets the havoc of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The havoc of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: TeamSPRatingDefenseHavoc
        """
        return self._havoc

    @havoc.setter
    def havoc(self, havoc):
        """Sets the havoc of this AdvancedSeasonStatOffense.


        :param havoc: The havoc of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: TeamSPRatingDefenseHavoc
        """

        self._havoc = havoc

    @property
    def standard_downs(self):
        """Gets the standard_downs of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The standard_downs of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: AdvancedSeasonStatOffenseStandardDowns
        """
        return self._standard_downs

    @standard_downs.setter
    def standard_downs(self, standard_downs):
        """Sets the standard_downs of this AdvancedSeasonStatOffense.


        :param standard_downs: The standard_downs of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: AdvancedSeasonStatOffenseStandardDowns
        """

        self._standard_downs = standard_downs

    @property
    def passing_downs(self):
        """Gets the passing_downs of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The passing_downs of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: AdvancedSeasonStatOffenseStandardDowns
        """
        return self._passing_downs

    @passing_downs.setter
    def passing_downs(self, passing_downs):
        """Sets the passing_downs of this AdvancedSeasonStatOffense.


        :param passing_downs: The passing_downs of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: AdvancedSeasonStatOffenseStandardDowns
        """

        self._passing_downs = passing_downs

    @property
    def rushing_plays(self):
        """Gets the rushing_plays of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The rushing_plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: AdvancedSeasonStatOffenseRushingPlays
        """
        return self._rushing_plays

    @rushing_plays.setter
    def rushing_plays(self, rushing_plays):
        """Sets the rushing_plays of this AdvancedSeasonStatOffense.


        :param rushing_plays: The rushing_plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: AdvancedSeasonStatOffenseRushingPlays
        """

        self._rushing_plays = rushing_plays

    @property
    def passing_plays(self):
        """Gets the passing_plays of this AdvancedSeasonStatOffense.  # noqa: E501


        :return: The passing_plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :rtype: AdvancedSeasonStatOffenseRushingPlays
        """
        return self._passing_plays

    @passing_plays.setter
    def passing_plays(self, passing_plays):
        """Sets the passing_plays of this AdvancedSeasonStatOffense.


        :param passing_plays: The passing_plays of this AdvancedSeasonStatOffense.  # noqa: E501
        :type: AdvancedSeasonStatOffenseRushingPlays
        """

        self._passing_plays = passing_plays

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
        if issubclass(AdvancedSeasonStatOffense, dict):
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
        if not isinstance(other, AdvancedSeasonStatOffense):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AdvancedSeasonStatOffense):
            return True

        return self.to_dict() != other.to_dict()