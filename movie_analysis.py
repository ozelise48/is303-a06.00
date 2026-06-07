"""
IS 303 - A06
Elise Osmun

Input:
movie_ratings.csv: A dataset of movie records containing columns: 
- title (string)
- genre (string text)
- release_year (written word strings to be converted)
- rating_1_5 (float numbers from 1 to 5)
- times_watched (integer count).            
- platform (string text)

Processes:
- load_data(): Reads the CSV file into a Pandas DataFrame.
- clean_data(): Standardizes text formatting, converts text numbers to digits, and removes rows with missing data.
- validate_data(): Runs assertions to verify types, non-null values, and logical data boundaries.
- analyze_data(): Calculates average ratings grouped by genre, platform, and release year.
- create_chart(): Generates and saves a line chart showing movie ratings over time.

Output:
- Printed tables displaying Average Rating by Genre and Platform.
- A line chart saved to disk as 'ratings_over_time.png'.
"""

import pandas as pd
import matplotlib.pyplot as plt
from word2number import w2n

def load_data():
    # Load csv and return a data frame (df)
    df = pd.read_csv("movie_ratings.csv")
    print(f"Loaded {len(df)} rows from 'movie_ratings.csv'.")
    return df

def clean_data(df):
    # Standardize string data
    df["genre"] = df["genre"].str.strip().str.title()
    df["platform"] = df["platform"].str.strip().str.title()
    
    # Convert text numbers to integers
    df["release_year"] = df["release_year"].apply(w2n.word_to_num)
    
    # Handle missing values
    df = df.dropna(subset=["rating_1_5", "times_watched"])
    
    print(f"After cleaning: {len(df)} rows")
    return df

def validate_data(df):
    assert df[["rating_1_5", "times_watched"]].notna().all().all(), "N/A data cleaning failed."
    assert df["release_year"].dtype == 'int64', "Release year into integer failed."
    assert (df["times_watched"] > 0).all(), "Times watched can not be negative or zero."
    print("All validation checks passed successfully.")

def analyze_data(df):
    # Added .round(2) to ensure high-quality, formatted printed numbers
    avg_rating_genre = df.groupby("genre")["rating_1_5"].mean().round(2)
    print(f"\n=== Average Rating by Genre ===")
    print(avg_rating_genre)

    avg_rating_plat = df.groupby("platform")["rating_1_5"].mean().round(2)
    print(f"\n=== Platform vs Rating Avg ===")
    print(avg_rating_plat)

    ratings_over_time = df.groupby("release_year")["rating_1_5"].mean()
    return ratings_over_time

def create_chart(ratings_over_time):
    ratings_over_time.plot(kind="line", color="blue", marker="o")
    plt.title("Movie Ratings Over Time")
    plt.xlabel("Release Year")
    plt.ylabel("Average Rating (1-5)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("ratings_over_time.png")
    print("\nChart successfully saved as 'ratings_over_time.png'")

# Main pipeline
df = load_data()
df = clean_data(df)
validate_data(df)
ratings_over_time = analyze_data(df)
create_chart(ratings_over_time)