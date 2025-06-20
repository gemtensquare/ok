import requests
from django.utils import timezone


from . import constants
from Helper.scraping import Scraping
from .helpers import Helper, GemtenPostHelper
from Facebook.facebook_helper import Facebook


def cron_scrape_all_news():
    news_ids = []
    news_ids += Scraping.scrape_all_news()
    # print("&&&&&**", news_ids)

    url = 'http://127.0.0.1:8000/api/news/scrape/'
    res = requests.get(url)
    response = res.json()
    return response


def cron_auto_post_news_to_all_pages():
    # GemtenPostHelper.process_and_publish_news_to_all_pages()
    url = 'http://127.0.0.1:8000/api/post/to/gemten/facebook/'
    res = requests.get(url)
    response = res.json()
    return response

def cron_post_to_facebook_page():
    Helper.post_Gemten_News_page()
    Helper.post_Gemten_Sports_page()
    Helper.post_Gemten_ESports_page()
    Helper.post_Gemten_ShowBiz_page()
    Helper.post_Gemten_Cricket_page()
    Helper.post_Gemten_Football_page()
    Helper.post_Gemten_Terabyte_page()

    Helper.post_Gemten_Scholar_page()
    Helper.post_Gemten_Citizen_page()
    Helper.post_Gemten_Quantum_page()
    Helper.post_Gemten_PetVerse_page()
    Helper.post_Gemten_TradeBeat_page()
    pass







def log_cron_run(job_name: str):
    timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
    with open(constants.CRON_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} — ✨ Yay! [{job_name}] just finished its run! ✨\n\n")
    print(f"{timestamp} — 🌈 [{job_name}] is sparkling now! 🌈")


def my_1_minute_job():
    timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
    fb = Facebook(page_id=constants.GEMTEN_NEWS_PAGE_ID, page_access_token=constants.GEMTEN_NEWS_PAGE_ACCESS_TOKEN)
    # fb.post_text_to_page(message=f"New post at {timestamp}")
    log_cron_run('1-Minute Job')
    # Add your 1-minute interval task logic here


def cron_scrape_all_bdcrictime_news():
    print('\n\n', '@@@'*30)
    print("*** Scraping all bdcrictime news...")
    Scraping.scrape_all_bdcrictime_news()


def cron_scrape_all_jugantor_news():
    Scraping.scrape_all_jugantor_news()

def cron_scrape_all_bd_pratidin_news():
    Scraping.scrape_all_bd_pratidin_news()

def cron_scrape_all_bbc_bangla_news():
    Scraping.scrape_all_bbc_bangla_news()

def cron_scrape_all_daily_star_news():
    Scraping.scrape_all_daily_star_news()


if __name__ == '__main__':
    print("Starting scheduled cron jobs...\n")
    my_1_minute_job()
    print("\nAll scheduled cron jobs completed.")


