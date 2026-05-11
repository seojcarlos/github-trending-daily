# generate_weekly.py
import os
from datetime import datetime, timedelta, timezone
from collections import Counter
import re

HIST_DIR = "trending_history"
OUTPUT_FILE = "trending_weekly.md"
DAYS = 7


def get_last_n_days_files(n):
    today = datetime.now(timezone.utc)
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
            match = re.match(r"\d+\.\s+\[([^\]]+)\]\(([^)]+)\)\s+⭐\s+([\d,.]+)", line)
            if match:
                stars_raw = match.group(3).replace(",", "").replace(".", "")
                repos.append({
                    "name": match.group(1),
                    "url": match.group(2),
                    "stars": int(stars_raw)
                })
    return repos


def main():
    os.makedirs(HIST_DIR, exist_ok=True)

    files = get_last_n_days_files(DAYS)
    appearances = Counter()
    best_stars = {}
    urls = {}

    for file in files:
        repos = extract_repos_from_file(file)
        for repo in repos:
            name = repo["name"]
            appearances[name] += 1
            urls[name] = repo["url"]
            if name not in best_stars or repo["stars"] > best_stars[name]:
                best_stars[name] = repo["stars"]

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not appearances:
        content = f"# ⭐ Repositorios más populares de la semana - {today}\n\nNo hay datos suficientes para la última semana.\n"
    else:
        lines = [f"# ⭐ Top repositorios de la semana - {today}\n"]
        lines.append(f"Basado en {len(files)} días de datos del trending diario.\n")
        for i, (name, count) in enumerate(appearances.most_common(25), 1):
            url = urls.get(name, f"https://github.com/{name}")
            stars = best_stars.get(name, 0)
            stars_fmt = f"{stars:,}".replace(",", ".")
            lines.append(f"{i}. [{name}]({url}) ⭐ {stars_fmt} — {count} apariciones\n")
        lines.append(f"\n<!-- Última actualización: {datetime.now(timezone.utc).isoformat()} UTC -->")
        content = "\n".join(lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
