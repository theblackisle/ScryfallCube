

def concatenate_sheets(*cardlists):
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

    target = card.properties[mode]

    color_share = {'W':0, 'U':0, 'B':0, 'R':0, 'G':0, 'Colorless':0}
    color_identity = {'Colorless':0,
                      'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0,
                      'Azorius':0, 'Dimir':0, 'Rakdos':0, 'Gruul':0, 'selesnya':0,
                      'Orzhov':0, 'Golgari':0, 'Simic':0, 'Izzet':0, 'Boros':0,
                      'Esper':0, 'Grixis':0, 'Jund':0, 'Naya':0, 'Bant':0,
                      'Temur':0, 'Sultai':0, 'Abzan':0,	'Mardu':0, 'Jeskai':0,
                      'UBRG':0, 'BRGW':0, 'RGWU':0, 'GWUB':0, 'WUBR':0,
                      '5C':0}

    for card in cardlist:
        if len(target) == 0:
            color_share['Colorless'] += 1
            color_identity['Colorless'] += 1
        else:
            for char in target:
                color_share[char] += 1


    raise NotImplementedError


def color_requirement_analysis(cardlist):
    raise NotImplementedError


def color_burden_analysis(cardlist):
    raise NotImplementedError


def cmc_breakdown(cardlist):
    raise NotImplementedError


def tag_breakdown(cardlist):
    raise NotImplementedError
