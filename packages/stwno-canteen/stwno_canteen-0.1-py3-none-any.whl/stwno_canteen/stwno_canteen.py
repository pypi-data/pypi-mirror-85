import urllib.request
import datetime
from enum import Enum
import csv
import logging
from typing import List
import re
import argparse
from .stwno_constants import Canteen,\
    CANTEENS,\
    CSV_ADDR_FORMAT_STR,\
    NutritionType,\
    MealType,\
    CSV_MEAL_TYPE_MAP,\
    CSV_NUTRITION_TYPE_MAP,\
    CSV_INDEX_DATE,\
    CSV_INDEX_MEAL_TYPE,\
    CSV_INDEX_MEAL_AND_META,\
    CSV_INDEX_NUTRITION_TYPE,\
    CSV_INDEX_STUDENT_PRICE,\
    CSV_INDEX_PERSONNEL_PRICE,\
    CSV_INDEX_GUEST_PRICE,\
    CSV_HEADER_LINE_CNT

from .csv_converters import convertCSVDate,\
    convertCSVDishName,\
    convertCSVMealType,\
    convertCSVNutritionType,\
    convertCSVIngredientsAndAllergens,\
    StwnoFoodIngredient


class StwnoCanteenPricing():
    studentPrice: float
    personnelPrice: float
    guestPrice: float

    def __init__(self, studentPrice: float, personnelPrice: float, guestPrice: float):
        self.studentPrice = studentPrice
        self.personnelPrice = personnelPrice
        self.guestPrice = guestPrice


class Dish():
    name: str
    ingredients: List[StwnoFoodIngredient]
    allergens: List[StwnoFoodIngredient]
    mealType: MealType
    pricing: StwnoCanteenPricing
    servedOn: datetime.date
    nutritionType: NutritionType

    def __init__(self, name: str, servedOn, nutritionType: NutritionType, ingredients, allergens, mealType, pricing):
        self.name = name
        self.servedOn = servedOn
        self.ingredients = ingredients
        self.allergens = allergens
        self.mealType = mealType
        self.pricing = pricing


def queryStwnoMenu(isoWeekNumber: int, canteen: Canteen) -> str:
    canteenID = CANTEENS[canteen]
    csvAddr = CSV_ADDR_FORMAT_STR.format(canteenID, isoWeekNumber)
    csvData = urllib.request.urlopen(csvAddr)
    csvString = csvData.read().decode('latin-1')
    return csvString


def getMenu(canteen: Canteen, day: datetime.date) -> List[Dish]:
    '''
    Get the menu of a STWNO canteen for a specific day

    Parameters
    -----------
        canteen (Canteen): The canteen to get the menu for
        day (datetime.date): The day of the menu

    Raises
    -------
        NoValidDateStringException
            The menu date returned from the Stwno api contained a malformatted date
        UnknownMealTypeException
            The meal type of a menu item returned from the Stwno api is unknown
        UnknownNutritionTypeException
            The nutrition type of a menu item returned from the Stwno api is unknown

    Returns
    --------
        The dishes served on the specified day in the specified Stwno canteen

    '''

    isoWeekNumber = day.isocalendar()[1]
    csvMenu = queryStwnoMenu(isoWeekNumber, canteen)
    csvReader = csv.reader(csvMenu.splitlines(), delimiter=';')
    rawMenu = list(csvReader)[CSV_HEADER_LINE_CNT:]
    dishes = []
    for rawDish in rawMenu:
        servedOn = convertCSVDate(rawDish[CSV_INDEX_DATE])
        dishName = convertCSVDishName(rawDish[CSV_INDEX_MEAL_AND_META])
        try:
            ingredients, allergens = convertCSVIngredientsAndAllergens(
                rawDish[CSV_INDEX_MEAL_AND_META])
        except:
            ingredients = allergens = []
        mealType = convertCSVMealType(rawDish[CSV_INDEX_MEAL_TYPE])
        nutritionType = convertCSVNutritionType(rawDish[CSV_INDEX_NUTRITION_TYPE])
        studentPrice = float(rawDish[CSV_INDEX_STUDENT_PRICE].replace(',', '.'))
        personnelPrice = float(rawDish[CSV_INDEX_PERSONNEL_PRICE].replace(',', '.'))
        guestPrice = float(rawDish[CSV_INDEX_GUEST_PRICE].replace(',', '.'))
        price = StwnoCanteenPricing(studentPrice, personnelPrice, guestPrice)
        dishes.append(Dish(dishName, servedOn, nutritionType,
                           ingredients, allergens, mealType, price))
    dishes = list(filter(lambda dish: dish.servedOn == day, dishes))
    return dishes

