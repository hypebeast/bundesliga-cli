# -*- coding: utf-8 -*-

import json
import urllib2


class OpenLigaDB:
    """
    Simple wrapper for http://openligadb-json-api.heroku.com.
    """
    ERSTE_LIGA = 'bl1'
    ZWEITE_LIGA = 'bl2'
    DRITTE_LIGA = 'bl3'

    def __init__(self):
        self.openLigaDBApiUrl = 'http://openligadb-json-api.herokuapp.com/api'

    def getMatchdayResults(self, matchday=0):
        """
        Returns the results for the given matchday
        """
        if matchday == 0:
            matchday = self.getNextMatchday();
        saison = self.getSeason()

        requestUrl = self.openLigaDBApiUrl + '/matchdata_by_group_league_saison'
        requestUrl += '?group_order_id=%s&league_saison=%s&league_shortcut=%s' % (matchday, saison, self.ERSTE_LIGA)
        data = json.load(urllib2.urlopen(requestUrl))

        return data['GetMatchdataByGroupLeagueSaisonResult']

    def getTable(self, season, league=ERSTE_LIGA):
        """
        Returns the table for the given season and league.
        """
        # 1. Build dictionary with all teams (key is the team id)
        teams = self.getTeams(season, league)
        table = {}
        for team in teams:
            table[team['teamID']] = {
                    'team_name': team['teamName'],
                    'points': 0,
                    'wins': 0,
                    'losses': 0,
                    'draws': 0,
                    'goals': 0,
                    'received_goals': 0
                    }

        matchData = self.getMatchDataByLeagueSaison(season, league)

        for match in matchData:
            if not match['matchIsFinished']:
                continue

            team1 = match['idTeam1']
            team2 = match['idTeam2']
            goals_team1 = int(match['pointsTeam1'])
            goals_team2 = int(match['pointsTeam2'])

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

        return sorted([value for key, value in table.iteritems()], key=lambda k: k['points'], reverse=True)

    def getNextMatchday(self):
        """
        Returns the next matchday (consider that the next matchday could be
        the current matchday).
        """
        requestUrl = self.openLigaDBApiUrl + '/current_group?league_shortcut=bl1'
        data = json.load(urllib2.urlopen(requestUrl))
        return data['GetCurrentGroupResult']['groupOrderID']

    def getRecentMatchday(self):
        """
        Returns the recent matchday.
        """
        previousMatchday = int(self.getNextMatchday()) - 1
        if previousMatchday < 1:
            previousMatchday = 1
        return str(previousMatchday)

    def getSeason(self):
        """
        Returns the current saison.
        """
        return 2014

    def getTeams(self, season, league=ERSTE_LIGA):
        """
        Returns a list of all teams for the given season and league.
        """
        requestUrl = self.openLigaDBApiUrl + '/teams_by_league_saison?league_saison=%s&league_shortcut=%s' % (season, league)
        data = json.load(urllib2.urlopen(requestUrl))

        teams = []
        for team in data['GetTeamsByLeagueSaisonResult']:
            teams.append(team['Team'])

        return teams

    def getMatchDataByLeagueSaison(self, season, league=ERSTE_LIGA):
        """
        """
        requestUrl = self.openLigaDBApiUrl + '/matchdata_by_league_saison?league_saison=%s&league_shortcut=%s' % (season, league)
        data = json.load(urllib2.urlopen(requestUrl))

        matchData = []
        for match in data['GetMatchdataByLeagueSaisonResult']:
            matchData.append(match['Matchdata'])

        return matchData

    def getMatchesByTeam(self, team):
        pass
