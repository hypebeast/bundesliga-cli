# -*- coding: utf-8 -*-

import datetime
# import string

from prettytable import PrettyTable


def parseDateTime(time):
    return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')


def from_utc(utcTime, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    """
    Convert UTC ISO-8601 time string to time.struct_time
    """
    return datetime.datetime.strptime(utcTime, fmt)


def create_results_table():
    x = PrettyTable(["Home", "Away", "Result", "Goals", "Status", "Date"])
    x.align["Home"] = "l"
    x.align["Away"] = "l"
    x.align["Date"] = "l"
    x.align["Goals"] = "l"
    return x


def create_table_table(rows):
    x = PrettyTable(["Rank", "Club", "Matches", "Wins", "Draws", "Losses",
                     "Goals", "GD", "Points"], align="r")
    x.align["Rank"] = "r"
    x.align["Club"] = "l"
    x.align["Matches"] = "r"
    x.align["Wins"] = "r"
    x.align["Draws"] = "r"
    x.align["Losses"] = "r"
    x.align["GD"] = "r"
    x.align["Points"] = "r"

    for row in rows:
        x.add_row(row)

    return x


def create_leagues_table():
    x = PrettyTable(["Name", "Season", "Shortcut"])
    x.align["Name"] = "l"
    return x


def create_teams_table():
    x = PrettyTable(["Name"])
    x.align["Name"] = "l"
    return x


def current_season():
    return "2014"


def process_matches(matches):
    if not matches:
        return

    results = []
    for match in matches:
        match_result = []
        # match = match['Matchdata']

        now = datetime.datetime.utcnow()
        okParsingMatchDate = False
        try:
            # matchDate = parseDateTime(match['MatchDateTimeUTC'])
            matchDate = parseDateTime(match['MatchDateTime'])
            date = matchDate.strftime('%H:%M %d.%m.%Y')
            okParsingMatchDate = True
        except:
            date = "-"
            status = "-"

        if okParsingMatchDate:
            if matchDate > now:
                status = "Not started"
                points = "-:-"
            else:
                if match['MatchIsFinished'] == True:
                    status = 'Finished'
                else:
                    status = 'Running'

        goalsInfo = ""
        if ('Goals' in match and match['Goals'] != None and
                len(match['Goals']) > 0):
            goals = match['Goals']
            for goal in goals:
                # goal = goal['Goal']
                if 'GoalGetterName' in goal:
                    scoreTeam1 = str(goal['ScoreTeam1'])
                    scoreTeam2 = str(goal['ScoreTeam2'])
                    goalsInfo += (scoreTeam1 + ':' + scoreTeam2 + ' ' +
                                  goal['GoalGetterName'] + ', ')

            goalsInfo = goalsInfo[:-2]

            maxLength = 50
            if len(goalsInfo) > maxLength:
                # index = string.rfind(goalsInfo[:maxLength-1], ',')
                index = goalsInfo.rfind(',', 0, maxLength-1)
                while index < 0:
                    index = goalsInfo.rfind(',', 0, maxLength)
                    maxLength += 1
                goalsInfo = (goalsInfo[:index] + '\n' +
                             goalsInfo[index+2:])

        points = '-:-'
        if match['MatchResults']:
            result = match['MatchResults'][-1]
            points = (str(result['PointsTeam1']) + " : " +
                      str(result['PointsTeam2']))
        else:
            points = '0 : 0'

        match_result.append(match['Team1']['TeamName'])
        match_result.append(match['Team2']['TeamName'])
        match_result.append(points)
        match_result.append(goalsInfo)
        match_result.append(status)
        match_result.append(date)

        results.append(match_result)

    return results


def process_table_stats(stats):
    results = []

    rank = 1
    for club in stats:
        count_matches = club['wins'] + club['losses'] + club['draws']
        goals = str(club['goals']) + ':' + str(club['received_goals'])
        gd = int(club['goals']) - int(club['received_goals'])

        club_result = []
        club_result.append(rank)
        club_result.append(club['team_name'])
        club_result.append(count_matches)
        club_result.append(club['wins'])
        club_result.append(club['draws'])
        club_result.append(club['losses'])
        club_result.append(goals)
        club_result.append(gd)
        club_result.append(club['points'])

        rank += 1

        results.append(club_result)

    return results
