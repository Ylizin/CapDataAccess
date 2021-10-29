from shibor import get_shibor,shibor_map
import schedule
import time 

if __name__ == '__main__':
    
    from functools import partial
    reps = [partial(get_shibor,ty) for ty in shibor_map.keys()]

    [print(schedule.every().day.at('16:00:00').do(rep)) for rep in reps]
    while True:
        schedule.run_pending()
        time.sleep(10)