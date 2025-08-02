from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "RobloxProfileChecker/1.0"
}

def get_user_id(username_or_id):
    if username_or_id.isdigit():
        return int(username_or_id)
    url = f"https://users.roblox.com/v1/usernames/users"
    res = requests.post(url, json={"usernames":[username_or_id]}, headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    if data["data"]:
        return data["data"][0]["id"]
    return None

def get_groups(user_id):
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    return data["data"]

def get_badges(user_id):
    url = f"https://badges.roblox.com/v1/users/{user_id}/roblox-badges"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return None
    data = res.json()
    return data["data"]

@app.route("/api/profile", methods=["POST"])
def profile():
    data = request.json
    user_input = data.get("user")
    choice = data.get("choice")  # 'groups', 'badges', or 'both'

    if not user_input or not choice:
        return jsonify({"error":"missing user or choice"}), 400

    user_id = get_user_id(user_input)
    if not user_id:
        return jsonify({"error":"user not found"}), 404

    response = {"userId": user_id}

    if choice in ("groups", "both"):
        groups = get_groups(user_id)
        response["groups"] = groups if groups else []

    if choice in ("badges", "both"):
        badges = get_badges(user_id)
        response["badgesCount"] = len(badges) if badges else 0

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
