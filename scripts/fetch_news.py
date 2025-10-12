# scripts/fetch_news.py
import requests
import os
import shutil
import json
from datetime import datetime

HTML_URL = "https://news.topurl.cn/?ip=125.95.207.0"
API_URL = "https://news.topurl.cn/api?ip=125.95.207.0&count=15"

from datetime import datetime

def get_year_progress():
    today = datetime.now()
    year = today.year
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    days_passed = (today - start).days + 1
    total_days = (end - start).days
    percent = days_passed / total_days * 100
    return percent


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
    
    # 标题行
    cal = data.get("calendar", {})
    date_str = f"{cal.get('cMonth')}月{cal.get('cDay')}日{cal.get('ncWeek')}"
    lunar_str = f"农历{cal.get('monthCn')}{cal.get('dayCn')}"
    lines.append(f"#海旁早报📑{date_str}，{lunar_str}")

    # 口号
    lines.append("🌈看#海旁早报，🌞品味世界事！")

    # 天气
    weather = data.get("weather", {}).get("detail", {})
    if weather:
        city = data.get("weather", {}).get("city", "")
        lines.append(f"明天{city}{weather.get('text_day')}转{weather.get('text_night')}，"
                     f"{weather.get('low')} ~ {weather.get('high')}℃，微风")
    lines.append("")

    # 新闻列表
    news_list = data.get("newsList", [])
    for i, news in enumerate(news_list, 1):
        lines.append(f"{i}. {news.get('title')}。")
    lines.append("")

    # 精神/名言
    sentence = data.get("sentence", {})
    if sentence:
        lines.append(f"【精神】{sentence.get('sentence')}")
    lines.append("")
        
    # 自动计算进度条
    percent = get_year_progress()
    blocks = int(percent // 10)  # 每格代表5%
    bar = "▓" * blocks + "░" * (10 - blocks)
    lines.append("【今年进度条】")
    lines.append(bar)
    lines.append(f"{datetime.now().year}年，您已经使用了{percent:.2f}%")

    # 写入 TXT
    with open("page.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
