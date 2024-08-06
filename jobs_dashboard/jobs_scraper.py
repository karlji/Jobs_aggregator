from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date, timedelta
from .support import parse_czech_date
from jobs_dashboard.models import Job
from selenium.webdriver.chrome.service import Service
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chrome options for Selenium WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

def save_page_source(page_source, page_num):
    """
    Saves the page source to an HTML file.
    """
    try:
        with open(f"page_{page_num}.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        logger.info(f"Saved page {page_num} as page_{page_num}.html")
    except Exception as e:
        logger.error(f"Failed to save page {page_num}: {e}")

def scrape_jobsCZ(URL):
    """
    Scrapes data from all URL subpages.
    """
    data_total = []
    page_num = 1
    
    # Use context manager for WebDriver to ensure it closes properly
    with webdriver.Chrome(options=chrome_options) as driver:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": headers["User-Agent"]})
        
        try:
            while True:
                driver.get(URL + str(page_num))
                page = driver.page_source
                #save_page_source(page, page_num)
                soup = BeautifulSoup(page, "html.parser")
                data_temp = soup.find_all('article', {"class": "SearchResultCard"})
                
                if soup.find_all('div', {"class": "Alert Alert--informative Alert--center mt-800 mb-600"}):
                    break
                
                data_total.extend(data_temp)
                page_num += 1
                
        except Exception as e:
            logger.error(f"An error occurred while scraping data: {e}")
    
    return data_total

def scrape_data(city, title, user):
    """
    Splits data into variables and formats it.
    """
    logger.info("Scrape called")
    clean_data(user)
    
    try:
        url = f"https://www.jobs.cz/prace/{city}/?q%5B%5D={title}&locality[radius]=0&page="
        data = scrape_jobsCZ(url)
        today = date.today()

        for item in data:
            # Extract and clean salary data
            salary_data = item.find("span", {"class": "Tag Tag--success Tag--small Tag--subtle"})
            salary_data = salary_data.string if salary_data else "N/A"
            
            # Extract and format published date
            published = item.find("div", {"class": "SearchResultCard__status SearchResultCard__status--default"})
            if published:
                published = published.string
                if "včera" in published:
                    published = (today - timedelta(days=1)).strftime("%d.%m.")
                elif "Přidáno" in published:
                    published = today.strftime("%d.%m.")
                elif "Aktualizováno" in published:
                    published = "Aktualizováno " + today.strftime("%d.%m.")
                else:
                    published = parse_czech_date(published)
            else:
                published = item.find("div", {"class": "SearchResultCard__status SearchResultCard__status--danger"})
                published = published.string if published else "Unknown"

            # Extract title, company, and link
            title = item.find("a", {"class": "link-primary SearchResultCard__titleLink"}).string
            company = item.find("li", {"class": "SearchResultCard__footerItem"}).find("span").string
            link = item.find("a", {"class": "link-primary SearchResultCard__titleLink"})["href"]
            unique_id = f"{title.lower().replace(' ', '')}_{company.lower().replace(' ', '')}"

            # Save job to the database
            job = Job(
                title=title,
                company=company,
                link=link,
                salary=salary_data,
                published_date=published,
                unique_id=unique_id,
                user=user
            )
            job.save()
    
    except Exception as e:
        logger.error(f"An error occurred while processing data: {e}")

def clean_data(user):
    """
    Cleans up existing job data for the user.
    """
    try:
        Job.objects.filter(user=user).delete()
    except Exception as e:
        logger.info("No data to delete or an error occurred while deleting data.")
        logger.error(e)
