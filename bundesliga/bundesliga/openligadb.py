# -*- coding: utf-8 -*-

import json
import re
from urllib.request import urlopen


class OpenLigaDB:
    """
    Simple wrapper for http://openligadb-json-api.heroku.com.
    """
    ERSTE_LIGA = 'bl1'
    ZWEITE_LIGA = 'bl2'
    DRITTE_LIGA = 'bl3'
    FUSSBALL_SPORT_ID = 1

    def __init__(self):
        # self.openLigaDBApiUrl = 'http://openligadb-json-api.herokuapp.com/api'
        self.openLigaDBApiUrl = 'https://www.openligadb.de/api'

    def getMatchdayResults(self, matchday=0, season="", league=""):
        """
        Returns the results for the given matchday
        """
        if matchday == 0:
            matchday = self.getNextMatchday()

        if season == "":
            season = self.getSeason()

        if league == "":
            league = self.ERSTE_LIGA

        requestUrl = (self.openLigaDBApiUrl + '/getmatchdata/' +
                      league + '/' + season + '/' + str(matchday))
        data = json.load(urlopen(requestUrl))

        # return data['GetMatchdataByGroupLeagueSaisonResult']
        return data

    def getTable(self, season, league=ERSTE_LIGA):
        """
        Returns the table for the given season and league.
        """
        # 1. Build dictionary with all teams (key is the team id)
        teams = self.getTeams(season, league)
        table = {}
        for team in teams:
            table[team['TeamId']] = {
                    'team_name': team['TeamName'],
                    'points': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'goals': 0,
                    'received_goals': 0
                    }

        matchData = self.getMatchDataByLeagueSaison(season, league)

        for match in matchData:
            if not match['MatchIsFinished']:
                continue

            team1 = match['Team1']['TeamId']
            team2 = match['Team2']['TeamId']
            # team2 = match['idTeam2']
            goals_team1 = int(match['MatchResults'][-1]['PointsTeam1'])
            goals_team2 = int(match['MatchResults'][-1]['PointsTeam2'])

            teamData1 = table[team1]
            teamData2 = table[team2]

            teamData1['goals'] += goals_team1
            teamData2['goals'] += goals_team2
            teamData1['received_goals'] += goals_team2
            teamData2['received_goals'] += goals_team1

            if goals_team1 > goals_team2:
                teamData1['points'] += 3
                teamData1['wins'] += 1
                teamData2['losses'] += 1
            elif goals_team1 < goals_team2:
                teamData2['points'] += 3
                teamData2['wins'] += 1
                teamData1['losses'] += 1
            else:
                teamData1['points'] += 1
                teamData2['points'] += 1
                teamData1['draws'] += 1
                teamData2['draws'] += 1

        return sorted([value for key, value in table.items()],
                      key=lambda k: (k['points'],
                                     k['goals']-k['received_goals'],
                                     k['goals']),
                      reverse=True)

    def getNextMatchday(self, league=ERSTE_LIGA):
        """
        Returns the next matchday (consider that the next matchday could be
        the current matchday).
        """
        requestUrl = (self.openLigaDBApiUrl +
                      '/getmatchdata/' + league)
        data = json.load(urlopen(requestUrl))
        # return data['GetCurrentGroupResult']['groupOrderID']
        return data[0]['Group']['GroupOrderID']

    def getRecentMatchday(self):
        """
        Returns the recent matchday.
        """
        previousMatchday = int(self.getNextMatchday()) - 1
        if previousMatchday < 1:
            previousMatchday = 1
        return str(previousMatchday)

    def getCurrentSeason(self, league=ERSTE_LIGA):
        requestUrl = (self.openLigaDBApiUrl +
                      '/getmatchdata/' + league)
        data = json.load(urlopen(requestUrl))
        leagueName = data[0]['LeagueName']
        season = re.sub(r'.*?(\d{4}).*', r'\1', leagueName)

        return season

    def getTeams(self, season, league=ERSTE_LIGA):
        """
        Returns a list of all teams for the given season and league.
        """
        requestUrl = (self.openLigaDBApiUrl +
                      '/getavailableteams/' + league + '/' + season)
        data = json.load(urlopen(requestUrl))

        teams = []
        for team in data:
            teams.append(team)

        return teams

    def getMatchDataByLeagueSaison(self, season, league=ERSTE_LIGA):
        """
        """
        requestUrl = (self.openLigaDBApiUrl +
                      '/getmatchdata/' + league + '/' + season)
        data = json.load(urlopen(requestUrl))

        matchData = []
        for match in data:
            matchData.append(match)

        return matchData

    def getMatchesByTeam(self, team):
        pass

    # depreceated
    # def getAvailLeagues(self):
    #     requestUrl = self.openLigaDBApiUrl + '/avail_leagues'
    #     data = json.load(urlopen(requestUrl))

    #     leagues = []
    #     for league in data['GetAvailLeaguesResult']:
    #         league = league['League']
    #         if (league['leagueSportID'] == self.FUSSBALL_SPORT_ID and
    #                 'test' not in league['leagueName'].lower() and
    #                 league['leagueID'] != 532):
    #             leagues.append(league)

    #     return leagues
