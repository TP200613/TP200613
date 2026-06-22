import requests
import re

LEETCODE_USERNAME = "_Tharun_13"

def get_leetcode_stats(username):
    url = "https://leetcode-stats-api.herokuapp.com/" + username
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "easy": data.get("easySolved", 0),
            "medium": data.get("mediumSolved", 0),
            "hard": data.get("hardSolved", 0),
            "total": data.get("totalSolved", 0)
        }
    return None

def update_readme(stats):
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "Easy |" in line and "Difficulty" not in line:
            new_lines.append(f"| 🟢 Easy | {stats['easy']} |\n")
        elif "Medium |" in line:
            new_lines.append(f"| 🟡 Medium | {stats['medium']} |\n")
        elif "Hard |" in line:
            new_lines.append(f"| 🔴 Hard | {stats['hard']} |\n")
        elif "**Total**" in line:
            new_lines.append(f"| **Total** | **{stats['total']}** |\n")
        else:
            new_lines.append(line)

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"Updated: Easy={stats['easy']}, Medium={stats['medium']}, Hard={stats['hard']}, Total={stats['total']}")

def main():
    stats = get_leetcode_stats(LEETCODE_USERNAME)
    if stats:
        update_readme(stats)
    else:
        print("Failed to fetch LeetCode stats")

if __name__ == "__main__":
    main()
