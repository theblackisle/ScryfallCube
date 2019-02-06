from collections import defaultdict
from Converter import *
import re

def concatenate_list(*cardlists, ignore_set=False, sum_dupl=False):
    """
    Card list들을 받아서 하나의 list로 합치고 중복되는 카드를 삭제함.

    Args:
        *cardlists (list): args of lists of Cards
    """

    total_cards = 0
    dupl_cards = 0
    seen = set()
    unique_sheet = []
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
        dupl_sheet.append(card)


    print("%s cards are collected." % total_cards)
    print("%s duplicated cards are removed from list." % dupl_cards)
    print("%s cards in list by now." % len(unique_sheet))
    return unique_sheet


def color_breakdown(cardlist, mode="color", weighted=False):

    color_share = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0}
    color_identity = defaultdict(lambda: 0)

    for card in cardlist:
        target = card.get_repr(mode, weighted=weighted)
        print(target, card.get_repr("name"))
        color_identity[target] += 1
        if len(target) == 0:
            color_share['C'] += 1
        else:
            for char in target:
                color_share[char] += 1

    if mode == 'color':
        pass

    print("\nColor_breakdown:")
    for key in sorted(color_identity.keys(), key=lambda x: color_to_nick(x)[0]):
        print(key)
        print("{:10}: {}".format(color_to_nick(key)[1], color_identity[key]))

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

def burden_analysis(cardlist, split=False):
    cmc_breakdown = defaultdict(lambda: defaultdict(lambda: []))
    for card in cardlist:
        if card.properties["nominal"]["layout"] == "Split":
            if split is True:
                cmc = card.properties["left"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["left"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["left"]["mana_cost"], "{} (// {})".format(card.properties["left"]["name"], card.properties["right"]["name"]), card.actual["nominal"]["quantity"]))

                cmc = card.properties["right"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["right"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["right"]["mana_cost"], "{} (// {})".format(card.properties["right"]["name"], card.properties["left"]["name"]), card.actual["nominal"]["quantity"]))

            else:
                cmc = card.properties["nominal"]["cmc"]
                generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
                cmc_breakdown[cmc][generic_cmc].append((card.properties["nominal"]["mana_cost"], card.properties["nominal"]["name"], card.actual["nominal"]["quantity"]))
        elif card.properties["nominal"]["layout"] in ("Flip", "Transform"):
            cmc = card.properties["nominal"]["cmc"]
            generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
            cmc_breakdown[cmc][generic_cmc].append((card.properties["nominal"]["mana_cost"], "{} (// {})".format(card.get_repr("name"), card.get_repr("name", back=True)), card.actual["nominal"]["quantity"]))

        else:
            cmc = card.properties["nominal"]["cmc"]
            generic_cmc = generic_mana_strip(card.properties["nominal"]["mana_cost"])
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
    symbols_breakdown = defaultdict(lambda:0)

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


def cmc_breakdown(cardlist):
    raise NotImplementedError


def tag_breakdown(cardlist):
    raise NotImplementedError
