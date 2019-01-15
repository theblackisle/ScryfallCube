

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
    std = mode

    


    for card in cardlist:
        card.__getattribute__(std)

    raise NotImplementedError


def color_requirement_analysis(cardlist):
    raise NotImplementedError


def color_burden_analysis(cardlist):
    raise NotImplementedError


def cmc_breakdown(cardlist):
    raise NotImplementedError


def tag_breakdown(cardlist):
    raise NotImplementedError
