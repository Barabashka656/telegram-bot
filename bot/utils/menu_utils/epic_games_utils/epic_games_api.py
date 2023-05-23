from zoneinfo import ZoneInfo
import datetime

from bot.loader import scheduler
from bot.utils.db_api.models_peewee import (
    db,
    EpicFreeGame,
    Utility,
    EpicMail
)
from bot.utils.menu_utils.epic_games_utils import show_epic_free_notification

from epicstore_api import EpicGamesStoreAPI


def get_free_games_dict() -> list | tuple:

    game_url = "https://store.epicgames.com/ru/p/"
    date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    free_games = []

    api = EpicGamesStoreAPI().get_free_games()
    games = api.get('data').get('Catalog').get('searchStore').get('elements')
    # current_time = datetime.datetime.now(ZoneInfo("Europe/Minsk"))

    for game in games:
        # не заносим в бд игры с ценником (платные)
        if game.get('price').get('totalPrice').get('discountPrice') == 0:
            pass
        else:
            continue

        title = game.get('title')
        description = game.get('description')

        if game.get('productSlug'):
            product_slug = game_url + game.get('productSlug')
        else:
            product_slug = game_url + game.get('catalogNs').get('mappings')[0].get('pageSlug')

        is_wide_image = False
        for image in game.get('keyImages'):
            if 'Wide' in image.get('type'):
                key_image_url = image.get('url')
                is_wide_image = True
                break

        if not is_wide_image:
            key_image_url = game.get('keyImages')[0].get('url')

        original_price = game.get('price').get('totalPrice').get('fmtPrice').get('originalPrice')
        if int(original_price):
            original_price += '$'
        else:
            original_price = None

        if game.get('promotions').get('promotionalOffers'):
            dates = game.get('promotions').get('promotionalOffers')[0].get('promotionalOffers')[0]
        else:
            dates = game.get('promotions').get('upcomingPromotionalOffers')[0].get('promotionalOffers')[0]
        raw_start_date = datetime.datetime.strptime(dates.get('startDate'), date_format)
        start_date = raw_start_date.astimezone(ZoneInfo('Europe/Minsk'))

        raw_end_date = datetime.datetime.strptime(dates.get('endDate'), date_format)
        end_date = raw_end_date.astimezone(ZoneInfo('Europe/Minsk'))

        viewable_date = game.get('viewableDate')

        if viewable_date:
            raw_viewable_date = datetime.datetime.strptime(viewable_date, date_format)
            viewable_date = raw_viewable_date.astimezone(ZoneInfo('Europe/Minsk'))

        free_games.append({
                          'title': title,
                          'description': description,
                          'product_slug': product_slug,
                          'key_image_url': key_image_url,
                          'start_date': start_date,
                          'viewable_date': viewable_date,
                          'end_date': end_date,
                          'original_price': original_price
                          })
    return free_games


async def manage_free_games() -> tuple | None:  # TODO(remake): remake func
    """
    The function writes data to the database
    :return:
    """
    flag = True
    try:
        free_games = get_free_games_dict()
    except Exception as e:
        print("getting free games failed")
        print(e.args)
        print(type(e.args))
        return e.args

    current_time = datetime.datetime.now(ZoneInfo("Europe/Minsk"))

    for date_dict in free_games:
        buf_date = date_dict.get('start_date')
        if not buf_date:
            buf_date = date_dict.get('viewable_date')
        if buf_date > current_time:
            new_start_date = buf_date
            flag = False
            break
    if flag:
        new_start_date = date_dict.get('end_date')

    new_end_date = min(game.get('end_date') for game in free_games if game.get('end_date'))
    if not new_start_date:
        run_date = new_end_date + datetime.timedelta(seconds=10)
    else:
        run_date = min(new_start_date, new_end_date) + datetime.timedelta(seconds=10)

    print('next write will be in', run_date)
    try:
        await write_to_database(run_date=run_date, games=free_games)
    except Exception as e:
        print("writing database error:", e)


async def write_to_database(run_date: str, games):
    with db:
        EpicFreeGame.delete().execute()
        EpicFreeGame.insert_many(games).execute()
        print("successful write to database")
        forced_mailing = False
        if forced_mailing:
            Utility(
                next_notification=run_date
            ).save()

        util_column = Utility().get_or_none()
        if not util_column:
            Utility(
                next_notification=run_date
            ).save()
        else:
            util_column.next_notification = run_date
            util_column.save()
            users = EpicMail.select()

            for user in users:
                await show_epic_free_notification(user_id=user.user_id.user_id)

            print("distribution was successful")

        scheduler.add_job(manage_free_games, 'date', run_date=run_date, replace_existing=True, id='epic_job')
        return None
