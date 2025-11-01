# fetch_saved_posts.py
import requests
import json

cookies = {}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://www.instagram.com/aaryanshhhhh/saved/",
    "Origin": "https://www.instagram.com",
    "X-CSRFToken": cookies.get("csrftoken"),
}

url = "https://www.instagram.com/graphql/query/"

data = {
    "doc_id": "24676492415387152",
    "variables": json.dumps({}),
    "av": "17841467141519613",
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "PolarisProfileSavedPostsTabContentQuery",
    "server_timestamps": "true",
}


def extract_reels_data(response_json):
    reels = []

    try:
        edges = (
            response_json.get("data", {})
            .get("xdt_api__v1__feed__saved__posts_connection", {})
            .get("edges", {})
        )

        for edge in edges:
            media = edge.get("node", {}).get("media", {})
            if media.get("media_type") == 2:
                reel_data = {
                    "id": media.get("id"),
                    "code": media.get("code"),
                    "caption": media.get("caption", {}).get("text"),
                    "username": media.get("user", {}).get("username"),
                    "like_count": media.get("like_count"),
                }
                reels.append(reel_data)
    except Exception as e:
        print("Error extracting data: ", e)

    return reels


def fetch():
    r = requests.post(url, headers=headers, cookies=cookies, data=data, timeout=30)
    print("status:", r.status_code)
    # try to parse JSON if possible
    try:
        j = r.json()
        reels_data = extract_reels_data(j)
        print(reels_data)
        # print(json.dumps(j, indent=2)[:10000])  # print up to 10k chars
        return reels_data
    except ValueError:
        print("non-json response (first 2000 chars):")
        print(r.text[:2000])
        return None


if __name__ == "__main__":
    fetch()
