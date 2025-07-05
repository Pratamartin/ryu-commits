import os
import requests
import svgwrite
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("USERNAME_GITHUB")

print("Username:", USERNAME)

query = f"""
query {{
  user(login: "{USERNAME}") {{
    contributionsCollection {{
      contributionCalendar {{
        weeks {{
          contributionDays {{
            date
            contributionCount
          }}
        }}
      }}
    }}
  }}
}}
"""

res = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers={"Authorization": f"bearer {TOKEN}"}
)

print("Status:", res.status_code)
print("Response:", res.json())

weeks = res.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
grid = [[day["contributionCount"] for day in week["contributionDays"]] for week in weeks]

CELL_SIZE = 12
PADDING = 10
dwg = svgwrite.Drawing("output/github-ryu-hadouken.svg", profile="tiny",
                       size=(53 * CELL_SIZE + 2 * PADDING, 7 * CELL_SIZE + 2 * PADDING))

dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#0d1117"))

for x in range(len(grid)):
    for y in range(len(grid[x])):
        color = "#39d353" if grid[x][y] > 0 else "#161b22"
        dwg.add(dwg.rect(
            insert=(PADDING + x * CELL_SIZE, PADDING + y * CELL_SIZE),
            size=(CELL_SIZE - 2, CELL_SIZE - 2),
            fill=color
        ))

# Ryu (como imagem externa)
dwg.add(dwg.image(href="assets/ryu_pixel.svg", insert=(PADDING - 12, PADDING + 5 * CELL_SIZE), size=(24, 24)))

for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] > 0:
            dwg.add(dwg.image(href="assets/hadouken_pixel.svg",
                              insert=(PADDING + x * CELL_SIZE, PADDING + y * CELL_SIZE),
                              size=(12, 12)))
dwg.save()


