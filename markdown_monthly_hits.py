from datetime import datetime, timedelta
from github import Github
from dotenv import load_dotenv
import os

# Set up authentication with a personal access token
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
REPO_NAME='org/repo'# org/repo
GITHUB_URL = 'https://github.company.com/api/v3'
g = Github(base_url=GITHUB_URL, login_or_token=ACCESS_TOKEN)


repo = g.get_repo(REPO_NAME)

# Recursive function to find all markdown files and their view statistics
def find_markdown_files(path):
    files = []
    contents = repo.get_contents(path)
    for item in contents:
        if item.type == "file" and item.name.endswith(".md"):
            view_stats = repo.get_views_traffic(f"{repo.full_name}/blob/main/{item.path}", per="week")
            total_views = sum(view_stats["views"])
            files.append((item.path, total_views))
        elif item.type == "dir":
            sub_files = find_markdown_files(item.path)
            files.extend(sub_files)
    return files

# Call the recursive function to find all markdown files and their view counts
markdown_files = find_markdown_files("")

# Get the number of days in the past month
today = datetime.today()
last_month_end = datetime(today.year, today.month, 1) - timedelta(days=1)
last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
num_days = (last_month_end - last_month_start).days + 1

# Print out the list of markdown files and their average monthly views in CSV format
print("File,Total Views,Average Monthly Views")
for file in markdown_files:
    avg_views = file[1] / num_days * 30
    print(f"{file[0]},{file[1]},{avg_views:.2f}")
