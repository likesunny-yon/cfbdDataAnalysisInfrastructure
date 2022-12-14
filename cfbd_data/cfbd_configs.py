default_ingestion_configs = {'api_type':
                                 {'GamesApi':
                                           {'get_team_game_stats':
                                                {'filter_configs':
                                                     {'year': 2022,
                                                      'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                                                      }
                                                 }
                                            ,'get_games':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }
                                           }
                                  ,'StatsApi':
                                           {'get_advanced_team_game_stats':
                                                {'filter_configs':
                                                     {'year': 2022,
                                                      'week': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                                                      }
                                                 }
                                           }
                                  ,'TeamsApi':
                                           {'get_fbs_teams':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }
                                            ,'get_roster':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                }
                                           }
                                  ,'BettingApi':
                                           {'get_lines':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }
                                           }
                                  ,'PlayersApi':
                                           {'get_player_season_stats':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }
                                            ,'get_transfer_portal':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }

                                            }
                                  ,'RecruitingApi':
                                           {'get_recruiting_players':
                                                {'filter_configs':
                                                     {'year': 2022
                                                      }
                                                 }
                                            ,'get_recruiting_groups':
                                                {'filter_configs':
                                                     {'start_year': 2019,
                                                      'end_year':2022
                                                      }
                                                 }

                                            }
                                  }
                             }
