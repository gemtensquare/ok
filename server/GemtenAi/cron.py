
CRONJOBS = [
    
    
    ('*/10 * * * *', 'Helper.cron.cron_scrape_all_news'),
    ('*/5 * * * *', 'Helper.cron.cron_auto_post_news_to_all_pages'),


    # ('*/4 * * * *', 'Helper.cron.cron_post_to_facebook_page'),
    ('*/10 * * * *', 'Helper.cron.cron_scrape_all_jugantor_news'),
    ('*/15 * * * *', 'Helper.cron.cron_scrape_all_bdcrictime_news'),
    # ('*/15 * * * *', 'Helper.cron.cron_scrape_all_bbc_bangla_news'),
    # ('*/15 * * * *', 'Helper.cron.cron_scrape_all_bd_pratidin_news'),
    # ('*/20 * * * *', 'Helper.cron.cron_scrape_all_daily_star_news'), # make this comment! no need at this time.
    # ('*/1 * * * *', 'Helper.cron.my_1_minute_job'),
]