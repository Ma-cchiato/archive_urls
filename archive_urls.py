import requests
import os
import time
from datetime import datetime
from urllib.parse import quote


def archive_url(url):
    api_url = "https://web.archive.org/save/"
    encoded_url = quote(url, safe='')
    response = requests.get(api_url + encoded_url)

    if response.status_code == 200:
        archived_url = response.url
        print(f"아카이빙 성공: {url.strip()}")
        print(f"아카이빙된 URL: {archived_url}")
        save_to_file(url.strip(), archived_url, "성공")
        remove_url_from_file(url.strip())
        return True  # 아카이빙 성공 시 True 반환
    else:
        print(f"아카이빙 실패: {url.strip()}")
        save_to_file(url.strip(), "", "실패")
        save_failed_url(url.strip())
        return False  # 아카이빙 실패 시 False 반환


def save_to_file(url, archived_url, status):
    file_path = "archived_urls.txt"

    with open(file_path, "a") as file:
        file.write(f"URL: {url}\n")
        if status == "성공":
            file.write(f"아카이빙된 URL: {archived_url}\n")
        file.write(f"아카이빙 결과: {status}\n\n")


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


def save_failed_url(url):
    now = datetime.now()
    file_name = now.strftime("fail_urls_%m%d_%H%M%S.txt")

    with open(file_name, "a") as file:
        file.write(f"아카이빙 실패 URL: {url}\n")


file_path = "urls.txt"

if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
    print("urls.txt 파일이 없거나 비어 있습니다. 파일을 생성하고 URL을 입력해 주세요.")
    with open(file_path, "w") as file:
        pass

if os.path.isfile(file_path) and os.stat(file_path).st_size != 0:
    with open(file_path, "r") as file:
        urls = file.readlines()

    num_urls = len(urls)
    print(f"아카이브 대상 URL: {num_urls}개")
    if num_urls > 0:
        print("아카이빙이 시작되었습니다.")

        success_count = 0
        failure_count = 0

        for index, url in enumerate(urls, 1):
            url = url.strip()
            if not url.startswith("http://") and not url.startswith("https://"):
                print(f"URL 형식이 올바르지 않습니다: {url}")
                save_to_file(url, "", "실패")
                save_failed_url(url)
                failure_count += 1
                continue

            print(f"아카이빙 진행 중: ({index}/{num_urls})")
            if archive_url(url):
                success_count += 1
            else:
                failure_count += 1

        print("아카이빙이 완료되었습니다.")
        print(f"- 성공: {success_count}")
        print(f"- 실패: {failure_count}")
        time.sleep(20)
    else:
        print("urls.txt에 URL을 입력해 주세요.")
else:
    print("urls.txt에 URL을 입력해 주세요.")
    time.sleep(5)
