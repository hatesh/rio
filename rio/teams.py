from __future__ import annotations
from typing import List

from rio.team import Team

from .logger import logger


class Teams:
    def __init__(self):
        self._teams = {}
        self._qualifiers = {}
        self._challengers = {}
        self._legends = {}

    def __iter__(self):
        return iter(sorted(self.teams.values(), key=lambda team: team.elo))

    @property
    def teams(self) -> dict:
        return self._teams

    @property
    def challengers(self) -> list:
        return sorted(self._challengers.values(), key=lambda team: team.elo)

    @property
    def legends(self) -> list:
        return sorted(self._legends.values(), key=lambda team: team.elo)

    @property
    def team_names(self) -> List[str]:
        return self.teams.keys()

    def add(self, team_name: str, stage: str = None):
        team_name = team_name.upper()
        if team_name not in self.teams.keys():
            team = Team(team_name)
            self._teams[team_name] = team
        else:
            team = self._teams[team_name]

        if stage is not None:
            if (
                "challangers" in stage.lower()
                and team_name not in self._challengers.keys()
            ):
                self._challengers[team_name] = team

            if "legends" in stage.lower() and team_name not in self._legends.keys():
                self._legends[team_name] = team

    def get(self, team_name: str) -> Team:
        team_name = team_name.upper()
        self.add(team_name)
        return self.teams.get(team_name)
