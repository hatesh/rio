from __future__ import annotations
from csv import DictReader
from copy import deepcopy
from pathlib import Path
from typing import Callable, Dict, List, Tuple
from json import dumps

from yaml import safe_load
from rio.predict import predict

from rio.teams import Teams
from rio.logger import logger


def load_major(file: Path = Path("./major.yaml")) -> Dict[str, Dict[str, List[Tuple[str]]]]:
    with open(file, "r") as yaml_file:
        return safe_load(yaml_file)


def load_matches(file: Path = Path("./rio.csv")) -> List[dict]:
    with open(file, "r") as csv_file:
        fieldnames = csv_file.readline().split(",")
        return list(DictReader(f=csv_file, fieldnames=fieldnames))


def process_matches(matches: list) -> Teams:
    teams = Teams()
    for match in matches:
        teams.add(team_name=match["Team A"], stage=match["Stage"])
        teams.add(team_name=match["Team B"], stage=match["Stage"])
        teams.get(match["Winner"]).record_win(teams.get(match["Loser"]))
    return teams


def print_block(print_function: Callable, message: str, char: str = "=", length: int = 100):
    print_function(char * length)
    print_function(f"{message:{char}^{length}}")
    print_function(char * length)


def main():
    matches = load_matches(file=Path("./cop.csv"))
    teams = process_matches(matches)
    major = load_major()

    for team in teams.legends:
        logger.debug(f"{team}")

    for stage_name, rounds in major.items():
        print_block(logger.info, f" {stage_name} ", char="*")

        for round, matches in rounds.items():
            print_block(logger.info, f" {round} ")
            for team_a_name, team_b_name in matches:
                print_block(logger.info, f" {round}: {team_a_name} vs {team_b_name} ", char='-')
                team_a = teams.get(team_a_name)
                logger.info(team_a)
                team_b = teams.get(team_b_name) 
                logger.info(team_b)
                winner = predict(team_a, team_b)
                print_block(logger.info, f"Winner is {winner.name}!", char=" ")
                loser = team_b if team_a == winner else team_a
                winner.record_win(loser)


if __name__ == "__main__":
    main()
