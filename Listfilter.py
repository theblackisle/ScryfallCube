from collections import defaultdict
from Converter import *

import pprint
import pyparsing
import re


def concatenate_list(*cardlists, ignore_set=False, sum_dupl=False):
    """
    Card list들을 받아서 하나의 list로 합치고 중복되는 카드를 삭제함.

    Args:
        *cardlists (list): args of lists of Cards
        ignore_set (bool): set이 달라도 name이 같으면 중복으로 처리함.
        sum_dupl (bool): 중복 카드를 삭제하면서 둘의 quantity를 더함.
    """

    total_cards = 0
    dupl_cards = 0
    seen = set()
    unique_sheet = []
    if sum_dupl:
        dupl_sheet = []

    for cardlist in cardlists:
        total_cards += len(cardlist)
        for card in cardlist:
            sample = card.get_repr("name") if ignore_set else card
            if sample not in seen:
                # set의 'in' operator는 __hash__를 통해 1차비교 후, 값이 같으면 __eq__로 2차비교한다.
                seen.add(sample)
                unique_sheet.append(card)
            else:
                print(card, "is duplicated.")
                dupl_cards += 1
                if sum_dupl:
                    dupl_sheet.append(card)

    if sum_dupl:
        for card in dupl_sheet:
            involved_card = next((x for x in unique_sheet if x.get_repr("name") == card.get_repr("name"))) \
                if ignore_set else next((x for x in unique_sheet if x == card))
            involved_card.actual["nominal"]["quantity"] += card.actual["nominal"]["quantity"]
            unique_sheet[unique_sheet.index(involved_card)] = involved_card  # involved_card quantity 변경 후 update

    print("%s cards are collected." % total_cards)
    print("%s duplicated cards are removed from list." % dupl_cards)
    print("%s cards in list by now." % len(unique_sheet))
    return unique_sheet


def _parser_printer(item, indent=0):
    isclose = False
    if type(item) is str:
        print(" "*indent, item)

    else:
        print(" "*(indent), "(")
        if len(item) == 0:
            print(" "*(indent+1), "*NULL*")
        for inner_item in item:
            _parser_printer(inner_item, indent=indent+1)
        isclose = True

    if isclose:
        print(" " *(indent), ")")

def listfilter_parser(query):
    query = "(" + query + ")"
    parsed_query = pyparsing.nestedExpr().searchString(query)[0][0]
    # (subtype:goblin SEX AND CITY) (hello) () NONO

    return parsed_query

    #found_expr = re.findall(r'(?:(?:[\S]+)(?:(?:>=)|(?:<=)|(?:!=)|(?:!:)|[><=!:])(?:[\S]+))|(?:AND|OR|EXCEPT)', parsed_query)

    #print(found_expr)

    # A OR A-BB : word OR (spaced query with parentheses)

def listfilter_interpreter(query):
    pass



def list_filter(cardlist, criterion, operator, value, weighted=False, split=False):
    expr_set = []
    searchset = []

    result_list = []

    for card in cardlist:
        if card.get_repr():
            pass




    return result_list




def list_sorter():
    pass

while __name__ == '__main__':
    query = input("parse for: ")
    if query == "quit":
        break
    print(listfilter_parser(query))
    _parser_printer(listfilter_parser(query))