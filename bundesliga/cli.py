# -*- coding: utf-8 -*-

import click

from openligadb import OpenLigaDB
from bundesliga import *


pass_openligadb = click.make_pass_decorator(OpenLigaDB)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Bundesliga results and stats for hackers.

    bundesliga-cli is a CLI tool that provides access to Bundesliga
    results and stats.

    Uses openligadb-json-api.heroku.com API which is itself a JSON wrapper
    around the OpenligaDB API (http://www.openligadb.de).
    """
    ctx.obj = OpenLigaDB()


@cli.command()
@click.option('--matchday', '-d', help='Defines the matchday')
@click.option('--league', '-l', help='Defines the league (e.g. bl1, bl2, bl3)')
@click.option('--season', '-s', help='Defines the season (e.g. 2014, 2013)')
@pass_openligadb
def matchday(openligadb, season, matchday, league):
    """
    Match results for the given matchday.

    Get all available league shortcuts with 'buli leagues'.

    Season format: e.g. 2014 or 2011
    """
    if not matchday:
        matchday = openligadb.getNextMatchday()

    if not league:
        league = openligadb.ERSTE_LIGA

    if not season:
        season = current_season()

    matches = openligadb.getMatchdayResults(matchday, season, league)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@pass_openligadb
def next(openligadb, league):
    """
    Shows the match results for the next/current matchday.

    Get all available league shortcuts with 'buli leagues'.

    Season format: e.g. 2014 or 2011
    """
    matchday = openligadb.getNextMatchday()

    if not league:
        league = openligadb.ERSTE_LIGA

    season = current_season()

    matches = openligadb.getMatchdayResults(matchday=matchday, season=season, league=league)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@pass_openligadb
def last(openligadb, league):
    """
    Shows the match results for the last matchday.

    Get all available league shortcuts with 'buli leagues'.

    Season format: e.g. 2014 or 2011
    """
    matchday = openligadb.getRecentMatchday()

    if not league:
        league = openligadb.ERSTE_LIGA

    season = current_season()

    matches = openligadb.getMatchdayResults(matchday=matchday, season=season, league=league)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@click.option('--season', '-s', help='Defines the season')
@pass_openligadb
def table(openligadb, league, season):
    """
    Shows the league table.

    By default the league table for the 1. Bundesliga and the currrent
    season is displayed.

    Get all available league shortcuts with 'buli leagues'.

    Season format: e.g. 2014 or 2011
    """
    if not league:
        league = openligadb.ERSTE_LIGA

    if not season:
        season = current_season()

    table = create_table_table()

    table_stats = openligadb.getTable(season, league)
    rows = process_table_stats(table_stats)

    for row in rows:
        table.add_row(row)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@click.option('--season', '-s', help='Defines the season')
@pass_openligadb
def teams(openligadb, league, season):
    """
    Shows the teams for a league and season.

    If no season is specified, the current season will be used.
    If no league is specified, the 1. Fussball Bundesliga will be used.

    League format: 'bl1' for 1. Bundesliga, 'bl2' for 2. Bundesliga, etc.

    Get all available league shortcuts with 'buli leagues'.

    Season format: e.g. 2014 or 2011
    """
    if not league:
        league = "bl1"

    if not season:
        season = current_season()

    table = create_teams_table()

    teams = openligadb.getTeams(season, league)

    for team in teams:
        row = [team['teamName']]
        table.add_row(row)

    print table


@cli.command()
@pass_openligadb
def leagues(openligadb):
    """
    Shows all available soccer leagues.

    The 'league shortcut' can be used to specify the league option for
    the other options.
    """
    table = create_leagues_table()
    leagues = openligadb.getAvailLeagues()

    for l in leagues:
        row = [l['leagueName'], l['leagueSaison'], l['leagueShortcut']]
        table.add_row(row)

    print table


cli.add_command(next)
cli.add_command(last)
cli.add_command(table)
cli.add_command(teams)
cli.add_command(leagues)
