# scripts/fetch_news.py
import requests
import os
import shutil
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://news.topurl.cn/?ip=125.95.207.0"

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    archive_folder = f"archive/{today}"
    os.makedirs(archive_folder, exist_ok=True)

    # 如果根目录已有旧文件，先归档
    for fname in ["page.html", "page.txt"]:
        if os.path.exists(fname):
            shutil.move(fname, f"{archive_folder}/{fname}")

    # 抓取网页
    resp = requests.get(URL, timeout=10)
    resp.encoding = resp.apparent_encoding
    html_content = resp.text

    # 保存当天最新 HTML 到根目录
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # 提取精简文本
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    with open("page.txt", "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    main()
