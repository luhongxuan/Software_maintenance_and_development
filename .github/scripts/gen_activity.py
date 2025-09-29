import os, requests, datetime

GH_TOKEN = os.getenv("GH_TOKEN")
GH_REPO = os.getenv("GH_REPO")  # e.g. owner/repo
TIME_WINDOW_HOURS = int(os.getenv("TIME_WINDOW_HOURS", "168"))

headers = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github+json"}

def fetch_commits():
    url = f"https://api.github.com/repos/{GH_REPO}/commits"
    r = requests.get(url, headers=headers, params={"per_page": 10})
    return r.json() if r.status_code == 200 else []

def fetch_prs():
    url = f"https://api.github.com/repos/{GH_REPO}/pulls"
    r = requests.get(url, headers=headers, params={"per_page": 10, "state": "all"})
    return r.json() if r.status_code == 200 else []

def render(commits, prs):
    items = []
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=TIME_WINDOW_HOURS)

    for c in commits:
        dt = datetime.datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z","+00:00"))
        if dt >= cutoff:
            sha = c["sha"][:7]
            msg = c["commit"]["message"].splitlines()[0]
            url = c["html_url"]
            items.append(f"- ✚ Commit `{sha}`: {msg} — {url}")

    for p in prs:
        dt = datetime.datetime.fromisoformat(p["updated_at"].replace("Z","+00:00"))
        if dt >= cutoff:
            num = p["number"]
            title = p["title"]
            url = p["html_url"]
            state = "merged" if p.get("merged_at") else p["state"]
            items.append(f"- 🔀 PR #{num} ({state}): {title} — {url}")

    return "\n".join(items) if items else "_No recent activity yet._"

if __name__ == "__main__":
    commits = fetch_commits()
    prs = fetch_prs()
    print(render(commits, prs))
