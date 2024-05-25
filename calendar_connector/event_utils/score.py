from typing import Literal

from calendar_connector.requests_types.event_type import EventType


def _extract_scores_for_opponent(
    event_data: EventType, left_or_right: Literal["left", "right"]
) -> tuple[str, int] | None:
    if left_or_right == "left":
        opponent = event_data.get("opponent_left")
    else:
        opponent = event_data.get("opponent_right")

    if opponent is None:
        return None

    score_str = opponent["score"]
    if score_str is None:
        return None
    name = opponent["short_name"]
    score = int(score_str)
    return name, score


def extract_scores(event_data: EventType) -> str | None:
    left = _extract_scores_for_opponent(event_data, "left")
    right = _extract_scores_for_opponent(event_data, "right")

    if left is None or right is None:
        return None

    left_name, left_score = left
    right_name, right_score = right
    return f"{left_name} {left_score} - {right_score} {right_name}"
