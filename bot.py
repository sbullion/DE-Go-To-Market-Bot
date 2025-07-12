import json
import csv
import sys

# -------------------------
# Dummy data for all platforms
# -------------------------
DUMMY_POSTS = {
    "twitter": [
        {"url": "https://twitter.com/post1", "text": "Bug bounty payouts are pathetic."},
        {"url": "https://twitter.com/post2", "text": "I love bug bounty programs."},
        {"url": "https://twitter.com/post3", "text": "I wasted days on this bug bounty with nothing to show."},
        {"url": "https://twitter.com/post4", "text": "Feeling frustrated after another bug bounty rejection."},
        {"url": "https://twitter.com/post5", "text": "Bug bounty hunting is the best way to learn security."},
        {"url": "https://twitter.com/post6", "text": "Bug bounty payouts seem like a scam sometimes."}
    ],
    "linkedin": [
        {"url": "https://linkedin.com/post1", "text": "Frustrated with bug bounties wasting my time."},
        {"url": "https://linkedin.com/post2", "text": "Bug bounty success story!"},
        {"url": "https://linkedin.com/post3", "text": "I think bug bounty programs are underpaying researchers."},
        {"url": "https://linkedin.com/post4", "text": "Bug bounties are a waste of time for serious security work."},
        {"url": "https://linkedin.com/post5", "text": "Just landed my first bug bounty payout, feeling accomplished!"},
        {"url": "https://linkedin.com/post6", "text": "Another rejection email from a bug bounty, getting tired of this."}
    ],
    "reddit": [
        {"url": "https://reddit.com/r/netsec/post1", "text": "Bug bounty scam ruined my day."},
        {"url": "https://reddit.com/r/netsec/post2", "text": "Bug bounty programs are great for learning."},
        {"url": "https://reddit.com/r/netsec/post3", "text": "Why do bug bounties always feel like a waste of time?"},
        {"url": "https://reddit.com/r/netsec/post4", "text": "Just got ghosted by a bug bounty program. Frustrating!"},
        {"url": "https://reddit.com/r/netsec/post5", "text": "Happy to contribute to open source and bug bounties alike."},
        {"url": "https://reddit.com/r/netsec/post6", "text": "Bug bounty payout was less than a cup of coffee. Pathetic."}
    ]
}

NEGATIVE_KEYWORDS = ["frustrated", "pathetic", "scam", "waste"]

results = []

def contains_negative_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw in text_lower for kw in keywords)

def save_results_json_csv(results):
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["platform", "url", "text", "decision"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)

def review_posts(posts, platform):
    post_idx = 0
    has_negative = False

    while post_idx < len(posts):
        post = posts[post_idx]

        if contains_negative_keywords(post["text"], NEGATIVE_KEYWORDS):
            has_negative = True
            print("\nPost Content:")
            print(f"{post['url']} Posted by [username] on [date] – \"{post['text']}\"")

            while True:
                decision = input("\nWould you like to comment offering Desired Effect as a solution? (y/n/q to quit this review): ").strip().lower()
                if decision == "y":
                    print("Reply successful!")
                    results.append({"platform": platform, "url": post["url"], "text": post["text"], "decision": "y"})
                    post_idx += 1
                    break
                elif decision == "n":
                    results.append({"platform": platform, "url": post["url"], "text": post["text"], "decision": "skipped"})
                    post_idx += 1
                    break
                elif decision == "q":
                    post_idx = len(posts)  # exit current review loop
                    break
                else:
                    print("Invalid input. Please enter y, n, or q.")
        else:
            post_idx += 1

    if not has_negative:
        print(f"\nNo posts with negative keywords found in {platform.upper()}.")
    else:
        print(f"\nFinished reviewing posts from {platform.upper()}.")

def main():
    keywords = sys.argv[1:] if len(sys.argv) > 1 else NEGATIVE_KEYWORDS
    platforms = list(DUMMY_POSTS.keys())

    while True:
        # Main menu
        print("\nAvailable options:")
        for idx, p in enumerate(platforms, 1):
            print(f"[{idx}] {p}")
        print("[A] All platforms")
        print("[Q] Quit")
        choice = input("Select an option (1-{}, A, or Q): ".format(len(platforms))).strip().lower()

        if choice == "q":
            print("\nQuitting and saving results...")
            save_results_json_csv(results)
            sys.exit(0)

        if choice == "a":
            print("\nSwitched to reviewing all platforms combined.")
            combined_posts = []
            for platform_name in platforms:
                for post in DUMMY_POSTS[platform_name]:
                    combined_posts.append({
                        "platform": platform_name,
                        "url": post["url"],
                        "text": post["text"]
                    })
            review_posts(combined_posts, "all-platforms")
            continue

        if not choice.isdigit() or not (1 <= int(choice) <= len(platforms)):
            print("Invalid choice. Please try again.")
            continue

        platform_idx = int(choice) - 1
        platform = platforms[platform_idx]
        print(f"\nSwitched to platform: {platform.upper()}")
        posts = DUMMY_POSTS[platform]
        review_posts(posts, platform)

if __name__ == "__main__":
    main()

