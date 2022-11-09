from rio.team import Team
from rio.logger import logger


def predict(team_a: Team, team_b: Team) -> Team | None:
    logger.debug(
        f"Looking out who would win out of {team_a.name} and {team_b.name}..."
    )

    if team_b.name in team_a.fought_against:
        logger.debug(
            f"{team_a.name} and {team_b.name} have already fought one another"
        )
        return team_a if team_a.compare(team_b) > 0 else team_b

    if not team_a.win_rate == team_b.win_rate:
        logger.debug(f"Prediction will be based off of winrate difference ({team_a.name}: {team_a.win_rate:.2f}, {team_b.name}: {team_b.win_rate:.2f})")
        return team_a if team_a.win_rate > team_b.win_rate else team_b

    common_vs = {team_a.name: 0, team_b.name: 0}

    for common_foe in [
        team for team in team_a.fought_against if team in team_b.fought_against
    ]:
        logger.debug(
            f"{team_a.name} and {team_b.name} have both fought {common_foe}"
        )
        compare_a = team_a.compare(common_foe)
        common_vs[team_a.name] += compare_a
        logger.debug(
            f"{team_a.name} {'won' if compare_a > 0 else 'lost' if compare_a < 0 else 'tied'} against {common_foe}"
        )
        compare_b = team_b.compare(common_foe)
        common_vs[team_b.name] += team_b.compare(common_foe)
        logger.debug(
            f"{team_b.name} {'won' if compare_b > 0 else 'lost' if compare_b < 0 else 'tied'} against {common_foe}"
        )

    logger.debug(f"Common foe wins: {common_vs}")

    if common_vs[team_a.name] == common_vs[team_b.name]:
        logger.debug(f"Prediction will be based off of elo difference ({team_a.name}: {team_a.elo}, {team_b.name}: {team_b.elo})")
        return team_a if team_a.elo > team_b.elo else team_b

    return team_a if common_vs[team_a.name] > common_vs[team_b.name] else team_b
