# fetch_trending.py
import requests
from datetime import datetime

url = "https://ghapi.huchen.dev/repositories?since=daily"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    today = datetime.utcnow().strftime("%Y-%m-%d")
    content = [f"# ⭐ Top 20 repositorios populares en GitHub - {today}\n"]

    for i, repo in enumerate(data[:20], 1):
        line = f"{i}. [{repo['author']}/{repo['name']}]({repo['url']}) ⭐ {repo['stars']}  \n   _{repo['description']}_\n"
        content.append(line)

    with open("trending_repos.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))

except Exception as e:
    print(f"❌ Error al obtener datos: {e}")
