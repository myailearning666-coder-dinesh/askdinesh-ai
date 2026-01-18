import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "d365fo_modules_end_to_end_concepts.csv")

df = pd.read_csv(CSV_PATH)

STOP_WORDS = {"how", "to", "is", "the", "a", "an", "of", "for"}

def simple_retrieve(question: str, module: str = "All", k: int = 5):
    keywords = [
        word for word in question.lower().split()
        if word not in STOP_WORDS
    ]

    results = []

    for _, row in df.iterrows():
        text = (
            f"{row['Title']} "
            f"{row['Module']} "
            f"{row['EntityOrTable']} "
            f"{row['WhatIsIt']} "
            f"{row['HowToCreateOrConfigure']}"
        ).lower()

        # ✅ Match ANY keyword, not ALL
        if any(keyword in text for keyword in keywords):
            if module == "All" or row["Module"].lower() == module.lower():
                results.append({
                    "content": text,
                    "module": row["Module"]
                })

        if len(results) >= k:
            break

    return results
