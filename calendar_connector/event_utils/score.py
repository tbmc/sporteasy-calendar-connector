from typing import Literal, cast, Any

from calendar_connector.consts import EVENT_TYPE


def _extract_scores_for_opponent(
    event_data: EVENT_TYPE, left_or_right: Literal["left", "right"]
) -> tuple[str, int] | None:
    opponent = event_data.get(f"opponent_{left_or_right}")
    if opponent is None:
        return None
    opponent = cast(dict[str, Any], opponent)
    score_str = opponent.get("score")
    if score_str is None:
        return None
    name = cast(str, opponent.get("short_name"))
    score = int(cast(str, score_str))
    return name, score


def extract_scores(event_data: EVENT_TYPE) -> str | None:
    left = _extract_scores_for_opponent(event_data, "left")
    right = _extract_scores_for_opponent(event_data, "right")

    if left is None or right is None:
        return None

    left_name, left_score = left
    right_name, right_score = right
    return f"{left_name} {left_score} - {right_score} {right_name}"
