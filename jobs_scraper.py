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

def scrape_data(city,title): #Splits data into variables and formats it.
    try:
        data = scrape_jobsCZ(
    f"https://beta.www.jobs.cz/prace/{city}/?q%5B%5D={title}&locality[radius]=0&page=")
        today = date.today()

        for item in data:
            salary_data = item.find(
                "span", {"class": "Tag Tag--success Tag--small Tag--light"})
            if salary_data != None:
                salary_data = salary_data.string
            else:
                salary_data = "N/A"

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
            title = item.find(
                    "a", {"class": "link-primary SearchResultCard__titleLink"}).string
            company = item.find("li", {"class": "SearchResultCard__footerItem"}).find(
                    "span").string
            link = item.find(
                    "a", {"class": "link-primary SearchResultCard__titleLink"})["href"]
            unique_id = title.lower().replace(" ", "") + "_" + company.lower().replace(" ", "")
            job = Job(
                title = title,
                company = company,
                link = link,
                salary = salary_data,
                published_date = published,
                unique_id = unique_id
            )
            job.save()
    except Exception as e:
        print(f"An error occurred while processing data: {str(e)}")

def clean_data():
    Job.objects.all().delete()
