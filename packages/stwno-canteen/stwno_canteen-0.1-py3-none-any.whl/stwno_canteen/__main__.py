import argparse
import datetime
from .stwno_canteen import getMenu
from .stwno_constants import Canteen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='STWNO canteen API. Main purpose is to be used\
            as a API in other python scripts, although it supports basic command line functionality.\
            Calling this module directly makes it possible to display the menu for the current day\
            for a given canteen.')
    parser.add_argument('-c', '--canteen', required=True,
                        help='ID of the canteen to fetch a menu from. The correct identifier can be\
                        obtained by browsing the stwno website or by looking at the stwno-constants file')
    args = parser.parse_args()
    menu = getMenu(Canteen.OTH_RGB_CANTEEN_LUNCH, datetime.date.today())
    for item in menu:
        print('{:<60} {:.2f}€'.format(item.name, item.pricing.studentPrice))
