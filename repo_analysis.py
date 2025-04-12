import csv
import datetime
import pandas as pd
from collections import Counter

def process_csv(csv_file):
    total_authors = 0
    total_committers = 0
    total_forks = 0
    total_open_issues = 0
    project_name = ""

    authors_counter = Counter()
    committers_counter = Counter()

    author_commit_dates = {}
    committer_commit_dates = {}

    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            authors_counter[(row['Author Name'], row['Author Email'], row['Project Name'])] += 1
            committers_counter[(row['Committer Name'], row['Committer Email'], row['Project Name'])] += 1

            total_forks = int(row['Total Forks'])
            total_open_issues = int(row['Total Open Issues'])
            project_name = row['Project Name']

            # Process author commit dates
            author_key = (row['Author Name'], row['Author Email'], row['Project Name'])
            author_date_str = row['Author Date']
            author_date = datetime.datetime.strptime(author_date_str, '%Y-%m-%d %H:%M:%S%z')
            if author_key not in author_commit_dates:
                author_commit_dates[author_key] = {'first_commit': author_date, 'last_commit': author_date}
            else:
                if author_date < author_commit_dates[author_key]['first_commit']:
                    author_commit_dates[author_key]['first_commit'] = author_date
                if author_date > author_commit_dates[author_key]['last_commit']:
                    author_commit_dates[author_key]['last_commit'] = author_date

            # Process committer commit dates
            committer_key = (row['Committer Name'], row['Committer Email'], row['Project Name'])
            committer_date_str = row['Committer Date']
            committer_date = datetime.datetime.strptime(committer_date_str, '%Y-%m-%d %H:%M:%S%z')
            if committer_key not in committer_commit_dates:
                committer_commit_dates[committer_key] = {'first_commit': committer_date, 'last_commit': committer_date}
            else:
                if committer_date < committer_commit_dates[committer_key]['first_commit']:
                    committer_commit_dates[committer_key]['first_commit'] = committer_date
                if committer_date > committer_commit_dates[committer_key]['last_commit']:
                    committer_commit_dates[committer_key]['last_commit'] = committer_date

    sorted_authors = sorted(authors_counter.items(), key=lambda x: x[1], reverse=True)
    sorted_committers = sorted(committers_counter.items(), key=lambda x: x[1], reverse=True)

    total_authors = len(sorted_authors)
    total_committers = len(sorted_committers)

    return {
        'total_authors': total_authors,
        'total_committers': total_committers,
        'total_forks': total_forks,
        'total_open_issues': total_open_issues,
        'project_name': project_name,
        'sorted_authors': sorted_authors,
        'sorted_committers': sorted_committers,
        'author_commit_dates': author_commit_dates,
        'committer_commit_dates': committer_commit_dates
    }

def write_to_df(authors, committers, author_commit_dates, committer_commit_dates):
    data_rows = []
    # Process author data
    for author, count in authors:
        name, email, project = author
        start_date = author_commit_dates[author]['first_commit'].strftime('%Y-%m-%d')
        end_date = author_commit_dates[author]['last_commit'].strftime('%Y-%m-%d')
        duration = (author_commit_dates[author]['last_commit'] - author_commit_dates[author]['first_commit']).days + 1
        commit_frequency = count / duration if duration > 0 else 0
        data_rows.append(['Author', name, email, project, start_date, end_date, count, commit_frequency])

    # Process committer data
    for committer, count in committers:
        name, email, project = committer
        start_date = committer_commit_dates[committer]['first_commit'].strftime('%Y-%m-%d')
        end_date = committer_commit_dates[committer]['last_commit'].strftime('%Y-%m-%d')
        duration = (committer_commit_dates[committer]['last_commit'] - committer_commit_dates[committer]['first_commit']).days + 1
        commit_frequency = count / duration if duration > 0 else 0
        data_rows.append(['Committer', name, email, project, start_date, end_date, count, commit_frequency])

    return pd.DataFrame(data_rows, columns=['Type', 'Name', 'Email', 'Project', 'Start Date', 'End Date', 'Occurrences', 'Commit Frequency'])

def save_df_to_csv(df, output_file):
    df.to_csv(output_file, index=False)

def main():
    file_name = input("Enter the CSV file name: ")
    result = process_csv(file_name)

    df = write_to_df(result['sorted_authors'], result['sorted_committers'], result['author_commit_dates'], result['committer_commit_dates'])

    df['Perc of Commits'] = df['Occurrences'] / df['Occurrences'].sum() * 100.0

    print(df)

    output_file = input("Enter the output CSV file name: ")
    save_df_to_csv(df, output_file)

if __name__ == "__main__":
    main()



    # print("\nTotal Authors:", result['total_authors'])
    # print("Total Committers:", result['total_committers'])
    # print("Total Forks:", result['total_forks'])
    # print("Total Open Issues:", result['total_open_issues'])
    # print("Project Name:", result['project_name'])

    # # Print sorted authors and committers by occurrence count (high to low)
    # print("\nAuthors (sorted by occurrence count - high to low):")
    # for i, (author, count) in enumerate(result['sorted_authors'], start=1):
    #     print(f"\nAuthor #{i}")
    #     print(f"Name: {author[0]}")
    #     print(f"Email: {author[1]}")
    #     print(f"Project: {author[2]}")
    #     author_key = (author[0], author[1], author[2])
    #     if author_key in result['author_commit_dates']:
    #         first_commit_date = result['author_commit_dates'][author_key]['first_commit'].strftime('%Y-%m-%d')
    #         last_commit_date = result['author_commit_dates'][author_key]['last_commit'].strftime('%Y-%m-%d')
    #         print(f"Start Date: {first_commit_date}")
    #         print(f"End Date: {last_commit_date}")
    #     print(f"Occurrences: {count}")

    # print("\nCommitters (sorted by occurrence count - high to low):")
    # for i, (committer, count) in enumerate(result['sorted_committers'], start=1):
    #     print(f"\nCommitter #{i}")
    #     print(f"Name: {committer[0]}")
    #     print(f"Email: {committer[1]}")
    #     print(f"Project: {committer[2]}")
    #     committer_key = (committer[0], committer[1], committer[2])
    #     if committer_key in result['committer_commit_dates']:
    #         first_commit_date = result['committer_commit_dates'][committer_key]['first_commit'].strftime('%Y-%m-%d')
    #         last_commit_date = result['committer_commit_dates'][committer_key]['last_commit'].strftime('%Y-%m-%d')
    #         print(f"Start Date: {first_commit_date}")
    #         print(f"End Date: {last_commit_date}")
    #     print(f"Occurrences: {count}")

