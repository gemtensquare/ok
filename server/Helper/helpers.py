from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
import os, textwrap, random, time, requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from . import constants
from Pages.models import GemtenPage
from News.models import News, Template
from Facebook.facebook_helper import Facebook

class Helper:
    def helper():
        pass

    def set_queue_news_to_page(page_id, news_ids):
        old_news_ids = cache.get(page_id, [])
        news_ids = list(set(old_news_ids + news_ids))
        cache.set(page_id, news_ids, timeout=None)


    def process_jugantor_image_url(image_url):
        url = None
        if image_url:
            url = image_url.replace('medium/', '')
        return url

    def process_bd_protidin_image_url(image_url):
        url = None
        if image_url:
            url = image_url.replace('thumbnails/', '')
        return url

    def process_bbc_news_image_url(url):
        url = url.replace('ws/240/', 'ws/999/')
        url = url.replace('.webp', '')
        return url
    
    def process_dayli_start_news_image_url(url):
        url = url.replace('big_201', 'very_big_1')
        url = url.replace('big_202', 'very_big_1')
        url = url.replace('medium_201', 'very_big_1')
        url = url.replace('medium_202', 'very_big_1')
        url = url.replace(' 1x', '')
        return url
    
    def process_jagonews24_news_image_url(image_url):
        url = None
        if image_url:
            url = image_url.replace('media/imgAllNew/XS/', 'media/imgAllNew/BG/')
            url = url.replace('media/imgAllNew/SM/', 'media/imgAllNew/BG/')
        return url

    def get_a_unique_image_name():
        image_name = f"{int(time.time())}_{random.randint(1, int(1e5))}.jpg"
        return image_name
    
    def wrap_bangla_text(text, font, max_width, draw):
        words = text.split(" ")
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())
        return lines
    
    def get_font_path(is_bangla_news):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, 'static', 'Geist-Bold.ttf')
        if is_bangla_news:
            font_path = os.path.join(BASE_DIR, 'static', 'NotoSerifBengali-ExtraBold.ttf')

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found at: {font_path}")
        
        return font_path

    def get_date_and_source_font_path():
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(BASE_DIR, 'static', 'NotoSerifBengali-ExtraBold.ttf')
        font_path = os.path.join(BASE_DIR, 'static', 'kalpurush.ttf')
        
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found at: {font_path}")
        
        return font_path

    def get_random_one_page_template_id(page_id):
        templates = Template.objects.filter(page_id=page_id)
        if not templates:
            templates = Template.objects.filter(page_id=constants.GEMTEN_NEWS_PAGE_ID)
        return random.choice(templates).id

    def get_random_one_page_template(page_id):
        templates = Template.objects.filter(page_id=page_id)
        if not templates:
            templates = Template.objects.filter(page_id=constants.GEMTEN_NEWS_PAGE_ID)
        return random.choice(templates)

    
    def log_scraping_news(news_from, news_ids=[]):
        timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
        message = (
            f"{timestamp} — 🐥 Visited [{news_from}] and colleced fresh {len(news_ids)} news! 📡\n"
            # f"{timestamp} — 🧺 IDs safely stored in the treasure chest: 🧾 [{', '.join(map(str, news_ids))}]\n\n"
        )
        if not news_ids or not len(news_ids):
            message = f"{timestamp} — 😴 No new news for [{news_from}] this time. The news birds are resting! 🐦💤\n"
            return

        log_dir = os.path.dirname(constants.NEWS_CRON_LOG_FILE)
        os.makedirs(log_dir, exist_ok=True)  # ✅ Ensure directory exists
        with open(constants.NEWS_CRON_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(message)


    def log_posting_news(page_name, post_count):
        timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
        message = f"{timestamp} — 🐣 Just dropped {post_count} shiny new news posts on [{page_name}]! 🎉✨\n"
        if not post_count:
            message = f"{timestamp} — 😴 No new posts for [{page_name}] this time. The news birds are resting! 🐦💤\n"
            return

        log_dir = os.path.dirname(constants.NEWS_POSTED_LOG_FILE)
        os.makedirs(log_dir, exist_ok=True)  # ✅ Ensure directory exists

        with open(constants.NEWS_POSTED_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(message)


class TemplateHelper:
    def processing_background_image_and_template_image(background_image, template_image, text, is_bangla_news=False):
        print('_^_*'*30)
        print("Start Processing" + " " + str(datetime.now()))

        # Double the size of the background for better quality when resizing/cropping
        bg_upscale = (background_image.width * 2, background_image.height * 2)
        background_image = background_image.resize(bg_upscale, Image.LANCZOS)

        # Apply image filter based on user selection
        filter_choice = "contrast"
        if filter_choice == "contrast":
            background_image = ImageEnhance.Contrast(background_image).enhance(1.5)
        elif filter_choice == "brightness":
            background_image = ImageEnhance.Brightness(background_image).enhance(1.2)
        elif filter_choice == "grayscale":
            background_image = background_image.convert("L").convert("RGBA")  # grayscale, then back to RGBA


        # Define the output canvas size
        canvas_width, canvas_height = 2000, 2500

        # Resize the template to fit the canvas
        template_image = template_image.resize((canvas_width, canvas_height))

        # Get original background size and aspect ratio
        bg_width, bg_height = background_image.size
        bg_ratio = bg_width / bg_height
        canvas_ratio = canvas_width / canvas_height
        b, g, r, a = 0, 255, 0, 0

        # Resize background to match canvas while keeping aspect ratio
        if bg_ratio > canvas_ratio:
            new_height = canvas_height
            new_width = int(bg_ratio * new_height)
        else:
            new_width = canvas_width
            new_height = int(new_width / bg_ratio)

        resized_bg = background_image.resize((new_width, new_height), Image.LANCZOS)

        # Crop center of resized background to match canvas size
        left = (new_width - canvas_width) // 2
        top = (new_height - canvas_height) // 2
        cropped_bg = resized_bg.crop((left, top, left + canvas_width, top + canvas_height))

        # Combine cropped background with the template (alpha compositing)
        combined = Image.alpha_composite(cropped_bg, template_image)

        # Prepare for text drawing
        draw = ImageDraw.Draw(combined)

        # Define the area for the main news text (red box area)
        red_x1, red_y1 = 150, 500
        red_x2, red_y2 = 1800, 300  # red_x2 is width, red_y2 is height
        red_width = red_x2 - red_x1
        red_height = red_y2 - red_y1

        # Store user text from message
        user_data = {}
        user_data["text"] = text

        # Font settings
        max_font_size = 150
        min_font_size = 110

        font_path = Helper.get_font_path(is_bangla_news)
        date_font_path = Helper.get_date_and_source_font_path()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        import unicodedata
        text = unicodedata.normalize('NFC', text)
        
        # If user manually chose font size, use it
        preferred_size = user_data.get("font_size", None)
        if preferred_size:
            font = ImageFont.truetype(font_path, preferred_size)
            lines = textwrap.wrap(text, width=22)
            line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] + 10 for line in lines]
            total_height = sum(line_heights)
        else:
            # Auto-determine font size that fits the box
            for font_size in range(max_font_size, min_font_size, -1):
                font = ImageFont.truetype(font=font_path, size=font_size, layout_engine=ImageFont.Layout.RAQM, encoding='utf-8')
                lines = textwrap.wrap(text, width=30)
                # lines = Helper.wrap_bangla_text(text, font, red_width, draw)
                line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] + 10 for line in lines]
                total_height = sum(line_heights)
                if total_height <= red_height:
                    break

        # Center text vertically
        y_text = red_y1 + (red_height - total_height) // 2

        # Draw each line of text
        for i, line in enumerate(lines):
            line_height = line_heights[i]
            line_width = draw.textlength(line, font=font)
            x_text = (red_width - line_width) // 2 + red_x1
            highlight_keywords = user_data.get("highlight_keywords", [])
            words = line.split()
            current_x = x_text
            for word in words:
                word_width = draw.textlength(word + ' ', font=font)
                part_colors = user_data.get("part_colors", {})
                if word.lower() in part_colors:
                    draw.text((current_x, y_text), word + ' ', font=font, fill=part_colors[word.lower()])
                elif word.lower() in highlight_keywords:
                    draw.text((current_x, y_text), word + ' ', font=font, fill=user_data.get("highlight_color", "yellow"))
                else:
                    draw.text((current_x, y_text), word + ' ', font=font, fill = (b, g, r, a) if user_data.get("text_color") == "black" else user_data.get("text_color", "white"))
                current_x += word_width
            y_text += line_height

        # Add current date in green box area
        date_str = datetime.now().strftime("%B %d, %Y")
        date_font = ImageFont.truetype(date_font_path, 62)
        date_width = draw.textlength(date_str, font=date_font)
        draw.text(((red_width - date_width) // 2 + red_x1, 650), date_str, font=date_font, fill=user_data.get("text_color", "white"))

        print('End Proccesing' + " " + str(datetime.now()))
        print('_^_*'*30)
        return combined
    

    def processing_background_image_and_new_template_image(background_image, template_image, text, source, is_bangla_news):
        font_path = Helper.get_font_path(is_bangla_news)
        date_font_path = Helper.get_date_and_source_font_path()

        # Canvas size (match the template size, e.g., 768x768 or 1024x1024)
        canvas_width, canvas_height = 1024, 1024  # Adjust if needed

        # Resize the template to fit the canvas
        template_image = template_image.resize((canvas_width, canvas_height))
        
        bg_width, bg_height = background_image.size
        bg_ratio = bg_width / bg_height
        canvas_ratio = canvas_width / canvas_height

        if bg_ratio > canvas_ratio:
            new_height = canvas_height
            new_width = int(bg_ratio * new_height)
        else:
            new_width = canvas_width
            new_height = int(new_width / bg_ratio)

        background_resized = background_image.resize((new_width, new_height), Image.LANCZOS)
        left = (new_width - canvas_width) // 2
        top = (new_height - canvas_height) // 2
        background_cropped = background_resized.crop((left, top, left + canvas_width, top + canvas_height))

        # === APPLY FILTER (OPTIONAL) ===
        background_cropped = ImageEnhance.Brightness(background_cropped).enhance(1.090)

        # === COMBINE TEMPLATE ===
        final_image = Image.alpha_composite(background_cropped, template_image)
        draw = ImageDraw.Draw(final_image)

        # === DRAW HEADLINE TEXT ===
        headline_box_x = 50
        headline_box_y = canvas_height - 300
        headline_box_width = canvas_width - 100
        headline_box_height = 340

        # Adjust font size to fit text
        max_font_size, min_font_size = 60, 30

        for font_size in range(max_font_size, min_font_size - 1, -1):
            font = ImageFont.truetype(font_path, font_size)
            lines = textwrap.wrap(text, width=30)
            line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] + 5 for line in lines]
            total_text_height = sum(line_heights)
            if total_text_height <= headline_box_height:
                break

        date_x, date_y = 165, 90
        y_text = headline_box_y + (headline_box_height - total_text_height) // 2

        for i, line in enumerate(lines):
            line_height = line_heights[i]
            line_width = draw.textlength(line, font=font)
            x_text = headline_box_x + (headline_box_width - line_width) // 2
            draw.text((x_text, y_text), line, font=font, fill="#FFFFFF")
            y_text += line_height

        # === DRAW DATE AND SOURCE AT TOP ===
        date_str = datetime.now().strftime("%B %d, %Y") + " Source: " + source
        date_font = ImageFont.truetype(font_path, 30)
        draw.text((date_x, date_y), date_str, font=date_font, fill="#FFFFFF")

        return final_image

    def get_template_color_code(template):
        color_code = "#8acaff"
        if template and 'color_code' in template.metadata:
            color_code = template.metadata['color_code']
        return color_code

    def processing_background_image_and_update_template_image(background_image, template_image, text, source, is_bangla_news, template=None):
        font_path = Helper.get_font_path(is_bangla_news)
        date_font_path = Helper.get_date_and_source_font_path()

        # === CANVAS DIMENSIONS ===
        canvas_width, canvas_height = 2800, 3500

        # Resize the template to fit the canvas
        template_image = template_image.resize((canvas_width, canvas_height))
        
                
        # === RESIZE BACKGROUND ===
        bg_ratio = background_image.width / background_image.height
        canvas_ratio = canvas_width / canvas_height

        # Keeps as-is; ensures full coverage, might crop
        if bg_ratio > canvas_ratio:
            new_height = canvas_height
            new_width = int(bg_ratio * new_height)
        else:
            new_width = canvas_width
            new_height = int(new_width / bg_ratio)

        resized_bg = background_image.resize((new_width, new_height), Image.LANCZOS)

        # 🔻 Offset background crop to move image downward (+200px shift)
        left = (new_width - canvas_width) // 2
        top = (new_height - canvas_height) // 2 - 850  # ⬅ shift crop down
        # top = max(0, top)  # prevents negative top if image is too short

        cropped_bg = resized_bg.crop((left, top, left + canvas_width, top + canvas_height))
        enhanced_bg = ImageEnhance.Brightness(cropped_bg).enhance(1.1)

        final_image = Image.alpha_composite(enhanced_bg, template_image)
        draw = ImageDraw.Draw(final_image)

        title_color_code = "#8acaff"
        date_source_color_code = "#8acaff"
        title_color_code = TemplateHelper.get_template_color_code(template)
        date_source_color_code = TemplateHelper.get_template_color_code(template)

        date_str = datetime.now().strftime("%d %B %Y") + " | " + source
        date_font = ImageFont.truetype(date_font_path, 85)
        date_text_width = draw.textlength(date_str, font=date_font)
        draw.text((canvas_width - date_text_width - 120, 115), date_str, font=date_font, fill=title_color_code)

        # === HEADLINE TEXT WITHIN BLACK BOX ===
        headline_top = 300
        headline_height = 800
        headline_left = 20
        headline_right = canvas_width - 20
        headline_width = headline_right - headline_left

        # Reduce space from left and right
        headline_left = 100  # was 50
        headline_right = canvas_width - 100  # was canvas_width - 50
        headline_width = headline_right - headline_left

        max_font_size, min_font_size = 220, 90

        for font_size in range(max_font_size, min_font_size - 1, -5):
            font = ImageFont.truetype(font_path, font_size)
            lines = textwrap.wrap(text, width=25)
            line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] + 20 for line in lines]
            total_height = sum(line_heights)
            if total_height <= headline_height:
                break

        y_text = headline_top + (headline_height - total_height) // 2
        y_text = 400
        for i, line in enumerate(lines):
            line_width = draw.textlength(line, font=font)
            x_text = (canvas_width - line_width) // 2
            draw.text((x_text, y_text), line, font=font, fill=date_source_color_code)
            y_text += line_heights[i]

        # === OPTIONAL: BOTTOM IMAGE ===
        # if os.path.exists(bottom_image_path):
        #     logo = Image.open(bottom_image_path).convert("RGBA").resize((400, 400))
        #     final_image.paste(logo, (canvas_width // 2 - 200, canvas_height - 500), logo)


        return final_image

    def process_news_with_new_template(news, template, template_code):
        file_name = os.path.splitext(os.path.basename(news.image.name))[0]
        edited_name = f"{file_name}_template{template.id}.jpg"
        edited_path = os.path.join(settings.MEDIA_ROOT, 'edited_images', edited_name)
        os.makedirs(os.path.dirname(edited_path), exist_ok=True)

        news_image = Image.open(news.image.path).convert("RGBA")
        template_image = Image.open(template.image.path).convert("RGBA")
        image = TemplateHelper.processing_background_image_and_update_template_image(news_image, template_image, news.title, news.source, news.type=='bn', template=template)
        if image.mode == "RGBA":
            image = image.convert("RGB")
        image.save(edited_path)
        
        news.is_edited = True
        news.all_edited_image[template_code] = f"edited_images/{edited_name}"
        news.save()
        return news


class GemtenPostHelper:
    def __init__(self):
        pass

    def publish_news_by_id(page_name, page_id, page_token, news_id):
        news = News.objects.get(id=news_id)
        template = Helper.get_random_one_page_template(page_id)
        
        template_code = f'template{template.id}'
        if template_code not in news.all_edited_image:
            TemplateHelper.process_news_with_new_template(news, template, template_code)

        success_post_count, failed_post_count = 0, 0
        image_path = os.path.join(settings.MEDIA_ROOT, news.all_edited_image.get(template_code))

        timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
        print(f"\n***** {str(timestamp)} '{news_id} news id' Start Posting on ==> '{page_name}'")
        
        intro = news.intro or news.title
        caption=f'{intro} \n\nMore details in Comment Section. {constants.POST_HASHTAGS}'

        facebook = Facebook(page_id=page_id, page_access_token=page_token)
        response = facebook.post_local_image_to_page(image_path=image_path, caption=caption)
        if response.status_code == 200:
            success_post_count += 1
            full_comments = f'{news.intro}\n\n More details: {news.url} {constants.POST_HASHTAGS}'
            # print(f"📌 full_comments:", full_comments)
            facebook.comment_on_post(response.json().get('post_id'), comment=full_comments)
        else:
            failed_post_count += 1
        
        timestamp = timezone.localtime().strftime("%d %B, %Y - %I:%M:%S %p")
        print(f"***** {str(timestamp)} '{news_id} news id' End Posting on ==> '{page_name}'\n")
        
        return success_post_count


    def publish_news_list_to_page(page_name, page_id, page_token, news_ids):
        success_post_ids = []
        for news_id in news_ids:
            is_success = GemtenPostHelper.publish_news_by_id(page_name, page_id, page_token, news_id)
            if is_success:
                success_post_ids.append(news_id)

        Helper.log_posting_news(page_name, len(success_post_ids))
        return success_post_ids

    def process_and_publish_news_to_all_pages():
        success_post_ids = []
        pages = GemtenPage.objects.all()
        for page in pages:
            page_name, page_id, page_token = page.get_name(), page.get_id(), page.get_token()

            news_ids = cache.get(page_id, [])
            first_5_news_ids, last_news_ids = news_ids[:5], news_ids[5:]
            cache.set(page_id, last_news_ids, timeout=None)
            
            success_post_ids += GemtenPostHelper.publish_news_list_to_page(page_name, page_id, page_token, first_5_news_ids)

        Helper.log_posting_news("😍 All Gemten Pages", len(success_post_ids))
        print(f'🐣 Just dropped {len(success_post_ids)} shiny new news posts on 😍 All Gemten Pages! 🎉✨\n')
        return success_post_ids