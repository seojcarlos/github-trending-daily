# generate_monthly.py
import os
from datetime import datetime, timezone
from collections import Counter
import re

HIST_DIR = "trending_history"
OUTPUT_FILE = "trending_monthly.md"


def get_current_month_files():
    today = datetime.now(timezone.utc)
    prefix = today.strftime("%Y-%m-")
    files = []
    if os.path.exists(HIST_DIR):
        for fname in sorted(os.listdir(HIST_DIR)):
            if fname.startswith(prefix) and fname.endswith(".md"):
                files.append(os.path.join(HIST_DIR, fname))
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

    files = get_current_month_files()
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

    today = datetime.now(timezone.utc)
    month_label = today.strftime("%B %Y")

    if not appearances:
        content = f"# ⭐ Repositorios más populares del mes - {month_label}\n\nNo hay datos suficientes para este mes.\n"
    else:
        lines = [f"# ⭐ Top repositorios del mes - {month_label}\n"]
        lines.append(f"Basado en {len(files)} días de datos del trending diario.\n")
        for i, (name, count) in enumerate(appearances.most_common(30), 1):
            url = urls.get(name, f"https://github.com/{name}")
            stars = best_stars.get(name, 0)
            stars_fmt = f"{stars:,}".replace(",", ".")
            lines.append(f"{i}. [{name}]({url}) ⭐ {stars_fmt} — {count} apariciones\n")
        lines.append(f"\n<!-- Última actualización: {today.isoformat()} UTC -->")
        content = "\n".join(lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
