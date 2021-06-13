import requests
from bs4 import BeautifulSoup
import pandas


def get_page_content(url):
    response = requests.get(url)
    response_code = response.status_code
    return response, response_code


def web_scraping(response, response_code):
    soup = BeautifulSoup(response.content, 'lxml')
    seven_day_data = soup.find_all(id="seven-day-forecast-container")
    # forecast_data = seven_day_data[0].find_all(class_="tombstone-container")
    # forecast_data = soup.find_all(class_="tombstone-container")
    if seven_day_data != []:
        period_tags = seven_day_data[0].select(".tombstone-container .period-name")
        periods = [pt.get_text() for pt in period_tags]
        short_desc_tags = seven_day_data[0].select(".tombstone-container .short-desc")
        short_desc = [sd.get_text() for sd in short_desc_tags]
        temp_tags = seven_day_data[0].select(".tombstone-container .temp")
        temps = [t.get_text() for t in temp_tags]
        desc_tags = seven_day_data[0].select(".tombstone-container img")
        desc = [d['title'] for d in desc_tags]
    else:
        print('We are very sorry !!! This page has been discarded ')

    return periods, short_desc, temps, desc


def print_data(periods, short_desc, temps, desc):
    weather = pandas.DataFrame({
        "periods": periods,
        "short_decs": short_desc,
        "temps": temps,
        "decs": desc
    })

    print(weather)


if __name__ == '__main__':
    url = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.YLxrGfkzbIX'
    page, status = get_page_content(url)
    if status == 200:
        periods, short_desc, temps, desc = web_scraping(page, status)
        print_data(periods, short_desc, temps, desc)
    else:
        print('We are very sorry !!! This page has been discarded ')



