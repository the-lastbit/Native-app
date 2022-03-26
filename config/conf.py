import dearpygui.dearpygui as dpg
from configparser import ConfigParser
from os import getcwd


tags = {
    "main": {
        "heatview": 1110000,
        "welcomescreen": 1110001,
        "group": 1110002,
        "header": 1110003,
        "welcometext": 1110004,
        "welcomebutton": 1110005,
        "column": 110006,
        "table": 1110007,
        "row": 1110008,
        "gainer": 1110009,
        "loser": 1110010,
        "trendup": 1110011,
        "personal": 1110012,
        "search": 0,
        "settings": 1110014,
        "calendar": 1110015,
        "restore": 1110016,
        "calendarcontainer": 1110016,
        "searchcontainer": 1110017,
        "webpage": 1110018,
        "loadingscreen": 1110019,
    },
    "heatmap": {
        "db_content_daily": {},
        "db_content_monthly": {},
        "db_content_search": {},
        "textures": {},
        "plot": {},
        "row": {},
        "view": {},
        "running": True,
        "width": 100,
        "height": 100,
        "start": 0,
        "stop": 0,
        "count": 0,
        "stage": 1111110,
        "group": 1111111,
        "buttongroup": 1111112,
        "btnstage": {},
        "principalgroup": {
            "staged": 1111114,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "portfoliogroup": {
            "staged": 1111120,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "topgrouptable": {
            "staged": 1111121,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "losergrouptable": {
            "staged": 1111122,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "trendgrouptable": {
            "staged": 1111123,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "topgrouptable-": {
            "staged": 1111130,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "losergrouptable-": {
            "staged": 1111131,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "trendgrouptable-": {
            "staged": 1111132,
            "table": int,
            "rows": {},
            "portfolio": {},
            "textures": {},
        },
        "principalgroup_": 1111124,
        "portfoliogroup_": 1111125,
        "topgrouptable_": 1111126,
        "losergrouptable_": 1111127,
        "trendgrouptable_": 1111128,
        "topgrouptable__": 11111330,
        "losergrouptable__": 11111340,
        "trendgrouptable__": 11111350,
        "counter": 0,
        "chart": 1111129,
        "stagedchart": int,
    },
    "miscellaneous": {
        "state": True,
        "count": 0,
        "start": 0,
        "stop": 0,
        "counter": 0,
        "activegroup": "principalgroup",
        "porfolioweight": int,
        "updating": 11111351,
        "updatestate": False,
    },
}

groups = [
    "topgrouptable",
    "losergrouptable",
    "trendgrouptable",
]

CONFIG_PATH = f"{getcwd()}/config/config.ini"


def get_token(filename=CONFIG_PATH, section="JWT"):
    parser = ConfigParser()
    parser.read(filename)
    parameters = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            parameters[param[0]] = param[1]
    else:
        return None
    return parameters


def set_token(
    filename=CONFIG_PATH, section="JWT", item="Access_token", new_token="default"
):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        config = parser[section]
        config[item] = new_token
        with open(CONFIG_PATH, "w") as conf:
            parser.write(conf)
