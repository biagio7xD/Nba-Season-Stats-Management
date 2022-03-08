from pony.orm import *
from ..model.model import *


@db_session
def get_all_team_of_season(season: int):
    return Team_Season.select(lambda tm: tm.season.season == season)


@db_session
def get_all_season():
    return Season.select()


@db_session
def get_team(idx: int):
    return Team.select(lambda t: t.id == idx).get()


@db_session
def get_team_season(season: int, idx: int):
    return Team_Season.select(lambda tm: tm.season.season == season and tm.team.id == idx).get()


@db_session
def get_team_stats(idx: int, season: int):
    return TeamStats.select(lambda ts: ts.team.team.id == idx and ts.team.season.season == season).get()


@db_session
def get_coach(idx: int, season: int):
    return Coach.select(lambda c: c.team_season.team.id == idx and c.team_season.season.season == season).get()


@db_session
def get_coach_stats(idx: str):
    return CoachStats.select(lambda c: c.coach.name == idx).get()


@db_session
def get_players(idx: int, season: int):
    return Player.select(lambda p: p.team_season.team.id == idx and p.team_season.season.season == season)


@db_session
def get_player_stats(idx: int):
    return PlayerStats.select(lambda ps: ps.player.id == idx).get()


@db_session
def get_team_staff(idx: int):
    return Staff.select(lambda s: s.team.id == idx).get()


@db_session
def get_arena(idx: int):
    return Arena.select(lambda a: a.team.id == idx).get()


@db_session
def get_max_capacity_arena():
    return Arena.select().order_by(desc(Arena.capacity))[:5]
