from zoneinfo import ZoneInfo
from pprint import pprint

import datetime

from loader import scheduler
from utils.db_api.models_peewee import *
from utils.menu_utils.epic_games_utils import show_epic_free_notification

from epicstore_api import EpicGamesStoreAPI




import json

async def write_to_database() -> tuple | None:
    """
    The function writes data to the database
    :return:
    """
    flag = True
    game_url = "https://store.epicgames.com/ru/p/"
    unknown_date = datetime.datetime.strptime('2099-01-01T00:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ZoneInfo('Europe/Minsk'))
    free_games = []
    try:
        api = EpicGamesStoreAPI().get_free_games()
        games = api.get('data').get('Catalog').get('searchStore').get('elements')
        current_time = datetime.datetime.now(ZoneInfo("Europe/Minsk"))
        
        for game in games:
            #не заносим в бд игры с ценником
            try:
                if game.get('price').get('totalPrice').get('discountPrice') == 0 and\
                            game.get('price').get('totalPrice').get('fmtPrice').get('discountPrice') == "0" and game.get('promotions'):
                   
                    pass
                else:
                    continue
            except Exception as e: 
                print(e.args)
            title = game.get('title')
            description = game.get('description')
            
            if game.get('productSlug'):
                product_slug = game_url + game.get('productSlug')
            else:
                product_slug = game_url + game.get('catalogNs').get('mappings')[0].get('pageSlug')

            for image in game.get('keyImages'):
                if 'Wide' in image.get('type'):
                    key_image_url = image.get('url')
                    break 

            release_date = datetime.datetime.strptime(game.get('effectiveDate'), "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ZoneInfo('Europe/Minsk'))
            if release_date == unknown_date:
                start_date = None
                end_date = None
            else:
                try:
                    if current_time > release_date:
                        dates = game.get('promotions').get('promotionalOffers')[0].get('promotionalOffers')[0]
                    else:
                        dates = game.get('promotions').get('upcomingPromotionalOffers')[0].get('promotionalOffers')[0]
                except AttributeError as ex:
                        print(ex.args)
                        start_date = None
                        end_date = None
                else:
                    start_date = datetime.datetime.strptime(dates.get('startDate'), "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ZoneInfo('Europe/Minsk'))
                    end_date = datetime.datetime.strptime(dates.get('endDate'), "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(ZoneInfo('Europe/Minsk'))
                    
            

            free_games.append({ 
                                'title': title, 
                                'description': description, 
                                'product_slug': product_slug,
                                'key_image_url': key_image_url, 
                                'start_date': start_date,
                                'end_date': end_date 
                                })
       
        for date_dict in free_games:
            buf_date = date_dict.get('start_date')
            if buf_date > current_time:
                new_start_date = buf_date
                flag = False
                break
        if flag:
            new_start_date = date_dict.get('end_date')

        new_end_date = min(game.get('end_date') for game in free_games if game.get('end_date'))

        run_date = min(new_start_date, new_end_date) + datetime.timedelta(seconds=10)
        print('next write will be in', run_date)
        
        with db:
            EpicFreeGame.delete().execute()
            EpicFreeGame.insert_many(free_games).execute()
            print("successful write to database")
            forced_mailing = False
            if forced_mailing:
                Utility(
                        next_notification = run_date
                        ).save()
                        
            util_column = Utility().get_or_none()

            if not util_column:
                Utility(
                    next_notification = run_date
                    ).save()
            else: 
                util_column.next_notification = run_date
                util_column.save()
                users = EpicMail.select()
                
                for user in users:        
                    await show_epic_free_notification(user_id = user.user_id.user_id)
                    
                print("distribution was successful")
                
           

        
        
        scheduler.add_job(write_to_database, 'date', run_date=run_date, replace_existing=True, id='epic_job')
        return None
    except TypeError as e:
        print(e.args)
        print(type(e.args), 'lol')
        return e.args
    except Exception as e:
        print(e.args)
        print(type(e.args))
        return e.args





