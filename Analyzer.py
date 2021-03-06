from collections import defaultdict
from Calculator import *

import pprint
import pyparsing
import re

def card_check(card, target, operator, criterion, weighted=False, split=False, back=False):
    """
    :param card: (Card.Card)
    :param target: (str) that in card property dict
    :param operator: (str) that will be parsed to operate target property and criterion
    :param criterion: (str) that allowed in target property range
    :param weighted: (bool) if True, weighted value will be returned from target property
    :param split: (bool) For split cards. 
                  if True, each left/right card face will be checked together, if false, only physical card itself is checked.
    :param back: (bool) For flip and transform cards. 
                 if True, front and back card face will be checked together, if false, only front card face is checked.
    
    :return: (list of SimpleCard) return all cards that meets criterion in a list
    """
    pass

def color_breakdown(cardlist, mode="color", weighted=False):

    color_share = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0}
    color_identity = defaultdict(lambda: 0)

    for card in cardlist:
        target = card.get_repr(mode, weighted=weighted)
        color_identity[target] += 1
        if len(target) == 0:
            color_share["C"] += 1
        else:
            for char in target:
                color_share[char] += 1

    if mode == 'color':
        pass

    print("\nColor_breakdown:")
    for key in sorted(color_identity.keys(), key=lambda x: color_to_nick(x)[0]):
        print("{:10}: {:3} of {}, total {:5.2f} %".format(color_to_nick(key)[1], color_identity[key], len(cardlist), 100 * color_identity[key] / len(cardlist)))

    print("\nColor_appearance:")
    for key in color_share.keys():
        print("{}: {:3} of {}, total {:5.2f} %".format(key, color_share[key], len(cardlist), 100*color_share[key]/len(cardlist)))
    print("")


def color_classify(cardlist, mode="color", seperate_split=False, seperate_transform=False):
    for card in cardlist:
        if seperate_split is True:
            pass
        if seperate_transform is True:
            pass


def general_analysis(cardlist, target, color="all", weighted=False, split=False, Transform=False, Flip=False):
    pass


def burden_analysis(cardlist, split=False):
    cmc_breakdown = defaultdict(lambda: defaultdict(lambda: []))
    for card in cardlist:
        if card.properties["nominal"]["layout"] == "Split":
            if split is True:
                cmc = card.properties["side_A"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["side_A"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["side_A"]["mana_cost"], "{} (// {})".format(card.properties["side_A"]["name"], card.properties["side_B"]["name"]), card.actual["nominal"]["quantity"]))

                cmc = card.properties["side_B"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["side_B"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["side_B"]["mana_cost"], "{} (// {})".format(card.properties["side_B"]["name"], card.properties["side_A"]["name"]), card.actual["nominal"]["quantity"]))

            else:
                cmc = card.properties["nominal"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["nominal"]["mana_cost"], card.properties["nominal"]["name"], card.actual["nominal"]["quantity"]))
        elif card.properties["nominal"]["layout"] in ("Flip", "Transform"):
            cmc = card.properties["nominal"]["cmc"]
            generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
            cmc_breakdown[cmc][generic_cmc].append((card.properties["nominal"]["mana_cost"], "{} (// {})".format(card.get_repr("name"), card.get_repr("name", side="back")), card.actual["nominal"]["quantity"]))

        else:
            cmc = card.properties["nominal"]["cmc"]
            generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
            if card.properties["nominal"]["mana_cost"] == "" and card.properties["nominal"]["cmc"] != 0:  # meld card 등
                generic_cmc = card.properties["nominal"]["cmc"]
            cmc_breakdown[cmc][generic_cmc].append((card.properties["nominal"]["mana_cost"], card.properties["nominal"]["name"], card.actual["nominal"]["quantity"]))

    color_burden = {"total": 0}
    card_quantity = {"total": 0}
    for i in sorted(cmc_breakdown.keys()):
        print("CMC %d:" % i)
        color_burden["local"] = 0
        card_quantity["local"] = 0
        for j in sorted(cmc_breakdown[i].keys(), reverse=True):
            color_burden["partial"] = 100*(i-j)/i if i != 0 else 0
            card_quantity["partial"] = 0
            for k in cmc_breakdown[i][j]:
                card_quantity["partial"] += k[2]

            card_quantity["local"] += card_quantity["partial"]
            card_quantity["total"] += card_quantity["local"]
            color_burden["local"] += color_burden["partial"] * card_quantity["partial"]
            color_burden["total"] += color_burden["local"]

            print(" '{}' color burden({:2.1f}% of total CMC): {} card(s)".format(i-j, color_burden["partial"], card_quantity["partial"]))
            for k in sorted(cmc_breakdown[i][j]):
                print("   x%s, [%s]: %s" % (k[2], symbolprettify(k[0]), k[1]))
        print(" Average color burden in CMC {} is: {:2.2f}%\n".format(i, color_burden["local"]/card_quantity["local"]))

    print("Total average color burden is: {:2.2f}%\n".format(color_burden["total"]/card_quantity["total"]))


def color_requirement_analysis(cardlist):
    symbols_breakdown = defaultdict(lambda: 0)

    weight = {
        'hybrid': 0.75,
        'mono_hybrid': 0.68,
        'pyrexian' : 0.1,
    }

    for card in cardlist:
        cmc = card.properties["cmc"]
        symbols = re.findall(r'{W}', card.properties["mana_cost"])
        hybrid_symbols = re.findall(r'{W/U}|{G/W}|{W/B}|{R/W}', card.properties["mana_cost"])
        mono_hybrid_symbols = re.findall(r'{2/W}', card.properties["mana_cost"])
        pyrexian_symbols = re.findall(r'{W/P}', card.properties["mana_cost"])
        burden = 0

    ''' {W/U}
        {U/B}
        {B/R}
        {R/G}
        {G/W}
        {W/B}
        {B/G}
        {G/U}
        {U/R}
        {R/W}
        '''

    raise NotImplementedError


def pt_breakdown(cardlist, mode="pt"):

    cmc_breakdown = defaultdict(lambda: defaultdict(lambda: []))

    raise NotImplementedError


def tag_breakdown(cardlist):
    raise NotImplementedError


