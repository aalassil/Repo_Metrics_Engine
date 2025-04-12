import sys
sys.setrecursionlimit(10**6)

from pydriller import Repository
import csv
import requests

def get_repository_data(username, repository):
    data = []

    url = f"https://api.github.com/repos/{username}/{repository}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_info = response.json()
        forks_count = repo_info["forks_count"]
        open_issues_count = repo_info["open_issues_count"]
        print(f"Total Forks: {forks_count}")
        print(f"Total Open Issues: {open_issues_count}")
    else:
        print(f"Failed to fetch repository info. Status code: {response.status_code}")
        forks_count = None
        open_issues_count = None

    i = 1
    for commit in Repository(f"https://github.com/{username}/{repository}").traverse_commits():
        i += 1

    print(f"Total Commits: {i}")

    i = 1
    for commit in Repository(f"https://github.com/{username}/{repository}").traverse_commits():
        print(i)
        commit_data = {
            "Hash": commit.hash,
            "Message": commit.msg,
            "Author Name": commit.author.name,
            "Author Email": commit.author.email,
            "Committer Name": commit.committer.name,
            "Committer Email": commit.committer.email,
            "Author Date": commit.author_date,
            "Committer Date": commit.committer_date,
            "Branches": ', '.join(commit.branches),
            "In Main Branch": commit.in_main_branch,
            "Merge": commit.merge,
            "Parents": ', '.join(commit.parents),
            "Project Name": commit.project_name,
            "Project Path": commit.project_path,
            "Deletions": commit.deletions,
            "Insertions": commit.insertions,
            "Lines": commit.lines,
            "Files": commit.files,
            "DMM Unit Size": commit.dmm_unit_size,
            "DMM Unit Complexity": commit.dmm_unit_complexity,
            "DMM Unit Interfacing": commit.dmm_unit_interfacing,
            "Total Forks": forks_count,
            "Total Open Issues": open_issues_count
        }

        i += 1

        data.append(commit_data)

    return data

if __name__ == "__main__":
    username = input("Enter GitHub username: ")
    repository = input("Enter repository name: ")
    repository_data = get_repository_data(username, repository)

    with open(f"{repository}.csv", "w", newline="") as csvfile:
        fieldnames = list(repository_data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in repository_data:
            writer.writerow(row)

    print(f"Data exported to {repository}.csv")
# print('json data: ', repository_data)