from __future__ import annotations
from csv import DictReader
from copy import deepcopy
from typing import Callable, List
from json import dumps
from rio.predict import predict

from rio.teams import Teams
from rio.logger import logger


def load_matches() -> List[dict]:
    with open("./rio.csv", "r") as csv_file:
        fieldnames = csv_file.readline().split(",")
        return list(DictReader(f=csv_file, fieldnames=fieldnames))


def process_matches(matches: list) -> Teams:
    teams = Teams()
    for match in matches:
        teams.add(team_name=match["Team A"], stage=match["Stage"])
        teams.add(team_name=match["Team B"], stage=match["Stage"])
        teams.get(match["Winner"]).record_win(teams.get(match["Loser"]))
    return teams


def print_block(print_function: Callable, message: str, char: str = "=", length: int = 80):
    print_function(char * length)
    print_function(f"{message:{char}^{length}}")
    print_function(char * length)


def main():
    matches = load_matches()
    teams = process_matches(matches)
    print_block(logger.info, f" Legends ")
    for team in teams.legends:
        logger.debug(f"{team}")
    
    rounds = {
        "ROUND 1": [("C9", "MOUZ"), ("FURIA", "NAVI"), ("HEROIC", "SPIRIT"), ("OUTSIDERS", "FNATIC")],
        "ROUND 2": [("C9", "OUTSIDERS"), ("FURIA", "HEROIC")],
        "ROUND 3": [("OUTSIDERS", "FURIA")]
    }
    
    for round, matches in rounds.items():
        print_block(logger.info, f" {round} ")
        for team_a_name, team_b_name in matches:
            print_block(logger.info, f" {round}: {team_a_name} vs {team_b_name} ", char='-')
            team_a = teams.get(team_a_name)
            logger.info(team_a)
            team_b = teams.get(team_b_name) 
            logger.info(team_b)
            winner = predict(team_a, team_b)
            logger.info(f"Winner is {winner.name}!")
            loser = team_b if team_a == winner else team_a
            winner.record_win(loser)


if __name__ == "__main__":
    main()
