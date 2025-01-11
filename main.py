import requests
from bs4 import BeautifulSoup
import subprocess


def extract_contributions(url):
    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")

    contributions_td = []
    contributions_tooltip = []
    for row in rows:
        contributions_td.extend(row.find_all("td")[1:])
        contributions_tooltip.extend(row.find_all("tool-tip"))
    assert len(contributions_td) == len(contributions_tooltip)

    contributions = {}
    for i in range(len(contributions_td)):
        _date = contributions_td[i]["data-date"]
        _count = int(contributions_tooltip[i].text.replace("No", "0").split(" ")[0])
        contributions[_date] = _count
    return contributions


def git_commit(commit_message="Your commit message here", date="YYYY-MM-DD HH:MM:SS", name="Your Name", email="Your Email"):
    env = {
        "GIT_AUTHOR_DATE": date,
        "GIT_COMMITTER_DATE": date,
        "GIT_AUTHOR_NAME": name,
        "GIT_COMMITTER_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_COMMITTER_EMAIL": email,
    }
    subprocess.run(["git", "commit", "-m", commit_message, "--allow-empty"], env=env)

def get_random_times(start_time="9:20:00", end_time="17:10:00", count=3):
    import random
    import datetime
    start = datetime.datetime.strptime(start_time, "%H:%M:%S")
    end = datetime.datetime.strptime(end_time, "%H:%M:%S")
    seconds = (end - start).total_seconds()
    # ToDo randomize it better
    times = [start + datetime.timedelta(seconds=random.randint(0, seconds)) for _ in range(count)]
    return [time.strftime("%H:%M:%S") for time in times]

# Flow
# 1. Extract contributions
url = "https://github.com/users/torvalds/contributions"
contributions = extract_contributions(url)

# 2. Date Filter
start_date = "2023-01-01"
end_date = "2024-01-01"
selected_contributions = {k: v for k, v in contributions.items() if start_date <= k <= end_date}

# 3. Commit
for _date, count in selected_contributions.items():
    times = get_random_times(start_time="9:20:00", end_time="17:10:00", count=count)
    for _time in times:
        _date = f"{_date} {_time}"
        git_commit(
            commit_message=f"Commit on {_date} {_time}",
            date=_date,
            name="i3130002",
            email="i3130002@gmail.com",
        )