import requests
import os
from datetime import datetime
from urllib.parse import quote


def archive_url(url):
    api_url = "https://web.archive.org/save/"
    encoded_url = quote(url, safe='')
    response = requests.get(api_url + encoded_url)

    if response.status_code == 200:
        # 응답에서 아카이빙된 URL 추출
        archived_url = response.url
        print(f"아카이빙 성공: {url.strip()}")
        print(f"아카이빙된 URL: {archived_url}")

        # 아카이빙된 URL을 날짜와 시간을 포함하여 파일에 저장
        save_to_file(url.strip(), archived_url)

        # urls.txt에서 아카이빙된 URL 삭제
        remove_url_from_file(url.strip())
    else:
        print(f"아카이빙 실패: {url.strip()}")


def save_to_file(original_url, archived_url):
    now = datetime.now()
    file_name = now.strftime("%m%d_%H%M%S") + ".txt"

    with open(file_name, "a") as file:
        file.write(f"원본 URL: {original_url}\n")
        file.write(f"아카이빙된 URL: {archived_url}\n\n")


def remove_url_from_file(url):
    file_path = "urls.txt"
    temp_file_path = "urls_temp.txt"

    with open(file_path, "r") as file, open(temp_file_path, "w") as temp_file:
        urls = file.readlines()
        for line in urls:
            if line.strip() != url:
                temp_file.write(line)

    os.remove(file_path)
    os.rename(temp_file_path, file_path)


file_path = "urls.txt"

if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
    print("urls.txt에 URL을 입력해 주세요")
    exit()

# 파일에서 URL 정보 읽어오기
with open(file_path, "r") as file:
    urls = file.readlines()

# 각 URL을 아카이빙하고 파일에 저장
for url in urls:
    archive_url(url.strip())

print("아카이빙이 완료되었습니다.")
