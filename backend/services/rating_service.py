import math
from typing import List, Tuple

class RatingSystem:
    RANKS = [
        (0, "Newbie", "#CCCCCC"), (1200, "Pupil", "#77FF77"),
        (1400, "Specialist", "#77DDBB"), (1600, "Expert", "#AAAAFF"),
        (1900, "Candidate Master", "#FF88FF"), (2100, "Master", "#FFCC88"),
        (2300, "International Master", "#FFBB55"), (2400, "Grandmaster", "#FF7777"),
        (2600, "International Grandmaster", "#FF3333"), (3000, "Legendary Grandmaster", "#AA0000"),
    ]
    
    @staticmethod
    def get_rank(rating: int) -> Tuple[str, str]:
        for threshold, rank, color in reversed(RatingSystem.RANKS):
            if rating >= threshold: return rank, color
        return "Newbie", "#CCCCCC"
    
    @staticmethod
    def calculate_expected_score(rating_a: int, rating_b: int) -> float:
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))
    
    @staticmethod
    def calculate_rating_change(current_rating: int, current_volatility: float, opponent_ratings: List[int], actual_scores: List[float], weight: float = 1.0) -> Tuple[int, float]:
        if not opponent_ratings: return current_rating, current_volatility
        expected = [RatingSystem.calculate_expected_score(current_rating, opp) for opp in opponent_ratings]
        total_expected = sum(expected) / len(expected)
        total_actual = sum(actual_scores) / len(actual_scores)
        k = max(10, 32 * weight / (1 + 0.01 * current_volatility))
        change = k * (total_actual - total_expected) * len(opponent_ratings)
        std = math.sqrt(sum((a - e) ** 2 for a, e in zip(actual_scores, expected)) / max(len(actual_scores), 1))
        new_vol = math.sqrt((current_volatility ** 2 + std ** 2) / 2)
        return max(100, round(current_rating + change)), min(300, new_vol)
    
    @staticmethod
    def calculate_dynamic_points(base: int, attempts: int, solves: int, decay: float = 0.95) -> int:
        if solves == 0: return base
        ratio = solves / max(attempts, 1)
        return max(int(base * 0.3), round(base * (decay ** (solves * ratio))))
