from Converter import *
from itertools import combinations

def mana_to_accessibility(mana):
    """
    :param mana: uglyfied mana cost from Scryfall JSON
    :return: (list of tuples) acessible color set
    """

    local_accessibility = []
    total_accessibility = set()
    colored_cmc = re.findall(r'{W/U}|{U/B}|{B/R}|{R/G}|{G/W}|{W/B}|{B/G}|{G/U}|{U/R}|{R/W}|{2/W}|{2/U}|{2/B}|{2/R}|{2/G}|{W/P}|{U/P}|{B/P}|{R/P}|{G/P}|{W}|{U}|{B}|{R}|{G}|{C}', mana)
    for symbol in colored_cmc:
        if re.findall(r'{W/U}', symbol): local_accessibility.append(('W', 'U'))
        if re.findall(r'{U/B}', symbol): local_accessibility.append(('U', 'B'))
        if re.findall(r'{B/R}', symbol): local_accessibility.append(('B', 'R'))
        if re.findall(r'{R/G}', symbol): local_accessibility.append(('R', 'G'))
        if re.findall(r'{G/W}', symbol): local_accessibility.append(('G', 'W'))
        if re.findall(r'{W/B}', symbol): local_accessibility.append(('W', 'B'))
        if re.findall(r'{B/G}', symbol): local_accessibility.append(('B', 'G'))
        if re.findall(r'{G/U}', symbol): local_accessibility.append(('G', 'U'))
        if re.findall(r'{U/R}', symbol): local_accessibility.append(('U', 'R'))
        if re.findall(r'{R/W}', symbol): local_accessibility.append(('R', 'W'))
        if re.findall(r'{W}', symbol): local_accessibility.append(('W'))
        if re.findall(r'{U}', symbol): local_accessibility.append(('U'))
        if re.findall(r'{B}', symbol): local_accessibility.append(('B'))
        if re.findall(r'{R}', symbol): local_accessibility.append(('R'))
        if re.findall(r'{G}', symbol): local_accessibility.append(('G'))
        if re.findall(r'{C}', symbol): local_accessibility.append(('C'))
        # {P/R},{2/R}등은 accessibility를 제한하지 않으므로 계산안해도 무방

    for item in local_accessibility:
        if len(total_accessibility) == 0:
            total_accessibility = set([frozenset([j]) for j in item])
        else:
            set_product = [frozenset(set(i) | set([k])) for i in total_accessibility for k in item]
            total_accessibility = set(set_product)

    redundant = set()
    for (i, j) in combinations(total_accessibility, 2):
        if i.issuperset(j):
            redundant.add(i)
        if j.issuperset(i):
            redundant.add(j)

    total_accessibility = total_accessibility - redundant
    if len(total_accessibility) == 0:
        return '∅',

    total_accessibility = [cyclicOrder(item) for item in total_accessibility]
    total_accessibility = sorted(total_accessibility, key=lambda x: color_to_nick(tuple(x))[0])
    return total_accessibility


def mana_to_cmc(mana):
    """
    :param mana: uglyfied mana cost from Scryfall JSON
    :return: cmc(int) is cmc calculated for param
    """
    if mana is "":
        return 0

    generic = re.findall(r'{\d+}', mana)
    if len(generic) != 0:
        generic_cmc = int(re.sub(r'{|}', '', generic[0]))
    else:
        generic_cmc = 0

    colored_cmc = len(re.findall(r'{W/U}|{U/B}|{B/R}|{R/G}|{G/W}|{W/B}|{B/G}|{G/U}|{U/R}|{R/W}|{2/W}|{2/U}|{2/B}|{2/R}|{2/G}|{W/P}|{U/P}|{B/P}|{R/P}|{G/P}|{W}|{U}|{B}|{R}|{G}|{C}', mana))

    return generic_cmc + colored_cmc


def mana_sum(mana1, mana2):
    """
    :param mana1, mana2: uglyfied mana cost from Scryfall JSON
    :return: sum(str) is mana added
    """
    mana = mana1+mana2
    x = re.findall(r'{X}', mana)
    x_sum = ""
    for item in x:
        x_sum += item

    generic = re.findall(r'{\d+}', mana)
    generic_sum = 0
    if len(generic) > 0:
        for item in generic:
            generic_sum += int(re.sub(r'{|}', '', item))
        generic_sum = "{%d}" % generic_sum
    if len(generic) == 0 or (generic_sum == "{0}" and len(x) > 0):
        generic_sum = ""

    # 아직 hybrid, twobrid, pyrexian mana를 color sort할 필요가 있는 카드(=split)가 mtg 내에 없음. 미구현
    hybrid = re.findall(r'{W/U}|{U/B}|{B/R}|{R/G}|{G/W}|{W/B}|{B/G}|{G/U}|{U/R}|{R/W}|{2/W}|{2/U}|{2/B}|{2/R}|{2/G}|{W/P}|{U/P}|{B/P}|{R/P}|{G/P}|{C}', mana)
    hybrid_sum = ""
    for item in hybrid:
        hybrid_sum += item

    color = {}
    color["W"] = re.findall(r'{W}', mana)
    color["U"] = re.findall(r'{U}', mana)
    color["B"] = re.findall(r'{B}', mana)
    color["R"] = re.findall(r'{R}', mana)
    color["G"] = re.findall(r'{G}', mana)
    present_color = cyclicOrder([item for item in ('W', 'U', 'B', 'R', 'G') if len(color[item]) > 0])

    color_sum = ""
    for item in present_color:
        color_sum += ("{%s}" % item) * len(color[item])

    return x_sum + generic_sum + hybrid_sum + color_sum


def mana_to_color(mana):
    color = {}
    color["W"] = re.findall(r'{W}|{2/W}|{W/P}|{W/U}|{G/W}|{W/B}|{R/W}', mana)
    color["U"] = re.findall(r'{U}|{2/U}|{U/P}|{W/U}|{U/B}|{G/U}|{U/R}', mana)
    color["B"] = re.findall(r'{B}|{2/B}|{B/P}|{U/B}|{B/R}|{W/B}|{B/G}', mana)
    color["R"] = re.findall(r'{R}|{2/R}|{R/P}|{B/R}|{R/G}|{U/R}|{R/W}', mana)
    color["G"] = re.findall(r'{G}|{2/G}|{G/P}|{R/G}|{G/W}|{B/G}|{G/U}', mana)
    return cyclicOrder([item for item in ('W', 'U', 'B', 'R', 'G') if len(color[item]) > 0])


def generic_mana_strip(mana):
    generic = re.findall(r'{\d+}', mana)
    if len(generic) != 0:
        generic_cmc = int(re.sub(r'{|}', '', generic[0]))
    else:
        generic_cmc = 0

    return generic_cmc


def alt_cost_finder(oracle, mode='finder'):
    pattern = '\d+'
    r = re.compile(pattern)
    re.findall(r'')


    re.findall(r'(?:(?:\S+)(?:(?:>=)|(?:<=)|(?:!=)|(?:!:)|[=:><])(?:\S+))|(?:AND|OR|EXCEPT)', oracle)
    if mode is 'finder':
        return

def is_empty_properties(value):
    if value in ("", )