from datetime import date
from pony.orm import *

db = Database()
# PostgreSQL
db.bind(provider='postgres', user='postgres', password='05041997', host='localhost', database='nba')


class Arena(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 30)
    capacity = Optional(int, nullable=True)
    city = Optional(str, 50, nullable=True)
    team = Optional(lambda: Team)


class Season(db.Entity):
    season = PrimaryKey(int)
    start_date = Required(date, unique=False)
    end_date = Required(date, unique=False)
    team_season = Set(lambda: Team_Season)


class Team_Season(db.Entity):
    season = Required(Season)
    team = Required(lambda: Team)
    coach = Optional(lambda: Coach)
    stats = Optional(lambda: TeamStats, cascade_delete=True)
    player = Set(lambda: Player)
    PrimaryKey(season, team)


class Team(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 50, unique=True, nullable=False)
    abbr = Optional(str, 5, unique=False, nullable=False)
    nickname = Optional(str, 50, unique=False, nullable=False)
    year_founded = Optional(int, unique=False)
    staff = Optional(lambda: Staff)
    arena = Optional(lambda: Arena)
    team_season = Set(lambda: Team_Season)


class Player(db.Entity):
    name = Required(str, 25, unique=False, nullable=False)
    age = Optional(int)
    team_season = Optional(lambda: Team_Season)
    position = Optional(str, 30, nullable=True)
    player_stats = Optional(lambda: PlayerStats, cascade_delete=True)


class Coach(db.Entity):
    name = Required(str, 25, unique=False, nullable=False)
    team_season = Required(Team_Season, unique=False)
    coach_stats = Optional(lambda: CoachStats, cascade_delete=True, unique=False)
    PrimaryKey(name, team_season)


class Staff(db.Entity):
    id = PrimaryKey(int, auto=True)
    owner = Required(str, 40, unique=False)
    manager = Optional(str, 25)
    team = Required(Team)


class TeamStats(db.Entity):
    id = PrimaryKey(int, size=8, auto=True)
    ELO = Required(float)
    FG_PCT = Required(float)
    FG3_PCT = Required(float)
    FGA = Required(float)
    FGM = Required(float)
    FG3M = Required(float)
    FG3A = Required(float)
    FG2M = Required(float)
    FG2A = Required(float)
    FG_MISSED = Required(float)
    FT_MISSED = Required(float)
    FTM = Required(float)
    FT_PCT = Required(float)
    FTA = Required(float)
    ORB = Required(float)
    DRB = Required(float)
    AST = Required(float)
    STL = Required(float)
    BLK = Required(float)
    TO = Required(float)
    PF = Required(float)
    EFFICACY = Required(float)
    PIE = Required(float)
    POSS = Required(float)
    PACE = Required(float)
    PTS = Required(float)
    team = Optional(Team_Season)


class PlayerStats(db.Entity):
    id = PrimaryKey(int, auto=True)
    GMS = Required(int)
    GStart = Required(int)
    MP = Required(int)
    FG = Required(int)
    FGA = Required(int)
    FGP = Required(float)
    ThreeP = Required(int)
    ThreePA = Required(int)
    ThreePP = Required(float)
    TwoP = Required(float)
    TwoPA = Required(float)
    TwoPP = Required(float)
    eFGP = Required(float)
    FT = Required(float)
    FTA = Required(float)
    FTP = Optional(float)
    ORB = Required(float)
    DRB = Required(float)
    TRB = Required(float)
    AST = Required(float)
    STL = Required(float)
    BLK = Required(float)
    TOV = Required(float)
    PF = Required(float)
    PTS = Required(float)
    player = Optional(Player)


class CoachStats(db.Entity):
    id = PrimaryKey(int, auto=True)
    SeasG = Required(int)
    SeasW = Required(int)
    SeasL = Optional(float)
    FranG = Required(int)
    FranW = Required(int)
    FranL = Required(int)
    CareW = Required(int)
    CareL = Required(int)
    CareWP = Required(float)
    POSeasG = Required(float)
    POSeasW = Required(float)
    POSeasL = Required(float)
    POFranW = Required(float)
    POFranG = Required(float)
    POFranL = Required(float)
    POCareG = Required(float)
    POCareW = Required(float)
    POCareL = Required(float)
    coach = Optional(Coach)


db.generate_mapping(create_tables=True)