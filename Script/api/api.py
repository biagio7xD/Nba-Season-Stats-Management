from fastapi import FastAPI, Request
from crud import *
from pydantic import BaseModel
from loguru import logger
from pony.orm.serialization import to_dict

app = FastAPI()


@app.get("/team/{teamID}/arena")
@db_session
def g_arena(teamID: int):
    arena = get_arena(teamID)
    return {
        'city': arena.city,
        'name': arena.name,
        'capacity': arena.capacity
    }


@app.get("/team/{teamID}/staff")
@db_session
def g_staff(teamID: int):
    staff = get_team_staff(teamID)
    return {
        'owner': staff.owner,
        'manager': staff.manager,
    }


@app.get('/team/{idx}')
@db_session
def g_team(idx: int, request: Request):
    el = get_team(idx)
    seasons = {}
    for s in el.team_season:
        seasons[s.season.season] = request.url_for('team_season_info', season=s.season.season, teamID=el.id)
    data = {
        'id': el.id,
        'name': el.name,
        'abbr': el.abbr,
        'nickname': el.nickname,
        'year_founded': el.year_founded,
        'arena': request.url_for("g_arena", teamID=el.id),
        'staff': request.url_for("g_staff", teamID=el.id),
        'seasons': seasons
    }
    return data


@app.get("/{coach}/stats")
@db_session
def g_coach_stats(coach: str):
    c = get_coach_stats(coach)
    data = {}
    for key, value in c.to_dict().items():
        if key == "coach" or key == "id":
            continue
        data[key] = value
    return data


@app.get("/{season}/team/{teamID}/coach")
@db_session
def g_coach(teamID: int, season: int, request: Request):
    c = get_coach(teamID, season)
    return {
        "name": c.name,
        "stats": request.url_for('g_coach_stats', coach=c.name)
    }


@app.get("/{season}/{teamID}/stats")
@db_session
def g_team_stats(season: int, teamID: int):
    c = get_team_stats(teamID, season)
    data = {}
    for key, value in c.to_dict().items():
        if key == "team" or key == "id":
            continue
        data[key] = value
    return data


@app.get("/{season}/{teamID}/{playerID}/stats")
@db_session
def g_player_stats(season: int, teamID: int, playerID: int):
    ps = get_player_stats(playerID)
    data = {}
    for key, value in ps.to_dict().items():
        if key == "player":
            continue
        data[key] = value
    return data


@app.get("/{season}/{teamID}/players")
@db_session
def g_players(season: int, teamID: int, request: Request):
    p = get_players(teamID, season)
    data = []
    for el in p:
        data.append({
            'name': el.name,
            'age': el.age,
            'position': el.position,
            'stats': request.url_for('g_player_stats', season=season, teamID=teamID, playerID=el.id)
        })
    return data


@app.get("/{season}")
@db_session
def all_season(request: Request, season: int):
    season_team = get_all_team_of_season(2018)
    data = []
    for el in season_team:
        data.append({
            'Team': el.team.name,
            'team_info': request.url_for("g_team", idx=el.team.id),
            'stats': request.url_for('g_team_stats', teamID=el.team.id, season=el.season.season),
            'coach': request.url_for('g_coach', teamID=el.team.id, season=el.season.season),
            'players': request.url_for('g_players', teamID=el.team.id, season=el.season.season)

        })
    return data


@app.get("/{season}/{teamID}/")
@db_session
def team_season_info(request: Request, season: int, teamID: int):
    season_team = get_team_season(season, teamID)
    data = {
        'Team': season_team.team.name,
        'team_info': request.url_for("g_team", idx=season_team.team.id),
        'stats': request.url_for('g_team_stats', teamID=season_team.team.id, season=season_team.season.season),
        'coach': request.url_for('g_coach', teamID=season_team.team.id, season=season_team.season.season),
        'players': request.url_for('g_players', teamID=season_team.team.id, season=season_team.season.season)
    }

    return data
