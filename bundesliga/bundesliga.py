# -*- coding: utf-8 -*-

import datetime
import string

from prettytable import PrettyTable


def parseDateTime(time):
    return datetime.datetime.strptime(time, '%a, %d %b %Y %H:%M:%S %Z')


def create_results_table():
    x = PrettyTable(["Home", "Away", "Result", "Goals", "Status", "Date"])
    x.align["Home"] = "l"
    x.align["Away"] = "l"
    x.align["Date"] = "l"
    x.align["Goals"] = "l"

    return x


def create_table_table():
    x = PrettyTable(["Rank", "Club", "Matches", "Wins", "Draws", "Losses", "Goals", "GD", "Points"])
    x.align["Club"] = "l"

    return x


def process_matches(matches):
    if not matches:
        return

    results = []
    for match in matches:
        match_result = []
        match = match['Matchdata']

        goalsInfo = ""
        now = datetime.datetime.utcnow()
        matchDate = parseDateTime(match['matchDateTimeUTC'])
        date = matchDate.strftime('%H:%M %d.%m.%Y')
        if matchDate > now:
            status = "Not started"
            points = "-:-"
        else:
            if match['matchIsFinished'] == True:
                status = 'Finished'
            else:
                status = 'Running'

            if match['goals'] != None and len(match['goals']) > 0:
                goals = match['goals']
                for goal in goals:
                    goal = goal['Goal']
                    if 'goalGetterName' in goal:
                        scoreTeam1 = str(goal['goalScoreTeam1'])
                        scoreTeam2 = str(goal['goalScoreTeam2'])
                        goalsInfo += scoreTeam1 + ':' + scoreTeam2 + ' ' + goal['goalGetterName'] + ', '

                goalsInfo = goalsInfo[:-2]

                maxLength = 50
                if len(goalsInfo) > maxLength:
                    index = string.rfind(goalsInfo[:maxLength-1], ',')
                    while index < 0:
                        index = string.rfind(goalsInfo[:maxLength])
                        maxLength += 1
                    goalsInfo = goalsInfo[:index] + '\n' + string.strip(goalsInfo[index+1:])

            points = str(match['pointsTeam1']) + " : " + str(match['pointsTeam2'])

        match_result.append(match['nameTeam1'])
        match_result.append(match['nameTeam2'])
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
