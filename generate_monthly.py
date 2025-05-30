import os
from datetime import datetime, timezone
from collections import Counter
import re

# Configuración
HIST_DIR = "trending_history"
OUTPUT_FILE = "trending_monthly.md"

def get_current_month_files():
    today = datetime.now(timezone.utc)
    prefix = today.strftime("%Y-%m-")
    files = []
    if os.path.exists(HIST_DIR):
        for fname in os.listdir(HIST_DIR):
            if fname.startswith(prefix) and fname.endswith(".md"):
                files.append(os.path.join(HIST_DIR, fname))
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
    # Crear carpeta de historial si no existe
    os.makedirs(HIST_DIR, exist_ok=True)
    
    files = get_current_month_files()
    counter = Counter()
    for file in files:
        repos = extract_repos_from_file(file)
        counter.update(repos)
    
    if not counter:
        content = "# No hay datos suficientes para este mes."
    else:
        content = ["# ⭐ Repositorios más populares del mes\n"]
        for i, (repo, count) in enumerate(counter.most_common(), 1):
            content.append(f"{i}. {repo} — {count} apariciones\n")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(content))

if __name__ == "__main__":
    main()
