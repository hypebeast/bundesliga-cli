# -*- coding: utf-8 -*-

import click

from openligadb import OpenLigaDB
from bundesliga import create_results_table, create_table_table, process_matches, process_table_stats


pass_bundesliga = click.make_pass_decorator(OpenLigaDB)

@click.group()
@click.pass_context
def cli(ctx):
    """
    bundesliga-cli is a command line tool that provides access to Bundesliga
    information and results.

    Uses API http://openligadb-json-api.heroku.com which is itself a JSON wrapper
    around the OpenligaDB API (http://www.openligadb.de).
    """
    ctx.obj = OpenLigaDB()


@cli.command()
@click.option('--matchday', '-d', help='Defines the matchday')
@click.option('--league', '-l', help='Defines the league (bl1, bl2, bl3)')
@pass_bundesliga
def matchday(bundesliga, matchday, league):
    """
    Match results for the given matchday.
    """
    if not matchday:
        matchday = bundesliga.getNextMatchday()

    if not league:
        league = bundesliga.ERSTE_LIGA

    matches = bundesliga.getMatchdayResults(matchday)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@pass_bundesliga
def current(bundesliga, league):
    """
    Shows the match results for the currrent matchday.
    """
    matchday = bundesliga.getNextMatchday()

    if not league:
        league = bundesliga.ERSTE_LIGA

    matches = bundesliga.getMatchdayResults(matchday)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@pass_bundesliga
def last(bundesliga, league):
    """
    Shows the match results for the last matchday.
    """
    matchday = bundesliga.getRecentMatchday()

    if not league:
        league = bundesliga.ERSTE_LIGA

    matches = bundesliga.getMatchdayResults(matchday)
    matches = process_matches(matches)

    table = create_results_table()
    for match in matches:
        table.add_row(match)

    print table


@cli.command()
@click.option('--league', '-l', help='Defines the league')
@click.option('--season', '-s', help='Defines the season')
@pass_bundesliga
def table(bundesliga, league, season):
    """
    Shows the league table for the given league.

    If no league is given the table for the 1. Bundesliga is displayed.
    """
    if not league:
        league = bundesliga.ERSTE_LIGA

    table = create_table_table()

    season = "2014"
    table_stats = bundesliga.getTable(season, league)
    rows = process_table_stats(table_stats)

    for row in rows:
        table.add_row(row)

    print table


cli.add_command(current)
cli.add_command(last)
cli.add_command(table)
