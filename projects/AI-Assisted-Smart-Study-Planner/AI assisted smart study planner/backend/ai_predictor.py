"""
ai_predictor.py — AI Productivity Prediction Engine

This module implements the ML-based productivity prediction system.

Approach:
  1. Collect user's last 7-day study history (hours, focus scores, times)
  2. Apply weighted regression + time-pattern analysis
  3. Predict today's productivity score (0–100)
  4. Identify peak study time windows

In a production setting, this can be upgraded to:
  - scikit-learn LinearRegression or RandomForestRegressor
  - TensorFlow/Keras LSTM for time-series forecasting
  - Personalized recommendation engine

For simplicity + portability, this uses statistical heuristics that
closely approximate ML results without requiring heavy ML libraries.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math


class ProductivityPredictor:
    """
    AI-based Productivity Predictor.

    Uses heuristic methods inspired by:
      - Exponential weighted moving average (EWMA)
      - Circadian rhythm modeling (time-of-day scoring)
      - Study consistency scoring
      - Recency-weighted trend analysis
    """

    # Time-of-day productivity weights (based on circadian rhythm research)
    HOURLY_BASE_WEIGHTS = {
        0: 0.20,  1: 0.15,  2: 0.10,  3: 0.10,  4: 0.15,  5: 0.25,
        6: 0.40,  7: 0.55,  8: 0.68,  9: 0.75, 10: 0.80, 11: 0.78,
       12: 0.65, 13: 0.58, 14: 0.50, 15: 0.58, 16: 0.68, 17: 0.72,
       18: 0.88, 19: 0.92, 20: 0.90, 21: 0.82, 22: 0.70, 23: 0.50,
    }

    def predict(
        self,
        productivity_records: List[Dict],
        sessions: List[Dict],
        current_hour: int = 18,
    ) -> Dict[str, Any]:
        """
        Main prediction method.

        Args:
            productivity_records: List of past daily productivity dicts
            sessions:             List of past study session dicts
            current_hour:         Current hour of day (0-23)

        Returns:
            dict with keys:
              - predicted_score      : float (0-100)
              - confidence           : str ("HIGH" / "MEDIUM" / "LOW")
              - trend                : str ("IMPROVING" / "STABLE" / "DECLINING")
              - best_study_window    : str (e.g. "6:00 PM – 8:30 PM")
              - best_start_hour      : int
              - recommendation       : str (natural language insight)
              - hourly_scores        : dict[hour → predicted score]
              - today_level          : str ("HIGH" / "MEDIUM" / "LOW")
        """
        scores = [r.get("productivity_score", 0) for r in productivity_records]
        hours  = [r.get("total_hours", 0) for r in productivity_records]

        if not scores:
            # Cold start — use defaults
            return self._cold_start_prediction(current_hour)

        # 1. Exponentially weighted moving average (EWMA)
        ewma_score = self._ewma(scores, alpha=0.4)

        # 2. Adjust for time of day
        time_multiplier = self.HOURLY_BASE_WEIGHTS.get(current_hour, 0.7)
        time_adjusted = ewma_score * (0.7 + 0.3 * time_multiplier / 0.92)

        # 3. Consistency bonus (studying every day gives a boost)
        consistency_bonus = self._consistency_bonus(productivity_records)
        final_score = min(100.0, time_adjusted + consistency_bonus)

        # 4. Trend analysis
        trend = self._compute_trend(scores)

        # 5. Find best study window
        best_hour = self._find_best_hour(sessions, current_hour)
        best_window = self._hour_to_window(best_hour)

        # 6. Predict hourly scores for today
        hourly_scores = self._predict_hourly(ewma_score)

        # 7. Confidence based on data volume
        confidence = "HIGH" if len(scores) >= 5 else "MEDIUM" if len(scores) >= 3 else "LOW"

        today_level = "HIGH" if final_score >= 75 else "MEDIUM" if final_score >= 50 else "LOW"

        recommendation = self._generate_recommendation(
            score=final_score,
            trend=trend,
            best_window=best_window,
            avg_hours=sum(hours) / len(hours) if hours else 0,
        )

        return {
            "predicted_score":   round(final_score, 1),
            "confidence":        confidence,
            "trend":             trend,
            "best_study_window": best_window,
            "best_start_hour":   best_hour,
            "recommendation":    recommendation,
            "hourly_scores":     hourly_scores,
            "today_level":       today_level,
        }

    def find_best_study_times(self, sessions: List[Dict]) -> Dict[str, Any]:
        """
        Analyze session history to identify the user's peak study hours.

        Returns:
            dict with ranked time windows and their average productivity.
        """
        if not sessions:
            return {
                "top_windows": [
                    {"window": "6:00 PM – 8:30 PM", "avg_focus": 88, "rank": 1},
                    {"window": "9:00 AM – 11:00 AM", "avg_focus": 75, "rank": 2},
                    {"window": "4:00 PM – 6:00 PM", "avg_focus": 68, "rank": 3},
                ],
                "message": "Default recommendation based on circadian research."
            }

        # Group sessions by hour bucket and compute avg focus
        hourly_buckets: Dict[int, List[float]] = {}
        for s in sessions:
            hour = s.get("hour_of_day", 18)
            focus = s.get("focus_score", 70)
            if hour not in hourly_buckets:
                hourly_buckets[hour] = []
            hourly_buckets[hour].append(float(focus))

        avg_by_hour = {
            h: sum(scores) / len(scores)
            for h, scores in hourly_buckets.items()
        }

        # Sort by average score
        sorted_hours = sorted(avg_by_hour.items(), key=lambda x: x[1], reverse=True)

        top_windows = [
            {
                "window": self._hour_to_window(hour),
                "avg_focus": round(score, 1),
                "rank": i + 1
            }
            for i, (hour, score) in enumerate(sorted_hours[:3])
        ]

        return {
            "top_windows": top_windows,
            "message": "Based on your historical study sessions."
        }

    def calculate_actual_productivity(
        self,
        duration_minutes: int,
        focus_score: int,
        hour_of_day: int,
    ) -> float:
        """
        Calculate the actual productivity score for a completed session.

        Formula:
          - Base = focus_score (user self-report, 0-100)
          - Duration weight = sigmoid curve (optimal: 50-90 min)
          - Time weight = circadian multiplier
        """
        # Duration score: peaks at 60-90 minutes
        duration_score = 100 * (
            1 / (1 + math.exp(-0.05 * (duration_minutes - 45)))
        ) * (
            1 / (1 + math.exp(0.02 * (duration_minutes - 120)))
        ) * 4

        duration_weight = min(1.0, duration_score / 100)

        time_weight = self.HOURLY_BASE_WEIGHTS.get(hour_of_day, 0.7)

        productivity = (
            0.5 * focus_score +
            0.3 * duration_weight * 100 +
            0.2 * time_weight * 100
        )

        return min(100.0, round(productivity, 1))

    # ─── Private Helpers ──────────────────────────────────────────────────────

    def _ewma(self, values: List[float], alpha: float = 0.4) -> float:
        """Exponentially Weighted Moving Average."""
        if not values:
            return 70.0
        ewma = values[0]
        for v in values[1:]:
            ewma = alpha * v + (1 - alpha) * ewma
        return ewma

    def _consistency_bonus(self, records: List[Dict]) -> float:
        """Award consistency bonus for consecutive study days."""
        if len(records) >= 7:
            return 5.0
        if len(records) >= 5:
            return 3.0
        if len(records) >= 3:
            return 1.5
        return 0.0

    def _compute_trend(self, scores: List[float]) -> str:
        """Simple linear trend detection."""
        if len(scores) < 3:
            return "STABLE"
        recent = scores[-3:]
        first_half  = sum(recent[:len(recent) // 2]) / max(1, len(recent) // 2)
        second_half = sum(recent[len(recent) // 2:]) / max(1, len(recent) - len(recent) // 2)
        diff = second_half - first_half
        if diff > 5:
            return "IMPROVING"
        elif diff < -5:
            return "DECLINING"
        return "STABLE"

    def _find_best_hour(self, sessions: List[Dict], current_hour: int) -> int:
        """Find the best study start hour from historical sessions."""
        if not sessions:
            return 18  # Default: 6 PM

        scores_by_hour: Dict[int, List[float]] = {}
        for s in sessions:
            hour  = s.get("hour_of_day", 18)
            focus = float(s.get("focus_score") or 70)
            if hour not in scores_by_hour:
                scores_by_hour[hour] = []
            scores_by_hour[hour].append(focus)

        best_hour = max(
            scores_by_hour,
            key=lambda h: sum(scores_by_hour[h]) / len(scores_by_hour[h]),
            default=18
        )
        return int(best_hour)

    def _hour_to_window(self, start_hour: int, duration_hours: float = 2.0) -> str:
        """Convert a start hour to a readable time window string."""
        end_hour = start_hour + int(duration_hours)
        end_minutes = int((duration_hours % 1) * 60)

        def fmt(h: int, m: int = 0) -> str:
            ampm = "AM" if h < 12 else "PM"
            h12 = h % 12 or 12
            return f"{h12}:{m:02d} {ampm}"

        return f"{fmt(start_hour)} – {fmt(end_hour, end_minutes)}"

    def _predict_hourly(self, base_score: float) -> Dict[str, float]:
        """Predict score for each hour of the day."""
        return {
            str(h): round(
                base_score * self.HOURLY_BASE_WEIGHTS.get(h, 0.5) / 0.92, 1
            )
            for h in range(6, 23)
        }

    def _cold_start_prediction(self, current_hour: int) -> Dict[str, Any]:
        """Return sensible defaults when no historical data is available."""
        time_weight = self.HOURLY_BASE_WEIGHTS.get(current_hour, 0.7)
        score = round(65 * time_weight / 0.5, 1)

        return {
            "predicted_score":   min(100.0, score),
            "confidence":        "LOW",
            "trend":             "STABLE",
            "best_study_window": "6:00 PM – 8:00 PM",
            "best_start_hour":   18,
            "recommendation":    (
                "Welcome! Start logging study sessions so the AI can "
                "personalize predictions for you. Generally, 6 PM – 9 PM "
                "is when most students perform best."
            ),
            "hourly_scores":     self._predict_hourly(65),
            "today_level":       "MEDIUM",
        }
