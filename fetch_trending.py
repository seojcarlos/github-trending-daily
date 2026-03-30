# fetch_trending.py
import requests
from datetime import datetime, timezone
import os
import re

GITHUB_TRENDING_URL = "https://github.com/trending?since=daily"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def parse_number(text):
    """Convierte '1,234' o '1.2k' a entero."""
    text = text.strip().replace(",", "")
    if "k" in text.lower():
        return int(float(text.lower().replace("k", "")) * 1000)
    try:
        return int(text)
    except ValueError:
        return 0


def fetch_trending():
    response = requests.get(GITHUB_TRENDING_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    html = response.text

    repos = []
    # Buscar cada artículo de repo en el HTML
    articles = re.findall(
        r'<article class="Box-row">(.*?)</article>', html, re.DOTALL
    )

    for article in articles[:20]:
        # Nombre del repo (author/name)
        name_match = re.search(
            r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', article
        )
        if not name_match:
            continue

        full_name = name_match.group(1).strip()
        full_name = re.sub(r"\s+", "", full_name)

        # Descripción
        desc_match = re.search(r'<p class="[^"]*">(.*?)</p>', article, re.DOTALL)
        description = ""
        if desc_match:
            description = re.sub(r"<[^>]+>", "", desc_match.group(1)).strip()

        # Estrellas totales
        stars_match = re.search(
            r'href="/[^"]+/stargazers"[^>]*>\s*(?:<[^>]+>\s*)*?([\d,]+)',
            article,
        )
        stars = parse_number(stars_match.group(1)) if stars_match else 0

        # Lenguaje
        lang_match = re.search(
            r'<span itemprop="programmingLanguage">(.*?)</span>', article
        )
        language = lang_match.group(1).strip() if lang_match else ""

        # Estrellas hoy
        today_match = re.search(r'([\d,]+)\s+stars\s+today', article)
        stars_today = parse_number(today_match.group(1)) if today_match else 0

        repos.append({
            "name": full_name,
            "url": f"https://github.com/{full_name}",
            "description": description,
            "stars": stars,
            "language": language,
            "stars_today": stars_today,
        })

    return repos


def main():
    try:
        repos = fetch_trending()
        if not repos:
            print("No se encontraron repos en trending")
            return

        now = datetime.now(timezone.utc)
        today = now.strftime("%Y-%m-%d")

        content = [f"# ⭐ Top {len(repos)} repositorios populares en GitHub - {today}\n"]

        for i, repo in enumerate(repos, 1):
            lang = f" `{repo['language']}`" if repo["language"] else ""
            today_str = f" (+{repo['stars_today']} hoy)" if repo["stars_today"] else ""
            line = (
                f"{i}. [{repo['name']}]({repo['url']}) ⭐ {repo['stars']:,}{today_str}{lang}  \n"
                f"   _{repo['description']}_\n"
            )
            content.append(line)

        content.append(f"\n<!-- Última actualización: {now.isoformat()} UTC -->")

        # Guardar historial
        os.makedirs("trending_history", exist_ok=True)
        with open(f"trending_history/{today}.md", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        # Guardar archivo principal
        with open("trending_daily.md", "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"Guardados {len(repos)} repos trending para {today}")

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        raise


if __name__ == "__main__":
    main()
