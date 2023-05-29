from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, timedelta
from support import parse_czech_date
from jobs_dashboard.config import * 
from jobs_dashboard.models import Job

def scrape_jobsCZ(URL): # Scrapes data from all URL subpages
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    page_num = 6
    data_total = []
    try:
        while True: 
            driver.get(URL + str(page_num))
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            data_temp = soup.find_all('article', {"class": "SearchResultCard"})
            data_total = data_total + data_temp
            if len(data_temp) < 1: # Stops loop when no more data is found
                break
            page_num += 1

    except Exception as e:
        print(f"An error occurred while scraping data: {str(e)}")

    finally:
        driver.quit()

    return data_total


data = scrape_jobsCZ(
    "https://beta.www.jobs.cz/prace/praha/?q[0]=sw%20developer&locality[code]=R200000&locality[label]=Praha&locality[coords]=50.08455,14.41778&locality[radius]=0%22&page=")
today = date.today()


def process_data(): #Splits data into variables and formats it.
    try:
        for item in data:
            salary_data = item.find(
                "span", {"class": "Tag Tag--success Tag--small Tag--light"})
            if salary_data != None:
                salary_data = salary_data.string

            published = item.find(
                "div", {"class": "SearchResultCard__status SearchResultCard__status--default"})
            
            if published != None: # Formats published dates for consistency
                published = published.string
                if "včera" in published:
                    published = today - timedelta(days=1)
                    published = published.strftime("%#d.%#m.")    
                elif "Přidáno" in published:
                    published = today.strftime("%#d.%#m.")
                elif "Aktualizováno" in published:
                    published = "Aktualizováno " + today.strftime("%#d.%#m.")  
                else:
                    published = parse_czech_date(published) # Converts czech months into numerical date
            else:
                published = item.find(
                    "div", {"class": "SearchResultCard__status SearchResultCard__status--danger"})
                if published != None:
                    published = published.string
            
            job = Job(
                title = item.find(
                    "a", {"class": "link-primary SearchResultCard__titleLink"}).string,
                company = item.find("li", {"class": "SearchResultCard__footerItem"}).find(
                    "span").string,
                link = item.find(
                    "a", {"class": "link-primary SearchResultCard__titleLink"})["href"],
                salary = salary_data,
                published_date = published
            )
            job.save()
    except Exception as e:
        print(f"An error occurred while processing data: {str(e)}")


process_data()
