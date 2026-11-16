#!/usr/bin/env python3
"""
Extract usernames from Instagram's pending_follow_requests.json and save them to a CSV.

Usage:
    python pending_requests_to_csv.py
    python pending_requests_to_csv.py --input pending_follow_requests.json --output pending_usernames.csv
"""

import argparse
import json

import pandas as pd


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_usernames(data):
    """
    Each record looks like:
      {"timestamp": ..., "media": [], "label_values": [
          {"label": "URL", "value": ""},
          {"label": "Name", "value": "..."},
          {"label": "Username", "value": "..."}
      ], "fbid": "..."}
    The username is the label_values entry whose label is "Username".
    """
    usernames = []
    for record in data:
        for item in record.get("label_values", []):
            if item.get("label") == "Username" and item.get("value"):
                usernames.append(item["value"])
    return usernames


def main():
    parser = argparse.ArgumentParser(description="Extract usernames from pending follow requests.")
    parser.add_argument("--input", default="pending_follow_requests.json", help="Input JSON file")
    parser.add_argument("--output", default="pending_usernames.csv", help="Output CSV file")
    args = parser.parse_args()

    usernames = extract_usernames(load_json(args.input))


    df = pd.DataFrame({"username": usernames})
    print(df)
    df.to_csv(args.output, index=False)

    print(f"Found {len(usernames)} usernames")
    print(df.to_string(index=False))
    print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()