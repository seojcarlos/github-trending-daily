# 🧠 auto-contributions — Automatización diaria de actividad en GitHub

![GitHub Stars](https://img.shields.io/github/stars/seojcarlos/auto-contributions?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/seojcarlos/auto-contributions)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/seojcarlos/auto-contributions/daily_trending.yml?label=Actualización%20Diaria)
![GitHub Repo Size](https://img.shields.io/github/repo-size/seojcarlos/auto-contributions)



---

## 🔥 ¿Qué hace este proyecto?

`auto-contributions` :

- ✅ Publica los **20 repositorios más populares de GitHub**
- 🔁 Actualiza dependencias reales vía **Dependabot**
- 📈 (Próximamente) Genera **informes técnicos automáticos**

Ideal para:
- Desarrolladores que quieren mejorar su huella digital
- Reclutadores que valoran perfiles activos
- Proyectos de portfolio que requieren actividad constante

---

## 🧠 Funcionalidades

| Tarea                              | Frecuencia | Tecnología             |
|-----------------------------------|------------|------------------------|
| Trending repos (Top 20 diarios)   | Diario     | Python + GitHub API    |
| Historial diario de trending      | Diario     | Python + Markdown      |
| Mejores de la semana/mes          | Semanal/Mensual | Python + Markdown  |
| Auto-merge de dependencias        | Diario     | GitHub Actions + Bot   |
| Informes técnicos (soon)          | Semanal    | GitHub API + Markdown  |

---

## 📅 Histórico y rankings

- El historial diario se guarda en la carpeta [`trending_history/`](./trending_history/) con un archivo por día (`YYYY-MM-DD.md`).
- Los repositorios más populares de la semana se generan en [`trending_weekly.md`](./trending_weekly.md) ejecutando `python generate_weekly.py`.
- Los repositorios más populares del mes se generan en [`trending_monthly.md`](./trending_monthly.md) ejecutando `python generate_monthly.py`.
- El archivo [`trending_daily.md`](./trending_daily.md) muestra el top 20 del día actual.

---

## ⚙️ Automatización técnica

Este repositorio utiliza:
- `GitHub Actions` con cron (`on: schedule`)
- `Python` para extracción de datos desde APIs públicas y generación de históricos/rankings
- Scripts: `fetch_trending.py` (historial diario), `generate_weekly.py` (ranking semanal), `generate_monthly.py` (ranking mensual)
- `Dependabot` con merge automático habilitado
- Commits automáticos con `bot@users.noreply.github.com`

---

## ⚙️ Automatización técnica

Este repositorio utiliza:
- `GitHub Actions` con cron (`on: schedule`)
- `Python` para extracción de datos desde APIs públicas
- `Dependabot` con merge automático habilitado
- Commits automáticos con `bot@users.noreply.github.com`

---

## 🌍 Visibilidad y SEO

El contenido de este repositorio está optimizado para aparecer en búsquedas relacionadas con:

- `GitHub Trending Automation`
- `Mejorar perfil GitHub`
- `Commits automáticos GitHub`
- `Dependabot + GitHub Actions`
- `Desarrollador activo GitHub`

---

## 🙌 Autor

Este proyecto ha sido desarrollado y automatizado por:

**Juan Carlos Díaz**  
[CEO en Convertiam.com](https://www.convertiam.com)  
📍 Barcelona, España  
🔗 [GitHub @seojcarlos](https://github.com/seojcarlos)  
🔗 [LinkedIn](https://www.linkedin.com/in/juan-carlos-diaz-seo)

---

## 💡 ¿Quieres hacer lo mismo?

Forkea este repositorio o [contáctame](mailto:juan@convertiam.com) si quieres replicar esta automatización para tu perfil profesional o empresa.
