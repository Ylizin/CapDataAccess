from report_crawl import get_url_rep
import schedule
import time 

if __name__ == '__main__':
    code='601995.SH'
    from functools import partial
    rep = partial(get_url_rep,code)
    print(schedule.every().day.at('16:00:00').do(rep))
    while True:
        schedule.run_pending()
        time.sleep(10)
