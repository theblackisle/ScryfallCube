from collections import defaultdict
from Converter import *

import pprint
from pyparsing import *
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

def listfilter(query, cardlist):
    nest_stctr = _listfilter_nest_parser(query)

    filted_list = _listfilter_expr_parser(nest_stctr, cardlist)

    return filted_list


def _listfilter_nest_parser(query):
    """

    :param query: str
    :return: <class 'pyparsing.ParseResults'>, a iterable which contains str or other ParseResults instances
    """

    query = "(" + query + ")"
    parsed_query = nestedExpr().searchString(query)[0][0]
    # (subtype:goblin SEX AND CITY) (hello) () NONO

    return parsed_query

def _listfilter_expr_parser(nest_stctr, cardlist):
    flag = "OR"
    result = set()

    for item in nest_stctr:
        if item in ("OR", "AND", "EXCEPT"):
            flag = item

        else:
            if type(item) is ParseResults:
                local_result = _listfilter_expr_parser(item, cardlist)

            elif type(item) is str:
                local_result = _listfilter_interpreter(item, cardlist)

            if flag == "AND":
                result &= local_result
            elif flag == "OR":
                result |= local_result
            elif flag == "EXCEPT":
                result -= local_result
            flag = "AND"

    return list(result)

def _listfilter_interpreter(query, cardlist=0, weighted=False, split=False):
    propertyWord = Word(alphas + "_")
    operatorWord = Literal(">=") | Literal("<=") | Literal("!=") | Literal("!:") | Literal("=") | Literal(":") | Literal(">") | Literal("<")
    valueWord = Word(alphanums + "*{}_,.:;+-/'æÆ" + '"')  # oracle:{T}:

    searchquery = propertyWord.setResultsName('property') + operatorWord.setResultsName('operator') + valueWord.setResultsName('value')
    parsedresult = searchquery.parseString(query)

    result = set()
    for card in cardlist:
        if _listfilter_operator(card, parsedresult["property"], parsedresult["operator"], parsedresult["value"]):
            result.add(card)

    return parsedresult

def _listfilter_operator(card, properties, operator, value):


    return True


def _listfilter_comparer(cardlist, weighted=False, split=False):


    expr_set = []
    searchset = []

    result_list = []

    for card in cardlist:
        if card.get_repr():
            pass

    parser = nestedExpr(opener="(", closer=")")
    parsed_query = parser.searchString(inputs)

    print(parsed_query)
    for nest in parsed_query:
        print(nest)

    found_expr = re.findall(r'(?:(?:\S+)(?:(?:>=)|(?:<=)|(?:!=)|(?:!:)|[=:><])(?:\S+))|(?:AND|OR|EXCEPT)', inputs)
    # A OR A-BB : word OR (spaced query with parentheses)

    expr_set = []
    searchset = []

    for item in found_expr:
        if item in ("OR", "AND", "EXCEPT"):
            expr_set.append((None, None, item))

    # return




    return result_list




def list_sorter():
    pass

while __name__ == '__main__':
    query = input("parse for: ")
    if query == "quit":
        break

    print(_listfilter_interpreter(query))