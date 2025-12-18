#Груша Вариант 1
import requests
from bs4 import BeautifulSoup
import json


url = "https://news.ycombinator.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

news_items = []

titles = soup.select(".athing")
subtexts = soup.select(".subtext")

for i, (title, sub) in enumerate(zip(titles, subtexts), start=1):
    title_text = title.select_one(".titleline a").get_text(strip=True)
    link = title.select_one(".titleline a")["href"]

    comments_tag = sub.find_all("a")[-1]
    comments_text = comments_tag.get_text()
    comments = 0
    if "comment" in comments_text:
        try:
            comments = int(comments_text.split()[0])
        except:
            comments = 0

    news_items.append({
        "title": title_text,
        "comments": comments,
        "link": link
    })

for idx, item in enumerate(news_items[:30], start=1):
    print(f"{idx}. Title: {item['title']}; Comments: {item['comments']};")

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(news_items, f, ensure_ascii=False, indent=4)

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hacker News Parsed Data</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #9bc5c3, #616161);
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        table {{
            width: 90%;
            margin: auto;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}
        th {{
            background: #333;
            color: #fff;
            padding: 12px;
            font-size: 18px;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        tr:hover {{
            background: #f1f1f1;
        }}
        .source {{
            text-align: center;
            margin-top: 20px;
        }}
        .source a {{
            color: #fff;
            font-size: 18px;
            text-decoration: none;
        }}
    </style>
</head>
<body>

<h1>Hacker News — Parsed News</h1>

<table>
    <tr>
        <th>#</th>
        <th>Title</th>
        <th>Comments</th>
    </tr>
"""

for i, item in enumerate(news_items[:30], start=1):
    html_content += f"""
    <tr>
        <td>{i}</td>
        <td><a href="{item['link']}" target="_blank">{item['title']}</a></td>
        <td>{item['comments']}</td>
    </tr>
"""

html_content += """
</table>

<div class="source">
    <p><a href="https://news.ycombinator.com/" target="_blank">Оригинальный источник данных — Hacker News</a></p>
</div>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Готово! Созданы файлы data.json и index.html")