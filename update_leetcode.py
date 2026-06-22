import requests
import json

LEETCODE_USERNAME = "_Tharun_13"

def get_leetcode_stats(username):
    url = "https://leetcode-stats-api.herokuapp.com/" + username
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Try primary API
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") != "error":
                return {
                    "easy": data.get("easySolved", 0),
                    "medium": data.get("mediumSolved", 0),
                    "hard": data.get("hardSolved", 0),
                    "total": data.get("totalSolved", 0)
                }
    except Exception as e:
        print(f"Primary API failed: {e}")

    # Try backup API
    try:
        query = {
            "query": """
            query getUserProfile($username: String!) {
                matchedUser(username: $username) {
                    submitStatsGlobal {
                        acSubmissionNum {
                            difficulty
                            count
                        }
                    }
                }
            }
            """,
            "variables": {"username": username}
        }
        response = requests.post(
            "https://leetcode.com/graphql",
            json=query,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            stats = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
            result = {"easy": 0, "medium": 0, "hard": 0, "total": 0}
            for item in stats:
                if item["difficulty"] == "Easy":
                    result["easy"] = item["count"]
                elif item["difficulty"] == "Medium":
                    result["medium"] = item["count"]
                elif item["difficulty"] == "Hard":
                    result["hard"] = item["count"]
                elif item["difficulty"] == "All":
                    result["total"] = item["count"]
            return result
    except Exception as e:
        print(f"Backup API failed: {e}")

    return None

def update_readme(stats):
    print(f"Stats fetched: Easy={stats['easy']}, Medium={stats['medium']}, Hard={stats['hard']}, Total={stats['total']}")
    
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "Easy" in line and "|" in line and "Difficulty" not in line:
            new_lines.append(f"| 🟢 Easy | {stats['easy']} |\n")
        elif "Medium" in line and "|" in line:
            new_lines.append(f"| 🟡 Medium | {stats['medium']} |\n")
        elif "Hard" in line and "|" in line:
            new_lines.append(f"| 🔴 Hard | {stats['hard']} |\n")
        elif "**Total**" in line and "|" in line:
            new_lines.append(f"| **Total** | **{stats['total']}** |\n")
        else:
            new_lines.append(line)

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("README updated successfully.")

def main():
    stats = get_leetcode_stats(LEETCODE_USERNAME)
    if stats:
        update_readme(stats)
    else:
        print("Failed to fetch LeetCode stats from all sources.")

if __name__ == "__main__":
    main()
