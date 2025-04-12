from github import Github
from github import Auth
import csv
import pandas as pd

def retreiveProjects(auth, language, numOfProjects):
   g = Github(auth=auth)
   query = f"language:{language}"
   language_repos = g.search_repositories(query=query, sort='stars', order='desc')
  
   project_list = [extractInfo(repo) for repo in language_repos[:int(numOfProjects)]]
   
   # df_repos = pd.DataFrame(project_list)
   # df_repos.to_csv('Repo_Dataset.csv', sep=', ', encoding = 'utf-8', index = False)
   for repo in project_list:
      print(repo)
   
def extractInfo(repo):
      return {
         'Repository Name': repo.name,
         'ID': repo.id,
         'Programming Language': repo.language,
         'Stars': repo.stargazers_count,
         'Forks': repo.forks_count,
         'Watchers': repo.subscribers_count,
         'PRs': repo.get_pulls(state='all').totalCount
      }

     
    
def main():
   language = input("Enter the programming language of the projects: ")
   numOfProjects = input("Enter the (top) number of projects: ")
   token = input("Enter your own token: ")
   auth = Auth.Token(token)
   # "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"

   retreiveProjects(auth, language, numOfProjects)


if __name__ == "__main__":
    main()








