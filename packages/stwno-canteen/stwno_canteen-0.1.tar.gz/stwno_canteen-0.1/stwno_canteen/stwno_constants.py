from enum import Enum

CSV_DATE_FORMAT = '%d.%m.%Y'
CSV_HEADER_LINE_CNT = 1  # header lines get removed before processing

CSV_INDEX_DATE = 0
CSV_INDEX_MEAL_TYPE = 2
CSV_INDEX_MEAL_AND_META = 3
CSV_INDEX_NUTRITION_TYPE = 4
CSV_INDEX_STUDENT_PRICE = 6
CSV_INDEX_PERSONNEL_PRICE = 7
CSV_INDEX_GUEST_PRICE = 8


class Canteen(Enum):
    UNI_RGB_CANTEEN = 1
    UNI_RGB_GUEST_CANTEEN = 2
    UNI_RGB_CAFETERIA_PT = 3
    UNI_RGB_CAFETERIA_CHEMISTRY = 4
    UNI_RGB_CAFETERIA_SPORT = 5
    OTH_RGB_CANTEEN_LUNCH = 6
    OTH_RGB_CANTEEN_DINNER = 7
    OTH_RGB_CAFETERIA_PRUEFENING = 8
    UNI_PAR_CANTEEN = 9
    UNI_PAR_NIKOLA_MONASTERY_CAFETERIA = 10
    HS_DEG_CANTEEN = 11
    HS_LA_CANTEEN = 12
    HS_SR_CANTEEN = 13
    HS_PAN_CANTEEN = 14


CANTEENS = {
    Canteen.UNI_RGB_CANTEEN: 'UNI-R',
    Canteen.UNI_RGB_GUEST_CANTEEN: 'UNI-R-Gs',
    Canteen.UNI_RGB_CAFETERIA_PT: 'Cafeteria-PT',
    Canteen.UNI_RGB_CAFETERIA_CHEMISTRY: 'Cafeteria-Chemie',
    Canteen.UNI_RGB_CAFETERIA_SPORT: 'Cafeteria-Sport',
    Canteen.OTH_RGB_CANTEEN_LUNCH: 'HS-R-tag',
    Canteen.OTH_RGB_CANTEEN_DINNER: 'HS-R-abend',
    Canteen.OTH_RGB_CAFETERIA_PRUEFENING: 'Cafeteria-pruefening',
    Canteen.UNI_PAR_CANTEEN: 'UNI-P',
    Canteen.UNI_PAR_NIKOLA_MONASTERY_CAFETERIA: 'Cafeteria-Nikolakloster',
    Canteen.HS_DEG_CANTEEN: 'HS-DEG',
    Canteen.HS_LA_CANTEEN: 'HS-LA',
    Canteen.HS_SR_CANTEEN: 'HS-RA',
    Canteen.HS_PAN_CANTEEN: 'HS-PAN'
}


class NutritionType(Enum):
    vegan = 1
    vegetarian = 2
    meat = 3


class MealType(Enum):
    MainDish = 1
    SideDish = 2
    Dessert = 3


CSV_MEAL_TYPE_MAP = {
    'HG': MealType.MainDish,
    'B': MealType.SideDish,
    'N': MealType.Dessert
}

CSV_NUTRITION_TYPE_MAP = {
    'V': NutritionType.vegetarian,
    'S': NutritionType.vegetarian,
    'VG': NutritionType.vegan,
    'M': NutritionType.meat,
    'F': NutritionType.meat
}

CSV_ADDR_FORMAT_STR = 'http://www.stwno.de/infomax/daten-extern/csv/{}/{}.csv'

STWNO_INGREDIENTS = {
    '1': 'colorants',
    '2': 'preservatives',
    '3': 'antioxidants',
    '4': 'flavor enhancers',
    '5': 'sulfured',
    '6': 'blackened',
    '7': 'waxed',
    '8': 'phosphate',
    '9': 'contains sweetener saccharine',
    '10': 'containes sweetener aspartam',
    '11': 'contains sweetener cyclamat',
    '12': 'contains sweetener acesulfam',
    '13': 'quinine',
    '14': 'caffeine',
    '15': 'genetically changed',
    '16': 'contains sulfates',
    '17': 'contains phenylalanin',
}

STWNO_ALLERGENS = {
    'AA': 'wheat gluten',
    'AB': 'rye gluten',
    'AC': 'barley gluten',
    'AD': 'oat gluten',
    'AE': 'spelt gluten',
    'AF': 'kamut gluten',
    'B': 'curstaceans',
    'C': 'eggs',
    'D': 'fish',
    'E': 'peanuts',
    'F': 'soy',
    'G': 'milk and milk products',
    'HA': 'almond',
    'HB': 'hazelnut',
    'HC': 'walnut',
    'HD': 'cashew',
    'HE': 'peca nut',
    'HF': 'brazil nut',
    'HG': 'pistachio',
    'HH': 'macadamia',
    'HI': 'queenslandnuss',
    'I': 'celeriac',
    'J': 'senap',
    'K': 'sesame seeds',
    'L': 'sulfur dioxide and sulfites',
    'M': 'lupines',
    'N': 'molluscs',
    'O': 'nitrate',
    'P': 'nitrate curing salt'
}
