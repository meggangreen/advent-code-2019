""" Day 14

    Notes:
    - "FUEL" is the goal -- root
    - products from "ORE" are the starting point -- leaves
    - 1xFUEL = sum(leaves) ORE requirements

    even the redditors are commenting on the difficulty of this challenge.
    jeffjeffjeffrey's code is the most helpful to me -- https://github.com/jeffjeffjeffrey/advent-of-code/blob/master/2019/day_14.ipynb

    recipes with ingredients and servings
        eg: recipes = {'A': {'servings': 10,
                             'ingredients': {'ingredient': 'ore', 'amount': 10}}

    orders queue and supply of leftover ingredients

"""

from collections import defaultdict  # supresses key errors
from queue import Queue
from math import ceil
import common as cmn

TEST_INPUT_1 = ["10 ORE => 10 A",
                "1 ORE => 1 B",
                "7 A, 1 B => 1 C",
                "7 A, 1 C => 1 D",
                "7 A, 1 D => 1 E",
                "7 A, 1 E => 1 FUEL"]

TEST_INPUT_2 = ["9 ORE => 2 A",
                "8 ORE => 3 B",
                "7 ORE => 5 C",
                "3 A, 4 B => 1 AB",
                "5 B, 7 C => 1 BC",
                "4 C, 1 A => 1 CA",
                "2 AB, 3 BC, 4 CA => 1 FUEL"]

TEST_INPUT_3 = ["157 ORE => 5 NZVS",
                "165 ORE => 6 DCFZ",
                "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
                "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
                "179 ORE => 7 PSHF",
                "177 ORE => 5 HKGWZ",
                "7 DCFZ, 7 PSHF => 2 XJWVT",
                "165 ORE => 2 GPVTF",
                "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT",]

def parse_ingredient(string):
    """ From jeffjeffjeffrey """

    quantity, ingredient = string.split(' ')
    return {"ingredient": ingredient, "quantity": int(quantity)}


def build_recipes(recipes_list):
    """ From jeffjeffjeffrey """

    recipes = dict()

    for recipe in recipes_list:
        ingredients_string, product_string = recipe.split(' => ')

        ingredients = []
        for ingredient in ingredients_string.split(', '):
            ingredients.append(parse_ingredient(ingredient))

        product = parse_ingredient(product_string)

        recipes[product['ingredient']] = {"servings": product['quantity'],
                                          "ingredients": ingredients}
    
    return recipes


def calc_ore_needed(quantity, recipes):
    """ From jeffjeffjeffrey """

    supply = defaultdict(int)
    orders = Queue()
    orders.put({"ingredient": "FUEL", "quantity": quantity})
    ore_needed = 0

    while not orders.empty():
        order = orders.get()

        if order['ingredient'] == "ORE":
            ore_needed += order['quantity']

        elif order['quantity'] <= supply[order['ingredient']]:
            supply[order['ingredient']] -= order['quantity']

        else:
            quantity_needed = order['quantity'] - supply[order['ingredient']]
            recipe = recipes[order['ingredient']]
            batches = ceil(quantity_needed / recipe['servings'])
            for ingredient in recipe['ingredients']:
                orders.put({"ingredient": ingredient['ingredient'], 
                            "quantity": ingredient['quantity'] * batches})
            leftover_quantity = batches * recipe['servings'] - quantity_needed
            supply[order['ingredient']] = leftover_quantity

    return ore_needed


def calc_fuel_given_ore(ore, recipes):
    """ From jeffjeffjeffrey with modified lower_bound """

    upper_bound = None
    lower_bound = 469536  # assume ore needed for 1 fuel is good lower bound


    while lower_bound + 1 != upper_bound:
        if upper_bound is None:
            guess = lower_bound * 2
        else:
            guess = (upper_bound + lower_bound) // 2
            
        ore_needed = calc_ore_needed(guess, recipes)
        if ore_needed > ore:
            upper_bound = guess
        else:
            lower_bound = guess
    
    return lower_bound


##########
if __name__ == "__main__":
    test_recipes_1 = build_recipes((TEST_INPUT_1))
    test_recipes_2 = build_recipes((TEST_INPUT_2))
    test_recipes_3 = build_recipes((TEST_INPUT_3))
    assert calc_ore_needed(1, test_recipes_1) == 31
    assert calc_ore_needed(1, test_recipes_2) == 165
    assert calc_ore_needed(1, test_recipes_3) == 13312

    recipes = build_recipes(cmn.listify_input_file("14-input.txt"))
    print(f"Part 1: {calc_ore_needed(1, recipes)}")  # answer 469536
    print(f"Part 2: {calc_fuel_given_ore(1000000000000, recipes)}")  # answer 3343477
