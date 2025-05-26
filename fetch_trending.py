# fetch_trending.py
import requests
from datetime import datetime
import os
url = "https://github-trending-api.de.a9sapp.eu/repositories?since=daily"

# Leer token de entorno si existe
token = os.environ.get("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {token}"} if token else {}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    today = datetime.utcnow().strftime("%Y-%m-%d")
    content = [f"# ⭐ Top 20 repositorios populares en GitHub - {today}\n"]

    for i, repo in enumerate(data[:20], 1):
        line = f"{i}. [{repo['author']}/{repo['name']}]({repo['url']}) ⭐ {repo['stars']}  \n   _{repo['description']}_\n"
        content.append(line)

    # 👉 Forzar un cambio mínimo con una línea oculta
    content.append(f"\n<!-- Última actualización: {datetime.utcnow().isoformat()} UTC -->")

    # Crear carpeta de historial si no existe
    os.makedirs("trending_history", exist_ok=True)
    # Guardar archivo diario en trending_history/YYYY-MM-DD.md
    with open(f"trending_history/{today}.md", "w", encoding="utf-8") as f_hist:
        f_hist.write("\n".join(content))
    # Guardar archivo principal
    with open("trending_daily.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))

except Exception as e:
    print(f"❌ Error al obtener datos: {e}")
