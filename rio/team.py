from __future__ import annotations
from copy import deepcopy
from typing import List, Tuple

from yaml import safe_load

from .logger import logger


LOW_ELO_MULTIPLER = 0.2
HIGH_ELO_MULTIPLIER = 1


with open("./teams.yaml", "r") as yaml_file:
    TEAM_ELOS = safe_load(yaml_file)


def get_team_region(team_name: str) -> Tuple[str, int]:
    for region_name, region in TEAM_ELOS.items():
        if team_name in [
            team.upper() for team in region["teams"] if isinstance(team, str)
        ]:
            elo = region["base_elo"]
            return region_name, elo

        for dict_team in [team for team in region["teams"] if isinstance(team, dict)]:
            for name in dict_team.keys():
                if name.upper() == team_name:
                    elo = dict_team[name]
                    logger.debug(
                        f"{team_name} from {region_name} (setting starting elo to {elo})"
                    )
                    return region_name, elo
    return "Unknown", 1000


class Team:
    def __init__(self, name: str):
        self.name = name.upper()
        self._wins = {}
        self._losses = {}
        self._net = None
        self._net_cached = False
        self.region, self.elo = get_team_region(team_name=name)
        self._win_count = 0
        self._matches = 0

    def __str__(self) -> str:
        return f"{self.name} ({self.region}) [Wins: {self.wins} / {self._matches} | {self.win_rate:.2f}%] [Net Wins: {self.total}] [Elo: {self.elo}]"

    def __eq__(self, other: Team) -> bool:
        return self.name == other.name

    @property
    def wins(self) -> int:
        return self._win_count

    @property
    def win_rate(self) -> float:
        if self._matches <= 0:
            return 0
        return (self._win_count / self._matches) * 100

    @property
    def won(self) -> dict:
        return self._wins

    @property
    def won_against(self) -> List[str]:
        return self.won.keys()

    @property
    def lost(self) -> dict:
        return self._losses

    @property
    def lost_against(self) -> List[str]:
        return self.lost.keys()

    @property
    def net(self) -> dict:
        if self._net_cached:
            return self._net
        self._net = deepcopy(self.won)
        for other_team_name, losses in self.lost.items():
            if other_team_name not in self._net.keys():
                self._net[other_team_name] = 0
            self._net[other_team_name] -= losses
        self._net_cached = True
        return self._net

    @property
    def total(self) -> int:
        return sum(net_val for net_val in self.net.values())

    @property
    def fought_against(self) -> List[str]:
        return self.net.keys()

    def compare(self, other_team: Team | str) -> int:
        other_team_name = (
            other_team.name if isinstance(other_team, Team) else other_team
        )
        return self.net.get(other_team_name, 0)

    def record_win(self, other_team: Team):
        logger.info(f"Recording win for {self.name} against {other_team.name}")
        if other_team.name not in self.won.keys():
            self._wins[other_team.name] = 0
        self._wins[other_team.name] += 1
        elo_change = round(self.elo_calc(other_team, won=True))
        other_team.record_loss(self)
        self.elo += elo_change
        self._net_cached = False
        self._win_count += 1
        self._matches += 1

    def elo_calc(self, other_team: Team, won: bool) -> float:
        # If they have the same elo, just change elo by 10%
        if self.elo == other_team.elo:
            return 0.1 * self.elo

        if won:
            skill_multiplier = (
                LOW_ELO_MULTIPLER if self.elo > other_team.elo else HIGH_ELO_MULTIPLIER
            )
        else:
            skill_multiplier = (
                HIGH_ELO_MULTIPLIER if self.elo > other_team.elo else LOW_ELO_MULTIPLER
            )

        delta = abs(self.elo - other_team.elo)
        return skill_multiplier * delta

    def record_loss(self, other_team: Team):
        if other_team.name not in self.lost.keys():
            self._losses[other_team.name] = 0
        self._losses[other_team.name] += 1
        self._net_cached = False
        self.elo -= round(self.elo_calc(other_team, won=False))
        self._matches += 1
