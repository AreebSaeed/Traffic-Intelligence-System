import pandas as pd

from config import INTERMEDIATE_DIR, LABELED_OUTPUT, MERGED_OUTPUT


def generate_labels() -> pd.DataFrame:
    """
    Placeholder label generation until real traffic observations are available.
    Produces a proxy congestion score from time, weather, and event features.
    """
    df = pd.read_csv(MERGED_OUTPUT, parse_dates=["datetime", "date"])

    score = (
        df["is_rush_hour"] * 2
        + df["is_weekend"] * 0.5
        + df["is_holiday"] * 1.5
        + df["is_event_day"] * 2
        + (df["rain"].fillna(0) > 0).astype(int) * 1
        + (df["cloud_cover"].fillna(0) > 80).astype(int) * 0.5
    )

    df["congestion_score"] = score
    df["traffic_level"] = pd.cut(
        score,
        bins=[-1, 2, 4, 10],
        labels=["low", "medium", "high"],
    )

    return df


if __name__ == "__main__":
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    labeled_df = generate_labels()
    labeled_df.to_csv(LABELED_OUTPUT, index=False)
    print(f"Saved {len(labeled_df)} labeled records to {LABELED_OUTPUT}")
