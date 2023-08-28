import json

import requests
from bs4 import BeautifulSoup


def processJob(row):
    url = f'https://www.metacareers.com/jobs/{row["jobId"]}'
    print(f"Processing {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {
        'jobId': row['jobId'],
        'title': row['title'],
        'locations': row['locations'],
        'teams': row['teams'],
        'subTeams': row['subTeams'],
        "minSalary": None,
        "maxSalary": None,
        "currency": None,
        "duration": None,
    }
    salary_div = soup.find_all("div", {"class": "_97fe _1n-_ _6hy- _94t2"})
    if len(salary_div) > 1:
        salary = salary_div[1]
        minMaxSalary = str(salary).split("<br")[0].split(">")[-1].strip()
        data["currency"] = minMaxSalary[0]
        data["duration"] = minMaxSalary.split("/")[1].split(" ")[0]
        data['minSalary'] = int(minMaxSalary.split(" ")[0].split("/")[0][1:].replace(",", ""))
        data['maxSalary'] = int(minMaxSalary.split(" ")[2].split("/")[0][1:].replace(",", ""))
    print(data)


def main():
    # processJob("588046992908247")
    # return
    url = 'https://www.metacareers.com/graphql'
    data = {
        '__ccg': 'EXCELLENT',
        'lsd': 'AVqlkG49q10',
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CareersJobSearchResultsQuery',
        'variables': '{"search_input":{"q":"","divisions":[],"offices":[],"roles":[],"leadership_levels":[],"saved_jobs":[],"saved_searches":[],"sub_teams":[],"teams":[],"is_leadership":false,"is_remote_only":false,"sort_by_new":false,"page":1,"results_per_page":null}}',
        'server_timestamps': 'true',
        'doc_id': '6638667699485633'
    }
    response = requests.post(url, data=data)
    print(response.text)
    for job in response.json()['data']['job_search'][6:]:
        row = {
            'jobId': job['id'],
            'title': job['title'],
            'locations': ", ".join(job['locations']),
            'teams': ", ".join(job['teams']),
            'subTeams': ", ".join(job['sub_teams']),
        }
        processJob(row)


def getHeaders():
    return {
        'authority': 'www.metacareers.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'origin': 'https://www.metacareers.com',
        'referer': 'https://www.metacareers.com/jobs/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-asbd-id': '198387',
        'x-fb-friendly-name': 'CareersJobSearchResultsQuery',
        'x-fb-lsd': 'AVqlkG49q10',
    }


if __name__ == '__main__':
    main()
