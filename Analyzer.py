from collections import defaultdict
from Converter import color_to_nick

def concatenate_list(*cardlists):
    """
    Card list들을 받아서 하나의 list로 합치고 중복되는 카드를 삭제함.

    Args:
        *sheets (list): args of lists of Cards
    """

    total_cards = 0
    dupl_cards = 0
    seen = set()
    unique_sheet = []
    for cardlist in cardlists:
        total_cards += len(cardlist)
        for card in cardlist:
            if card not in seen:
                seen.add(card)
                unique_sheet.append(card)
            else:
                print(card, "is duplicated.")
                dupl_cards += 1

    print("%s cards are collected." % total_cards)
    print("%s duplicated cards are removed from list." % dupl_cards)
    print("%s cards in list by now." % len(unique_sheet))
    return unique_sheet


def color_breakdown(cardlist, mode="color"):

    color_share = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0, 'C': 0}
    color_identity = defaultdict(lambda: 0)

    for card in cardlist:
        target = card.properties[mode]
        color_identity[target] += 1
        if len(target) == 0:
            color_share['C'] += 1
        else:
            for char in target:
                color_share[char] += 1

    if mode == 'color':
        pass

    print("\nColor_breakdown:")
    for key in sorted(color_identity.keys(), key=lambda color: color_to_nick(color)[0]):
        print("{:10}: {}".format(color_to_nick(key)[1], color_identity[key]))

    print("\nColor_appearance:")
    for key in color_share.keys():
        print("{}: {:3} of {}, total {:5.2f} %".format(key, color_share[key], len(cardlist), 100*color_share[key]/len(cardlist)))
    print("")


def color_requirement_analysis(cardlist):
    raise NotImplementedError


def color_burden_analysis(cardlist):
    raise NotImplementedError


def cmc_breakdown(cardlist):
    raise NotImplementedError


def tag_breakdown(cardlist):
    raise NotImplementedError
