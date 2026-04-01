import numpy as np
import pandas as pd
from datetime import datetime
import json

def rank_repositories(
    json_path,
    popularity_weights={"stargazers": 0.25, "contributors": 0.5, "watchers": 0.25},
    maturity_weights={"projectAge": 1 / 3, "commits": 1 / 3, "codeLines": 1 / 3},
    apply_penalties=True,
    text_languages=["Text", "Markdown", "CSV"],
):
    """
    Ranks repositories based on popularity and maturity metrics with optional penalties.

    Parameters:
    -----------
    json_path : str
        Path to the JSON file containing repository data in the expected format (IF provided through GHS the 'items' key will be used)
    popularity_weights : dict
        Dictionary of column names and their weights for popularity score (default: {'stargazers': 0.25, 'contributors': 0.5, 'watchers': 0.25})
    maturity_weights : dict
        Dictionary of column names and their weights for maturity score (default: {'projectAge': 1/3, 'commits': 1/3, 'codeLines': 1/3})
    apply_penalties : bool
        Whether to apply pre-defined penalties for stars-to-commits ratio and text percentage (default: True)
    text_languages : list
        List of languages considered as "text" for text percentage calculation (default: ['Text', 'Markdown', 'CSV'])

    Returns:
    --------
    pandas.DataFrame
        Dataframe with calculated scores and rankings
    """
    # If the data is provided in the GHS JSON format (with 'items' key), extract the 'items' list
    with open(json_path, "r") as file:
        data = json.load(file)
        if "items" in data:
            data = data["items"]

    # Load the data
    df = pd.DataFrame(data)

    # Check if the data is in the expected format
    required_columns = [
        "stargazers",
        "contributors",
        "watchers",
        "commits",
        "size",
        "createdAt",
        "metrics",
        "codeLines",
        "forks",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"The input data is missing these required columns: {missing_columns}"
        )

    # Calculate the project age in days without overwriting 'createdAt'
    if "createdAt" in df.columns:
        created_at_dates = pd.to_datetime(df["createdAt"])
        df["projectAge"] = (pd.Timestamp.now() - created_at_dates).dt.days

    # Clean up the structure - remove unnecessary columns
    # CAUTION: For this step we assume that all columns have already been filtered so that all their values are 'False' and thus provide no useful information!
    drop_columns = ["isFork", "isArchived", "isDisabled", "isLocked"]
    columns_to_drop = [col for col in drop_columns if col in df.columns]
    if columns_to_drop:
        df.drop(labels=columns_to_drop, axis=1, inplace=True)

    # Remove rows with missing data in essential columns
    essential_columns = []
    for col in list(popularity_weights.keys()) + list(maturity_weights.keys()):
        if col != "projectAge":  # projectAge is calculated
            essential_columns.append(col)
    df.dropna(subset=essential_columns, inplace=True)

    # POPULARITY SCORE CALCULATION
    # Normalize popularity metrics and calculate weighted score
    for column, weight in popularity_weights.items():
        if column in df.columns:
            norm_col = f"normalized_{column}"
            df[norm_col] = normalize_column(df[column])

    popularity_score = 0
    for column, weight in popularity_weights.items():
        if f"normalized_{column}" in df.columns:
            popularity_score += weight * df[f"normalized_{column}"]
    df["popularity_score"] = popularity_score

    # MATURITY SCORE CALCULATION
    # Normalize maturity metrics and calculate weighted score
    for column, weight in maturity_weights.items():
        if column in df.columns:
            norm_col = f"normalized_{column}"
            df[norm_col] = normalize_column(df[column])

    maturity_score = 0
    for column, weight in maturity_weights.items():
        if f"normalized_{column}" in df.columns:
            maturity_score += weight * df[f"normalized_{column}"]
    df["maturity_score"] = maturity_score

    # Apply penalties if requested
    if apply_penalties:
        # Stars-to-commits ratio penalty
        if "stargazers" in df.columns and "commits" in df.columns:
            df["stars_to_commits"] = (df["stargazers"] + 1) / (
                df["commits"] + 1
            )  # Avoid division by zero
            df["stars_commits_penalty"] = apply_stars_commits_penalty(
                df["stars_to_commits"]
            )
        else:
            df["stars_commits_penalty"] = 1.0

        # Text percentage penalty
        if "metrics" in df.columns:
            df["text_percentage"] = df.apply(
                lambda x: calculate_text_percentage(x["metrics"], text_languages),
                axis=1,
            )
            df["text_penalty"] = apply_text_penalty(df["text_percentage"])
        else:
            df["text_penalty"] = 1.0

        # # Apply combined penalty for educational repositories
        # df['educational_penalty'] = df.apply(apply_educational_repo_penalty, axis=1)
        # Apply two fork based penalties
        if "forks" in df.columns and "stargazers" in df.columns:
            # Calculate and apply forks-to-stars ratio penalty
            df["forks_to_stars"] = (df["forks"] + 1) / (
                df["stargazers"] + 1
            )  # Avoid division by zero
            df["forks_stars_penalty"] = apply_forks_stars_penalty(df["forks_to_stars"])
        else:
            df["forks_stars_penalty"] = 1.0

        # First, add back the forks-to-codeLines calculation and penalty
        if "forks" in df.columns and "codeLines" in df.columns:
            df["forks_to_codeLines"] = (df["forks"] + 1) / (
                df["codeLines"] + 1
            )  # Avoid division by zero
            df["forks_codelines_penalty"] = apply_forks_codelines_penalty(
                df["forks_to_codeLines"]
            )
        else:
            df["forks_codelines_penalty"] = 1.0

        # Apply penalties to scores
        # Apply both stars-to-commits and forks-to-stars penalties to popularity score
        df["popularity_score_pen"] = (
            df["popularity_score"]
            * df["stars_commits_penalty"]
            * df["forks_stars_penalty"]
        )
        # Apply both text and forks-to-codelines penalties to maturity score
        df["maturity_score_pen"] = (
            df["maturity_score"] * df["text_penalty"] * df["forks_codelines_penalty"]
        )
    else:
        # No penalties
        df["popularity_score_pen"] = df["popularity_score"]
        df["maturity_score_pen"] = df["maturity_score"]

    # Calculate the final rank score (equal weight to popularity and maturity)
    df["rank_score"] = (0.5 * df["popularity_score_pen"] + 0.5 * df["maturity_score_pen"]).round(2)

    # Calculate the rank based on the score
    df["rank"] = df["rank_score"].rank(ascending=False)

    # Sort by rank
    return df.sort_values("rank")


def normalize_column(column):
    """Normalize a column using log transformation to a 0-100 scale"""
    return (
        (np.log(column + 1) - np.log(column.min() + 1))
        / (np.log(column.max() + 1) - np.log(column.min() + 1))
        * 100
    )


def apply_stars_commits_penalty(ratio):
    """Apply penalty based on stars-to-commits ratio"""
    conditions = [(ratio > 40), (ratio > 30), (ratio > 20), (ratio > 15), (ratio > 10)]
    choices = [0.1, 0.25, 0.5, 0.75, 0.9]

    # Apply the conditions using numpy.select with default=1.0 (no penalty)
    return np.select(conditions, choices, default=1.0)


def apply_text_penalty(percentage):
    """Apply penalty based on text percentage"""
    conditions = [
        (percentage > 80),
        (percentage > 60),
        (percentage > 25),
        (percentage > 20),
    ]
    choices = [0.1, 0.25, 0.5, 0.75]

    # Apply the conditions using numpy.select with default=1.0 (no penalty)
    return np.select(conditions, choices, default=1.0)


def calculate_text_percentage(metrics_data, text_languages):
    """
    Calculates the percentage of text content in a repository.

    Parameters:
    -----------
    metrics_data : list
        List of dictionaries with metrics data
    text_languages : list
        List of languages considered as "text" for text percentage calculation

    Returns:
    --------
    float
        Percentage of text content in the repository
    """
    if not isinstance(metrics_data, list):
        return 0

    total_lines = 0
    text_lines = 0

    for metric in metrics_data:
        language = metric.get("language", "")
        code_lines = metric.get("codeLines", 0)

        total_lines += code_lines

        # Count the lines of text-based formats
        if language in text_languages:
            text_lines += code_lines

    # Calculate percentage
    return (text_lines / total_lines) * 100 if total_lines > 0 else 0


def apply_forks_stars_penalty(ratio):
    """
    Apply penalty based on forks-to-stars ratio.

    Educational repositories typically have many forks but fewer stars,
    resulting in higher ratios than production repositories.
    """
    conditions = [
        (ratio > 3.0),  # Very strong indicator
        (ratio > 1.2),  # Strong indicator (helps catch eugenp/tutorials)
        (ratio > 1.0),  # Moderate indicator
        (ratio > 0.5),  # Mild indicator
    ]
    choices = [0.2, 0.4, 0.6, 0.9]

    # Apply the conditions using numpy.select with default=1.0 (no penalty)
    return np.select(conditions, choices, default=1.0)


def apply_forks_contributors_penalty(ratio):
    """
    Apply penalty based on forks-to-contributors ratio.

    Educational repositories often have many forks but few contributors,
    as users fork to complete exercises but don't contribute back.
    """
    conditions = [
        (ratio > 150),  # Very strong indicator (catches eugenp/tutorials)
        (ratio > 100),  # Strong indicator
        (ratio > 75),  # Moderate indicator
        (ratio > 50),  # Mild indicator
    ]
    choices = [0.5, 0.7, 0.85, 0.95]

    # Apply the conditions using numpy.select with default=1.0 (no penalty)
    return np.select(conditions, choices, default=1.0)


def apply_forks_codelines_penalty(ratio):
    """
    Apply penalty based on forks-to-codeLines ratio.
    A high ratio indicates potentially educational repositories.

    Based on the analysis of sample repositories, educational repositories
    have significantly higher forks-to-codeLines ratios compared to
    regular project repositories.
    """
    conditions = [
        (ratio > 3.0),  # Very strong indicator of educational repos
        (ratio > 1.0),  # Strong indicator
        (ratio > 0.5),  # Moderate indicator
        (ratio > 0.1),  # Mild indicator
    ]
    choices = [0.1, 0.3, 0.6, 0.8]

    # Apply the conditions using numpy.select with default=1.0 (no penalty)
    return np.select(conditions, choices, default=1.0)


__all__ = [
    "rank_repositories",
    "calculate_text_percentage",
    "apply_text_penalty",
    "apply_stars_commits_penalty",
    "normalize_column",
    "apply_forks_stars_penalty",
    "apply_forks_contributors_penalty",
    "apply_forks_codelines_penalty",
]
