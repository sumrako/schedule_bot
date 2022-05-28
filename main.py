import datetime

import requests
from bs4 import BeautifulSoup


def get_schedule():
    headers = {
        "user agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143"
                      " YaBrowser/22.5.0.1792 Yowser/2.5 Safari/537.36"
    }
    date = datetime.datetime.today()
    params = {
        "groupId": 531873790,
        "selectedWeek": int(date.strftime("%V")) - 6,
        "selectedWeekday": date.weekday() + 1
    }
    print(params)
    url = "https://ssau.ru/rasp"
    r = requests.get(url=url, headers=headers, params=params)

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.find_all("div", attrs={"class": ["lesson-border-type-2", "lesson-border-type-3"]})
    times = soup.find_all("div", class_="schedule__time")

    time_begin = [time.find("div", class_="schedule__time-item").text.strip()
                  for time in times
                  if time.find_next_sibling("div").find("div")]
    titles = []
    teachers = []
    places = []

    for item in items:
        if item.find("div", class_="schedule__groups").text.strip() != 'Подгруппы: 1':
            print(item)
            class_num = 3
            sub_item = item.find("div", class_=f"schedule__lesson lesson-border lesson-border-type-{class_num}")
            if sub_item is None:
                class_num = 2
                sub_item = item.find("div", class_=f"schedule__lesson lesson-border lesson-border-type-{class_num}")

            titles.append(item.find("div", class_="schedule__discipline").text.strip())
            teachers.append(item.find("div", class_="schedule__teacher").text.strip())

            place = item.find("div", class_="schedule__place").text.strip()
            places.append("онлайн" if "ON-LINE" in place else place)

    print(titles)
    total_schedule = [{"time": time_begin[i],
                       "title": titles[i],
                       "teacher": teachers[i],
                       "place": places[i]} for i in range(0, len(titles)) if titles[i] != '']
    return total_schedule


def main():
    get_schedule()


if __name__ == '__main__':
    main()
