import os
from datetime import datetime, timedelta
from collections import Counter
import re

# Configuración
HIST_DIR = "trending_history"
OUTPUT_FILE = "trending_weekly.md"
DAYS = 7

def get_last_n_days_files(n):
    today = datetime.now(datetime.UTC)
    files = []
    if os.path.exists(HIST_DIR):
        for i in range(n):
            day = today - timedelta(days=i)
            fname = os.path.join(HIST_DIR, f"{day.strftime('%Y-%m-%d')}.md")
            if os.path.exists(fname):
                files.append(fname)
    return files

def extract_repos_from_file(filepath):
    repos = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            match = re.match(r"\d+\. \[([^\]]+)\]\([^)]+\)", line)
            if match:
                repos.append(match.group(1))
    return repos

def main():
    files = get_last_n_days_files(DAYS)
    counter = Counter()
    for file in files:
        repos = extract_repos_from_file(file)
        counter.update(repos)
    if not counter:
        content = "# No hay datos suficientes para la última semana."
    else:
        content = ["# ⭐ Repositorios más populares de la semana\n"]
        for i, (repo, count) in enumerate(counter.most_common(), 1):
            content.append(f"{i}. {repo} — {count} apariciones\n")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(content))

if __name__ == "__main__":
    main()
