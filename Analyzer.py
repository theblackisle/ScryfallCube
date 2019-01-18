from collections import defaultdict
from Converter import color_to_nick, symbolprettify
import re

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
    for key in sorted(color_identity.keys(), key=lambda color_key: color_to_nick(color_key)[0]):
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



def burden_analysis(cardlist):
    cmc_breakdown = defaultdict(lambda: defaultdict(lambda: []))
    for card in cardlist:
        cmc = card.properties["cmc"]
        print(card.properties["name"], card.properties["mana_cost"])
        generic = re.findall(r'{\d+}', card.properties["mana_cost"])
        if len(generic) != 0:
            generic_cmc = int(re.sub(r'{|}', '', generic[0]))
        else:
            generic_cmc = 0
        cmc_breakdown[cmc][generic_cmc].append( (card.properties["mana_cost"], card.properties["name"]) )

    total_color_burden = 0
    for i in sorted(cmc_breakdown.keys()):
        print("CMC %d" % i)
        local_color_burden = 0
        CMC_card_length = 0
        for j in sorted(cmc_breakdown[i].keys(), reverse=True):
            color_burden = 100*(i-j)/i if i != 0 else 0
            CMC_card_length += len(cmc_breakdown[i][j])
            local_color_burden += color_burden * len(cmc_breakdown[i][j])
            total_color_burden += local_color_burden
            print(" '{}' color burden({:2.1f}% of total CMC): {} card(s)".format(i-j, color_burden, len(cmc_breakdown[i][j])))
            for k in sorted(cmc_breakdown[i][j]):
                print("   %s: %s" % (symbolprettify(k[0]), k[1]))
        print("Average color burden in CMC {} is: {:2.2f}%\n".format(i, local_color_burden/CMC_card_length))

    print("Total average color burden is: {:2.2f}%\n".format(total_color_burden/len(cardlist)))

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
