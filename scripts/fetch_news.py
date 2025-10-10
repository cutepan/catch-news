# scripts/fetch_news.py
import requests
import os
import shutil
import json
from datetime import datetime

HTML_URL = "https://news.topurl.cn/?ip=125.95.207.0"
API_URL = "https://news.topurl.cn/api?ip=125.95.207.0"

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    archive_folder = f"archive/{today}"
    os.makedirs(archive_folder, exist_ok=True)

    # 归档旧文件
    for fname in ["page.html", "page.txt"]:
        if os.path.exists(fname):
            shutil.move(fname, f"{archive_folder}/{fname}")

    # 抓取 HTML 页面
    html_resp = requests.get(HTML_URL, timeout=10)
    html_resp.encoding = html_resp.apparent_encoding
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html_resp.text)

    # 抓取 API JSON
    api_resp = requests.get(API_URL, timeout=10)
    api_resp.encoding = "utf-8"
    data = api_resp.json().get("data", {})

    # 生成 TXT 内容
    lines = []

    # 📅 日期信息
    cal = data.get("calendar", {})
    if cal:
        lines.append("📅 日期信息")
        lines.append(f"公历: {cal.get('cYear')}年{cal.get('cMonth')}月{cal.get('cDay')}日 {cal.get('ncWeek')}")
        lines.append(f"农历: {cal.get('yearCn')}{cal.get('monthCn')}{cal.get('dayCn')} ({cal.get('animal')}年)")
        lines.append("")

    # 🌦 天气
    weather = data.get("weather", {}).get("detail", {})
    if weather:
        lines.append("🌦 天气预报")
        lines.append(f"日期: {weather.get('date')}")
        lines.append(f"白天: {weather.get('text_day')}  夜间: {weather.get('text_night')}")
        lines.append(f"气温: {weather.get('low')}℃ ~ {weather.get('high')}℃")
        lines.append(f"湿度: {weather.get('humidity')}%  风速: {weather.get('wind_speed')} m/s")
        lines.append("")

    # 📰 新闻
    news_list = data.get("newsList", [])
    if news_list:
        lines.append("📰 今日新闻")
        for i, news in enumerate(news_list, 1):
            lines.append(f"{i}. [{news.get('category')}] {news.get('title')} (重要度: {news.get('score')})")
            lines.append(f"   链接: {news.get('url')}")
        lines.append("")

    # 📜 历史上的今天
    history = data.get("historyList", [])
    if history:
        lines.append("📜 历史上的今天")
        for h in history:
            lines.append(f"- {h.get('event')}")
        lines.append("")

    # 📖 诗词
    poem = data.get("poem", {})
    if poem:
        lines.append("📖 每日诗词")
        lines.append(f"《{poem.get('title')}》 - {poem.get('author')}")
        for line in poem.get("content", []):
            lines.append(line)
        lines.append("")

    # 💡 成语
    phrase = data.get("phrase", {})
    if phrase:
        lines.append("💡 每日成语")
        lines.append(f"{phrase.get('phrase')} ({phrase.get('pinyin')})")
        lines.append(f"释义: {phrase.get('explain')}")
        lines.append(f"出处: {phrase.get('from')}")
        lines.append("")

    # ✍️ 名言
    sentence = data.get("sentence", {})
    if sentence:
        lines.append("✍️ 每日一句")
        lines.append(f"{sentence.get('sentence')} —— {sentence.get('author')}")
        lines.append("")

    # 写入 TXT
    with open("page.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
