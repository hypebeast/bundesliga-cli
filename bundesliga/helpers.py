# -*- coding: utf-8 -*-

import datetime
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

        # now = datetime.datetime.utcnow()
        now = datetime.datetime.now()
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
            else:
                if match['MatchIsFinished'] == True:
                    status = 'Finished'
                else:
                    status = 'Running'

        if status == 'Not started':
            score = '-:-'
        else:
            score = '0:0'

        if match['Goals']:
            goalsInfo = []
            for goals in match['Goals']:
                score = (str(goals['ScoreTeam1']) + ':' +
                         str(goals['ScoreTeam2']))
                if goals['GoalGetterName']:
                    goalsInfo.append(score + ' ' + goals['GoalGetterName'])
                else:
                    goalsInfo.append(score)

            goalsInfo = ', '.join(goalsInfo)
            maxLength = 50
            if len(goalsInfo) > maxLength:
                index = goalsInfo.rfind(',', 0, maxLength-1)
                while index < 0:
                    index = goalsInfo.rfind(',', 0, maxLength)
                    maxLength += 1
                goalsInfo = (goalsInfo[:index] + '\n' +
                             goalsInfo[index+2:])
        else:
            goalsInfo = ''

        points = parse_points(match, score)
        if not points:
            points = '-:-'

        match_result.append(match['Team1']['TeamName'])
        match_result.append(match['Team2']['TeamName'])
        match_result.append(points)
        match_result.append(goalsInfo)
        match_result.append(status)
        match_result.append(date)

        results.append(match_result)

    return results


def parse_points(match, score):
    fulltime = None
    halftime = None
    if match['MatchResults']:
        halftime = ['(' + str(x['PointsTeam1']) +
                    ':' + str(x['PointsTeam2']) + ')'
                    for x in match['MatchResults']
                    if x['ResultName'] == 'Halbzeitergebnis']
        fulltime = [str(x['PointsTeam1']) + ':' + str(x['PointsTeam2'])
                    for x in match['MatchResults']
                    if x['ResultName'] == 'Endergebnis']

    if fulltime:
        result = fulltime[0] + ' ' + halftime[0]
    elif halftime:
        result = score + ' ' + halftime[0]
    else:
        result = score

    return result


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
