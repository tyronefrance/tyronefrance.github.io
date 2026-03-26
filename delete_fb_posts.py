import requests
import time

PAGE_ID = "tyfrauk"  # or use the numeric page ID
ACCESS_TOKEN = "PASTE_YOUR_PAGE_ACCESS_TOKEN_HERE"

BASE_URL = "https://graph.facebook.com/v19.0"

def get_all_posts():
    posts = []
    url = f"{BASE_URL}/{PAGE_ID}/posts"
    params = {"access_token": ACCESS_TOKEN, "limit": 100, "fields": "id,message,created_time"}

    while url:
        res = requests.get(url, params=params)
        data = res.json()

        if "error" in data:
            print(f"Error fetching posts: {data['error']['message']}")
            break

        batch = data.get("data", [])
        posts.extend(batch)
        print(f"Fetched {len(posts)} posts so far...")

        # Follow pagination
        url = data.get("paging", {}).get("next")
        params = {}  # params are already encoded in the 'next' URL

    return posts

def delete_post(post_id):
    url = f"{BASE_URL}/{post_id}"
    res = requests.delete(url, params={"access_token": ACCESS_TOKEN})
    return res.json()

def main():
    print("Fetching all posts...")
    posts = get_all_posts()
    print(f"\nFound {len(posts)} posts total.")

    if not posts:
        print("No posts to delete.")
        return

    confirm = input(f"\nDelete ALL {len(posts)} posts? Type YES to confirm: ")
    if confirm != "YES":
        print("Aborted.")
        return

    deleted = 0
    failed = 0
    for post in posts:
        result = delete_post(post["id"])
        if result.get("success"):
            deleted += 1
            print(f"[{deleted}/{len(posts)}] Deleted {post['id']}")
        else:
            failed += 1
            print(f"Failed to delete {post['id']}: {result}")
        time.sleep(0.3)  # avoid rate limiting

    print(f"\nDone. Deleted: {deleted}, Failed: {failed}")

if __name__ == "__main__":
    main()
