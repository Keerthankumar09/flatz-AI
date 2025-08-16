import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")


users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
items_df = pd.read_csv(os.path.join(DATA_DIR, "items.csv"))
interactions_df = pd.read_csv(os.path.join(DATA_DIR, "interactions.csv"))

def get_recommendations(user_id: int, top_n: int = 5):
    user = users_df[users_df["user_id"] == user_id].iloc[0]
    user_community = user["community"]

    # Filter items for the same community
    community_items = items_df[items_df["community"] == user_community]

    # Score based on interaction frequency
    item_scores = interactions_df.groupby("item_id")["interaction_type"].count().reset_index()
    item_scores.rename(columns={"interaction_type": "score"}, inplace=True)

    ranked_items = community_items.merge(item_scores, on="item_id", how="left").fillna(0)
    ranked_items = ranked_items.sort_values(by="score", ascending=False)

    recommendations = []
    for _, row in ranked_items.head(top_n).iterrows():
        reason = f"Popular in your community ({user_community})"
        recommendations.append({
            "item_id": row["item_id"],
            "title": row["title"],
            "description": row["description"],
            "reason": reason
        })
    
    return recommendations
