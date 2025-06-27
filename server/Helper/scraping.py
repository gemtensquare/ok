from bs4 import BeautifulSoup
import requests, os, random, time
from django.utils import timezone
from django.core.cache import cache
from django.core.files.base import ContentFile


from .helpers import Helper
from News.models import News
from . import constants

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

class Scraping:
    def test():
        print("test")
        pass

    
    def save_news(title, intro, category, news_url, image_url, source="", type="bn"):
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            print('*** skipping *** for image')
            return None
        
        print('&&& saving news &&&')

        filename = Helper.get_a_unique_image_name()
        news_obj, created = News.objects.get_or_create(
            title=title, intro=intro, category=category, type=type,
            url=news_url, image_url=image_url, source=source,
        )
        news_obj.image.save(filename, ContentFile(image_response.content), save=True)
        
        return news_obj



    def scrape_khela(topic, category=None):
        added_news_ids = []
        url = 'https://khela.com/' + topic
        res = requests.get(url=url, headers=HEADERS, timeout=30)

        print()
        print('***'*30)
        print(url, res.status_code)
        if res.status_code != 200: 
            print('*** skipping for status code ***')
            return []

        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select(".items-stretch")
        for card in cards:
            link_tag = card.select_one("a")
            img_tag = card.select_one("img")
            title_tag = card.select_one("h3")
            intro_tag = card.select_one("h3")

            news_url = link_tag['href'] if link_tag else None
            title = title_tag.text.strip() if title_tag else None
            intro = intro_tag.text.strip() if intro_tag else None
            image_url = img_tag['src']

            if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                print('*** skipping *** for image')
                continue
                
            print('&&& saving news &&&')
            
            filename = Helper.get_a_unique_image_name()

            news_obj = News.objects.create(
                title=title, category=category, type="bn", intro=intro,
                url=news_url, image_url=image_url, source="khela.com", 
            )
            news_obj.image.save(filename, ContentFile(image_response.content), save=True)
            added_news_ids.append(news_obj.id)
        return added_news_ids


    def scrape_jugantor(topic, category=None):
        response = []
        url = 'https://www.jugantor.com/' + topic
        res = requests.get(url=url, headers=HEADERS, timeout=30)

        print()
        print('***'*30)
        print(url, res.status_code)
        if res.status_code != 200: 
            print('*** skipping for jugantor status code ***')
            return []

        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select(".media.positionRelative.marginB5")
        for card in cards:
            title_tag = card.select_one("h4")
            intro_tag = card.select_one("p")
            link_tag = card.select_one("a.linkOverlay")
            img_tag = card.select_one("img")

            title = title_tag.text.strip() if title_tag else None
            intro = intro_tag.text.strip() if intro_tag else None
            news_url = link_tag['href'] if link_tag else None
            image_url =  Helper.process_jugantor_image_url(img_tag['data-src'])

            if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                print('*** skipping *** for image')
                continue

            print('&&& saving news &&&')
            
            filename = Helper.get_a_unique_image_name()

            news_obj, created = News.objects.get_or_create(
                title=title, category=category, type="bn", intro=intro,
                url=news_url, image_url=image_url, source="jugantor.com", 
            )
            news_obj.image.save(filename, ContentFile(image_response.content), save=True)
            response.append(news_obj.id)
        return response
    
    
    def scrape_bd_pratidin(topic, category=None):
        response = []
        url = 'https://www.bd-pratidin.com/' + topic
        res = requests.get(url=url, headers=HEADERS, timeout=30)

        print()
        print('***'*30)
        print(url, res.status_code)
        if res.status_code != 200: 
            print('*** skipping for status code ***')
            return []

        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select(".col-6.col-lg-4.col-xl-3.mb-3") + soup.select(".col-6.my-3")
        for card in cards:
            title_tag = card.select_one("h5")
            link_tag = card.select_one("a.stretched-link")
            img_tag = card.select_one("img")

            title = title_tag.text.strip() if title_tag else None
            news_url = link_tag['href'] if link_tag else None
            image_url =  Helper.process_bd_protidin_image_url(img_tag['src'])

            if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                print('*** skipping *** for image')
                continue

            print('&&& saving news &&&')
            
            filename = Helper.get_a_unique_image_name()

            news_obj = News.objects.create(
                title=title, category=category, type="bn",
                url=news_url, image_url=image_url, source="bd-pratidin.com", 
            )
            news_obj.image.save(filename, ContentFile(image_response.content), save=True)
            response.append(news_obj.id)
        return response
    
    
    def scrape_bbc_bangla(topic, category=None):
        response = []
        url = 'https://www.bbc.com/bengali/topics/' + topic
        res = requests.get(url=url, headers=HEADERS, timeout=30)
                
        print()
        print('***'*30)
        print(url, res.status_code)
        if res.status_code != 200: 
            print('*** skipping for status code ***')
            return []

        soup = BeautifulSoup(res.text, 'html.parser')
        all_news = soup.select('.bbc-t44f9r')

        for news in all_news:
            soup = BeautifulSoup(str(news), 'html.parser')
            ref = soup.find('a')
            img = soup.find('img')

            title = ref.get_text()
            news_url = ref['href']
            image_url = Helper.process_bbc_news_image_url(img['src'])

            if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                print('*** skipping *** for image')
                continue

            print('&&& saving news &&&')
            
            filename = Helper.get_a_unique_image_name()

            news_obj = News.objects.create(
                title=title, category=category, type="bn",
                url=news_url, image_url=image_url, source="bbc.com", 
            )
            news_obj.image.save(filename, ContentFile(image_response.content), save=True)
            response.append(news_obj.id)
        return response

    def scrape_shikshabarta_news(topic, category=None):
        base_url = 'https://shikshabarta.com/category/'

        url = base_url + topic
        response = requests.get(url, headers=HEADERS, timeout=30)
        print()
        print('***'*30)
        print(url, response.status_code)

        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')

        def process_image_url(url):
            index = url.find('?resize=')
            return url[:index]

        news_ids = []
        cards = soup.select("article.item-list")
        for card in cards:
            # Title and news URL
            title_tag = card.select_one("h2.post-box-title a")
            title = title_tag.text.strip() if title_tag else ""
            news_url = title_tag['href'] if title_tag else ""

            # Image URL
            image_tag = card.select_one("div.post-thumbnail img")
            image_url = image_tag['src'] if image_tag else ""
            image_url = process_image_url(image_url)

            # Summary
            summary_tag = card.select_one("div.entry p")
            summary = summary_tag.text.strip() if summary_tag else ""

            if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            news_obj = Scraping.save_news(title, summary, category, news_url, image_url, source="shikshabarta.com")
            
            if news_obj:
                news_ids.append(news_obj.id)
        return news_ids

    def scrape_ew_en_news(topic, category=None):
        base_url = 'https://ew.com/'
        url = base_url + topic + '/'

        print()
        print('***' * 30)
        print("Main Page:", url)

        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print("Failed to fetch main page.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select("a.mntl-card.card.card--no-image")

        def get_main_image_from_article(article_url):
            try:
                response = requests.get(article_url, headers=HEADERS, timeout=30)
                if response.status_code != 200:
                    return ""
                soup = BeautifulSoup(response.text, 'html.parser')
                image_tag = soup.select_one("img.primary-image__image")
                if image_tag:
                    return image_tag.get("src", "")
            except Exception as e:
                print(f"Failed to fetch article {article_url}:", e)
            return None
        
        news_ids = []
        for card in cards:
            # Title and URL
            title_tag = card.select_one(".card__title-text")
            title = title_tag.text.strip() if title_tag else ""
            news_url = card.get("href", "")

            if not title or not news_url or News.objects.filter(title=title, url=news_url):
                # print('*** skipping ***')
                continue

            # Visit the news URL and get the main image from the article page
            image_url = get_main_image_from_article(news_url)
            if not image_url:
                print('*** skipping for image ***')
                continue


            news_obj = Scraping.save_news(title, title, category, news_url, image_url, source="ew.com", type="en")
            if news_obj:
                news_ids.append(news_obj.id)

        return news_ids

    def scrape_daily_star(topic, category=None):
        response = []
        base_url = 'https://bangla.thedailystar.net/'
        url = base_url + topic
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)

            print()
            print('***'*30)
            print(url, res.status_code)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                cards = soup.select('.card.position-relative.horizontal')
                for card in cards:
                    try:
                        source_tag = card.select_one('source')
                        image_url = Helper.process_dayli_start_news_image_url(source_tag['data-srcset']) if source_tag and source_tag.has_attr('data-srcset') else ''
                        
                        content = card.select_one('.card-content')
                        if not content:
                            continue

                        title_tag = content.select_one('h3.title a')
                        title = title_tag.text.strip() if title_tag else ''
                        news_url = base_url + title_tag['href'] if title_tag else ''

                        intro_tag = content.select_one('p.intro')
                        intro = intro_tag.text.strip() if intro_tag else ''

                        if not image_url or not title or not news_url or News.objects.filter(title=title, url=news_url):
                            # # print('*** skipping ***')
                            continue

                        news_obj = Scraping.save_news(title, intro, category, news_url, image_url, source="bangla.thedailystar.net")
                        response.append(news_obj.id)
                        
                    except Exception as inner_e:
                        print(f"Error parsing a card: {inner_e}")
            else:
                print(f"Request failed with status code {res.status_code}")
        except Exception as e:
            print(f"The Daily Star error: {e}")
        return response
    
    
    def scrape_dainikshiksha_news(category_id, category=None):
        url = f"https://www.dainikshiksha.com/data/bn/category/{category_id}/paginate-1.json"
        response = requests.get(url)

        def process_image_url(url):
            url = url.replace('thumb.webp', 'medium.webp')
            return url
        
        print()
        print('***'*30)
        print(url, response.status_code)

        news_ids = []
        if response.status_code == 200:
            data = response.json()
            latest_news = data.get('latestNews', [])
            for news in latest_news:
                title = news.get('title', '')
                news_url = news.get('url', '')
                image_url = process_image_url(news.get('thumbnail', ''))

                if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                    # # print('*** skipping ***')
                    continue
                
                news_obj = Scraping.save_news(title, title, category, news_url, image_url, source="dainikshiksha.com")
                if news_obj:
                    news_ids.append(news_obj.id)
        return news_ids
    

    def scrape_daily_star_en(topic, category=None):
        news_ids = []
        base_url = 'https://www.thedailystar.net/'
        url = base_url + topic
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            
            print()
            print('***'*30)
            print(url, res.status_code)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                for card in soup.select('.card.position-relative.horizontal'):
                    try:
                        image_url = Helper.process_dayli_start_news_image_url(card.select_one('source')['data-srcset'])
                        
                        card = card.select_one('.card-content')

                        title = card.select_one('a').text.strip()
                        news_url = base_url + card.select_one('a')['href']
                        if not title or not news_url or not image_url or News.objects.filter(title=title, url=news_url):
                            # # print('*** skipping ***')
                            continue

                        intro = card.select_one('.intro').text.strip() if card.select_one('.intro') else ''
                        image_url = image_url.replace(' 1x', '')

                        news_obj = Scraping.save_news(title, intro, category, news_url, image_url, source="thedailystar.net", type="en")
                        if news_obj:
                            news_ids.append(news_obj.id)

                    except Exception as inner_e:
                        print(f"Error parsing a card: {inner_e}")
            else:
                print(f"Request failed with status code {res.status_code}")
        except Exception as e:
            print(f"The Daily Star error: {e}")
        return news_ids
    


    def scrape_jagonews24(topic, category=None):
        response = []
        base_url = 'https://www.jagonews24.com/'
        url = base_url + topic
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                cards = soup.select(".single-block.cat-block")
                for card in cards:
                    try:
                        link_tag = card.select_one("a")
                        img_tag = card.select_one("img")
                        title_tag = card.select_one("h3 a")

                        # Extracting data
                        news_url = link_tag['href'] if link_tag else None
                        title = title_tag.text.strip() if title_tag else None

                        # Use data-src for actual image; fallback to src
                        raw_image_url = img_tag.get('data-src') or img_tag.get('src')
                        image_url = Helper.process_jagonews24_news_image_url(raw_image_url)

                        if not image_url or not title or not news_url or News.objects.filter(title=title, url=news_url):
                            # # print('*** skipping ***')
                            continue

                        news_obj = Scraping.save_news(title, title, category, news_url, image_url, source="jagonews24.com")
                        if news_obj:
                            response.append(news_obj.id)
                        
                    except Exception as inner_e:
                        print(f"Error parsing a card: {inner_e}")
            else:
                print(f"Request failed with status code {res.status_code}")
        except Exception as e:
            print(f"The Daily Star error: {e}")
        return response
    
    def scrape_bdcrictime(topic, category=None):
        response = []
        base_url = 'https://bn.bdcrictime.com/'
        url = base_url + topic
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            print(url, res.status_code)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')

                cards = soup.select(".post2")
                for card in cards:
                    try:
                        # Title and link
                        link_tag = card.select_one(".content a")
                        title = link_tag.text.strip() if link_tag else "None"
                        news_url = base_url + link_tag['href'] if link_tag and link_tag.has_attr('href') else "None"

                        # Image
                        img_tag = card.select_one("img")
                        raw_image_url = img_tag.get('data-src') or img_tag.get('src') if img_tag else None
                        image_url = raw_image_url

                        if not image_url or not title or not news_url or News.objects.filter(title=title, url=news_url):
                            # # print('*** skipping ***')
                            continue

                        news_obj = Scraping.save_news(title, title, category, news_url, image_url, source="bdcrictime.com")
                        response.append(news_obj.id)
                        
                    except Exception as inner_e:
                        print(f"Error parsing a card: {inner_e}")
            else:
                print(f"Request failed with status code {res.status_code}")
        except Exception as e:
            print(f"The Daily Star error: {e}")
        return response
    
    def scrape_bbc_pets_news():
        base_url = 'https://www.bbc.com'
        url = 'https://www.bbc.com/news/topics/c51grdzv08yt'

        def process_image_url(url):
            return url.replace('/480/', '/999/')

        response = requests.get(url, headers=HEADERS, timeout=30)
                
        print()
        print('***'*30)
        print(url, response.status_code)
        if response.status_code != 200: 
            print('*** skipping for status code ***')
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        response = []
        cards = soup.select('.sc-225578b-0.btdqbl')
        for card in cards:
            # Article URL
            url_tag  = card.select_one('a')
            news_url = base_url + url_tag['href']

            # Title
            title_tag = card.select_one('[data-testid="card-headline"]')
            title = title_tag.text.strip() if title_tag else ""

            # Intro
            intro_tag = card.select_one('[data-testid="card-description"]')
            intro = intro_tag.text.strip() if intro_tag else ""

            # Date
            date_tag = card.select_one('[data-testid="card-metadata-lastupdated"]')
            date = date_tag.text.strip() if date_tag else ""

            # Tag/Location
            tag_tag = card.select_one('[data-testid="card-metadata-tag"]')
            tag = tag_tag.text.strip() if tag_tag else ""

            # Image URL (get largest version from srcset)
            img_tag = card.select_one('img.sc-d1200759-0.dvfjxj')
            image_url = process_image_url(img_tag['src']) if img_tag else ""

            if not image_url or not title or not news_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            news_obj = Scraping.save_news(title, intro, "Pets", news_url, image_url, source="bbc.com", type="en")
            response.append(news_obj.id)
        return response

    
    def scrape_lawyersclubbangladesh(topic, category=None):
        base_url = 'https://lawyersclubbangladesh.com/category/'

        url = base_url + topic
        response = requests.get(url=url, headers=HEADERS, timeout=30)
                
        print()
        print('***'*30)
        print(url, response.status_code)
        if response.status_code != 200: 
            print('*** skipping for status code ***')
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        def process_image_url(url):
            url = url.replace('-421x281', '')
            url = url.replace('-100x100', '')
            url = url.replace('-150x150', '')
            url = url.replace(' ', '')
            return url
        
        news_ids = []
        cards = soup.select("article.tipi-xs-12.clearfix.with-fi.ani-base")
        for card in cards:
            title_tag = card.select_one("h3.title a")
            image_tag = card.select_one("a.mask-img img")

            title = title_tag.text.strip() if title_tag else ""
            news_url = title_tag["href"] if title_tag and title_tag.has_attr("href") else ""
            image_url = image_tag["data-lazy-src"] if image_tag and image_tag.has_attr("data-lazy-src") else ""

            image_url = process_image_url(image_url)

            if not image_url or not title or not news_url or News.objects.filter(title=title, url=news_url):
                # # print('*** skipping ***')
                continue

            news_obj = Scraping.save_news(title, title, category, news_url, image_url, source="lawyersclubbangladesh.com")
            if news_obj:
                news_ids.append(news_obj.id)
        return news_ids

    def scrape_all_lawyersclubbangladesh_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all lawyersclubbangladesh news...")

        news_ids = []
        news_ids += Scraping.scrape_lawyersclubbangladesh("পড়াশোনা/", "Education")
        news_ids += Scraping.scrape_lawyersclubbangladesh("বিশেষ-সংবাদ/", "Special News")
        news_ids += Scraping.scrape_lawyersclubbangladesh("আদালত-প্রাঙ্গণ/", "Courthouse")
        news_ids += Scraping.scrape_lawyersclubbangladesh("দৈনন্দিন-জীবনে-আইন/", "Daily Law")
        news_ids += Scraping.scrape_lawyersclubbangladesh("সংসদ-ও-মন্ত্রী-সভা/", "Parliament and Cabinet")

        National_news_ids = Scraping.scrape_lawyersclubbangladesh("জাতীয়/", "National")

        news_ids += National_news_ids
        Helper.log_scraping_news('Lawer Club Bangladesh', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SCHOLAR_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, National_news_ids)

        return news_ids

    def scrape_all_khela_news():
        Cricket_news_ids = Scraping.scrape_khela('cricket', 'Cricket')
        Football_news_ids = Scraping.scrape_khela('football', 'Football')

        news_ids = Cricket_news_ids + Football_news_ids
        Helper.log_scraping_news('Khela', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_CRICKET_PAGE_ID, Cricket_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_FOOTBALL_PAGE_ID, Football_news_ids)
        return news_ids
    
    def scrape_all_pets_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all pets news...")
        news_ids = Scraping.scrape_bbc_pets_news()
        Helper.log_scraping_news('Pets', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_PetVerse_PAGE_ID, news_ids)
        return news_ids

    def scrape_all_jagonews24_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all jagonews24 news...")
        news_ids = []

        Cricket_news_ids = Scraping.scrape_jagonews24('sports/cricket', 'Cricket')
        Football_news_ids = Scraping.scrape_jagonews24('sports/football', 'Football')
        Entertainment_news_ids = Scraping.scrape_jagonews24('entertainment/hollywood', 'Entertainment')
        Entertainment_news_ids += Scraping.scrape_jagonews24('entertainment/bollywood', 'Entertainment')

        news_ids += Cricket_news_ids + Football_news_ids + Entertainment_news_ids
        Helper.log_scraping_news('Jagonews24', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_CRICKET_PAGE_ID, Cricket_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Cricket_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Football_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_FOOTBALL_PAGE_ID, Football_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Cricket_news_ids + Football_news_ids)
        return news_ids
    
    def scrape_all_daily_star_en_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all daily star english news...")
        news_ids = []
        news_ids += Scraping.scrape_daily_star_en('business', 'Business')

        Sports_news_ids = Scraping.scrape_daily_star_en('sports', 'Sports')
        TechStartup_news_ids = Scraping.scrape_daily_star_en('tech-startup', 'TechStartup')
        Bangladesh_news_ids = Scraping.scrape_daily_star_en('news/bangladesh', 'Bangladesh')
        Entertainment_news_ids = Scraping.scrape_daily_star_en('entertainment', 'Entertainment')

        news_ids += TechStartup_news_ids
        news_ids += Sports_news_ids + Bangladesh_news_ids + Entertainment_news_ids

        Helper.log_scraping_news('Daily Star English', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, Bangladesh_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, TechStartup_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_TERABYTE_PAGE_ID, TechStartup_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Entertainment_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)

        return news_ids

    def _scrape_all_ew_en_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all ew news...")
        news_ids = []
        news_ids += Scraping.scrape_ew_en_news('books', 'Books')
        # Scraping.scrape_ew_en_news('binge', 'Entertainment')
        news_ids += Scraping.scrape_ew_en_news('music', 'Entertainment')
        news_ids += Scraping.scrape_ew_en_news('movies', 'Entertainment')
        news_ids += Scraping.scrape_ew_en_news('celebrity', 'Celebrities')
        
        Helper.log_scraping_news('EW', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, news_ids)
        
        return news_ids
    

    def scrape_all_jugantor_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all jugantor news...")
        news_ids = []
        # return news_ids
        # news_ids += Scraping.scrape_jugantor('health', 'Health')
        news_ids += Scraping.scrape_jugantor('economics', 'Economy')
        # news_ids += Scraping.scrape_jugantor('business', 'Business')

        Sports_news_ids = Scraping.scrape_jugantor('sports', 'Sports')
        Jobs_news_ids = Scraping.scrape_jugantor('job-seek', 'Jobs')
        Politics_news_ids = Scraping.scrape_jugantor('politics', 'Politics')
        Technology_news_ids = []
        # Technology_news_ids = Scraping.scrape_jugantor('technology', 'Technology')
        Entertainment_news_ids = Scraping.scrape_jugantor('entertainment', 'Entertainment')

        news_ids += Politics_news_ids + Jobs_news_ids
        news_ids += Technology_news_ids + Entertainment_news_ids + Sports_news_ids

        Helper.log_scraping_news('Jugantor', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, Jobs_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SCHOLAR_PAGE_ID, Jobs_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, Politics_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_TERABYTE_PAGE_ID, Technology_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)
        # print("\n\nDone, Scraping all jugantor news...")
        return news_ids
    
    def scrape_all_dainikshiksha_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all dainikshiksha news...")
        dainikshiksha_data = [
            (2, 'College'),
            (4, 'University'),
            (6, 'Madrasha'),
            (7, 'School'),
            (14, 'Admission'),
            (17, 'JobNews'),
        ]
        news_ids = []
        for category_id, category in dainikshiksha_data:
            news_ids += Scraping.scrape_dainikshiksha_news(category_id, category)

        Helper.log_scraping_news('Dainik Shiksha', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SCHOLAR_PAGE_ID, news_ids)
        # print("\n\nDone, Scraping all dainikshiksha news...")
        return news_ids
    
    def scrape_all_bd_pratidin_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all bd pratidin news...")
        news_ids = []
        news_ids += Scraping.scrape_bd_pratidin('islam', 'Islam')
        news_ids += Scraping.scrape_bd_pratidin('economy', 'Economy')
        news_ids += Scraping.scrape_bd_pratidin('national', 'National')
        news_ids += Scraping.scrape_bd_pratidin('health-tips', 'Health')
        news_ids += Scraping.scrape_bd_pratidin('city-news', 'City News')

        Sports_news_ids = Scraping.scrape_bd_pratidin('sports', 'Sports')
        Science_news_ids = Scraping.scrape_bd_pratidin('science', 'Science')
        Politics_news_ids = Scraping.scrape_bd_pratidin('minister-spake', 'Politics')
        Entertainment_news_ids = Scraping.scrape_bd_pratidin('entertainment', 'Entertainment')

        news_ids += Science_news_ids
        news_ids += Entertainment_news_ids + Sports_news_ids + Politics_news_ids

        Helper.log_scraping_news('BD Pratidin', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Science_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, Politics_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Entertainment_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)
        # print("\n\nDone, Scraping all bd pratidin news...")
        return news_ids
    
    def scrape_all_bbc_bangla_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all bbc bangla news...")
        news_ids = []
        news_ids += Scraping.scrape_bbc_bangla('cg7265yyxn1t', 'Health')
        news_ids += Scraping.scrape_bbc_bangla('cjgn7233zk5t', 'Economy')
        
        
        World_news_ids = Scraping.scrape_bbc_bangla('c907347rezkt', 'World')
        Sports_news_ids = Scraping.scrape_bbc_bangla('cdr56g57y01t', 'Sports')
        Politics_news_ids = Scraping.scrape_bbc_bangla('cqywj91rkg6t', 'Politics')
        Technology_news_ids = Scraping.scrape_bbc_bangla('c8y94k95v52t', 'Technology')

        news_ids += World_news_ids
        news_ids += Technology_news_ids + Sports_news_ids + Politics_news_ids
        Helper.log_scraping_news('BBC Bangla', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, World_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, Politics_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Technology_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_TERABYTE_PAGE_ID, Technology_news_ids)
        # print("\n\nDone, Scraping all bbc bangla news...")
        return news_ids
    
    def scrape_all_daily_star_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all daily star news...")
        news_ids = []
        news_ids += Scraping.scrape_daily_star('health', 'Health')
        news_ids += Scraping.scrape_daily_star('business', 'Business')

        Abroad_news_ids = Scraping.scrape_daily_star('abroad', 'Abroad')
        Sports_news_ids = Scraping.scrape_daily_star('sports', 'Sports')
        Technology_news_ids = Scraping.scrape_daily_star('tech-startup', 'Technology')
        Education_news_ids = Scraping.scrape_daily_star('youth/education', 'Education')
        Entertainment_news_ids = Scraping.scrape_daily_star('entertainment', 'Entertainment')

        news_ids += Abroad_news_ids
        news_ids += Entertainment_news_ids + Education_news_ids + Technology_news_ids + Sports_news_ids
        
        Helper.log_scraping_news('Daily Star', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Abroad_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Entertainment_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Entertainment_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_TERABYTE_PAGE_ID, Technology_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)
        # print("\n\nDone, Scraping all daily star news...")
        return news_ids
    
    def scrape_all_bdcrictime_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all bdcrictime news...")
        news_ids = []

        Sports_news_ids = Scraping.scrape_bdcrictime('news', 'Cricket')

        news_ids += Sports_news_ids
        
        Helper.log_scraping_news('BD CricTime', news_ids=news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_CRICKET_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        # print("\n\nDone, Scraping all bdcrictime news...")
        return news_ids
    
    def scrape_all_shikshabarta_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all shikshabarta news...")
        news_ids = []

        Jobs_news_ids = Scraping.scrape_shikshabarta_news("চাকরি/", "Jobs")
        Sports_news_ids = Scraping.scrape_shikshabarta_news("স্পোর্টস/", "Sports")
        College_news_ids = Scraping.scrape_shikshabarta_news("কলেজ/", "College")
        Madrasa_news_ids = Scraping.scrape_shikshabarta_news("মাদরাসা/", "Madrasa")
        Education_news_ids = Scraping.scrape_shikshabarta_news("পড়ালেখা/", "Education")
        Entertainment_news_ids = Scraping.scrape_shikshabarta_news("বিনোদন/", "Entertainment")
        Middle_School_news_ids = Scraping.scrape_shikshabarta_news("মাধ্যমিক/", "Middle School")
        Primary_School_news_ids = Scraping.scrape_shikshabarta_news("প্রাথমিক/", "Primary School")
        Technical_Education_news_ids = Scraping.scrape_shikshabarta_news("কারিগরি/", "Technical Education")

        news_ids += Education_news_ids + Jobs_news_ids
        news_ids += Technical_Education_news_ids + Madrasa_news_ids
        news_ids += Middle_School_news_ids + Primary_School_news_ids + College_news_ids
        
        Helper.set_queue_news_to_page(constants.GEMTEN_Citizen_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SCHOLAR_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_SPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ESPORTS_PAGE_ID, Sports_news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_Global_PAGE_ID, Entertainment_news_ids)

        news_ids += Sports_news_ids + Entertainment_news_ids
        Helper.set_queue_news_to_page(constants.GEMTEN_NEWS_PAGE_ID, news_ids)
        Helper.set_queue_news_to_page(constants.GEMTEN_ShowBiz_PAGE_ID, Entertainment_news_ids)
        Helper.log_scraping_news('Shikshabarta', news_ids=news_ids)
        
        # print("\n\nDone, Scraping all shikshabarta news...")
        return news_ids
    


    def scrape_all_news():
        print()
        print()
        print('^^^'*30)
        print("Scraping all news...")
        news_ids = []
        news_ids += Scraping.scrape_all_pets_news()
        news_ids += Scraping.scrape_all_khela_news()
        # news_ids += Scraping.scrape_all_jugantor_news()
        news_ids += Scraping._scrape_all_ew_en_news()
        news_ids += Scraping.scrape_all_bdcrictime_news()
        news_ids += Scraping.scrape_all_bdcrictime_news()
        news_ids += Scraping.scrape_all_jagonews24_news()
        news_ids += Scraping.scrape_all_bbc_bangla_news()
        news_ids += Scraping.scrape_all_daily_star_news()
        news_ids += Scraping.scrape_all_bd_pratidin_news()
        news_ids += Scraping.scrape_all_shikshabarta_news()
        news_ids += Scraping.scrape_all_daily_star_en_news()
        news_ids += Scraping.scrape_all_dainikshiksha_news()
        news_ids += Scraping.scrape_all_lawyersclubbangladesh_news()
        
        print("\n\nDone, Scraping all news...")
        Helper.log_scraping_news('😝 All News Site', news_ids=news_ids)

        return news_ids
    

    def _scrape_all__news():
        news_ids = []
        return news_ids

