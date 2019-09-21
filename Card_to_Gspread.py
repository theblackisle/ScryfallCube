from Converter import *

gspread_index = {
    'name': 0,  # str
    'mana_cost': 1,  # str
    'alt_cost': 2,  # str
    'cmc': 3,  # int
    'x_in_cmc': 4, # str
    'color': 5,  # tuple of str
    'actual_color': 6,  # tuple of str - ACTUAL
    'color_identity': 7,  # tuple of str
    'color_accessibility': 8,  # list of tuple of str - ACTUAL # accessibility는 원래가 actual한 것.
    'supertype': 9,  # list of str
    'actual_supertype': 10,  # list of str - ACTUAL
    'subtype': 11,  # list of str
    'actual_subtype': 12,  # list of str - ACTUAL
    'set': 13,  # str, upper()-ed
    'rarity': 14,  # str, title()-ed
    'layout': 15,  # str
    'power': 16,  # str
    'actual_power': 17,  # str - ACTUAL
    'power_tendency': 18,  # str - ACTUAL
    'toughness': 19,  # str
    'actual_toughness': 20,  # str - ACTUAL
    'toughness_tendency': 21,  # str - ACTUAL
    'loyalty': 22,  # str
    'actual_loyalty': 23,  # str - ACTUAL
    'loyalty_tendency': 24,  # str - ACTUAL
    'oracle': 25,  # str
    'buff': 26,  # list of str - ACTUAL
    'nerf': 27,  # list of str - ACTUAL
    'tags': 28,  # list of str - ACTUAL
    'usd': 29,  # float
    'crop_image': 30,  # str
    'quantity': 31  # int - ACTUAL
}

def prettify(card):
    # Card.card to displayable gspread row

    properties = card.properties

    prettylist = [""]*len(gspread_index)
    prettylist[gspread_index["buff"]] = '\n'.join(properties["nominal"]["buff"])
    prettylist[gspread_index["nerf"]] = '\n'.join(properties["nominal"]["nerf"])
    prettylist[gspread_index["tags"]] = '\n'.join(properties["nominal"]["tags"])
    prettylist[gspread_index["color_identity"]] = ''.join(properties["nominal"]["color_identity"])
    prettylist[gspread_index["set"]] = properties["nominal"]["set"]
    prettylist[gspread_index["rarity"]] = properties["nominal"]["rarity"]
    prettylist[gspread_index["usd"]] = "{:.2f}".format(properties["nominal"]["usd"])
    prettylist[gspread_index["layout"]] = properties["nominal"]["layout"]
    prettylist[gspread_index["quantity"]] = properties["nominal"]["quantity"]

    if properties["nominal"]["layout"] == 'Transform':
        prettylist[gspread_index["name"]] = '{}\n{}'.format(properties["side_A"]["name"],
                                                            properties["side_B"]["name"])
        prettylist[gspread_index["mana_cost"]] = symbolprettify(properties["nominal"]["mana_cost"])
        prettylist[gspread_index["alt_cost"]] = symbolprettify(properties["nominal"]["alt_cost"])
        prettylist[gspread_index["cmc"]] = properties["nominal"]["cmc"]
        prettylist[gspread_index["x_in_cmc"]] = properties["nominal"]["x_in_cmc"]
        prettylist[gspread_index["color"]] = '{}\n{}'.format(''.join(properties["side_A"]["color"]),
                                                             ''.join(properties["side_B"]["color"]))
        prettylist[gspread_index["actual_color"]] = '{}\n{}'.format(''.join(properties["side_A"]["actual_color"]),
                                                                    ''.join(properties["side_B"]["actual_color"]))
        prettylist[gspread_index["color_accessibility"]] = ','.join([''.join(item) for item in properties["nominal"]["color_accessibility"]])
        prettylist[gspread_index["supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["supertype"]),
                                                                 ' '.join(properties["side_B"]["supertype"]))
        prettylist[gspread_index["actual_supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_supertype"]),
                                                                        ' '.join(properties["side_B"]["actual_supertype"]))
        prettylist[gspread_index["subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["subtype"]),  # if properties["side_A"]["subtype"] != "" else ""),
                                                               ' '.join(properties["side_B"]["subtype"]))
        prettylist[gspread_index["actual_subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_subtype"]),
                                                                      ' '.join(properties["side_B"]["actual_subtype"]))
        prettylist[gspread_index["power"]] = '{}\n{}'.format(properties["side_A"]["power"],
                                                             properties["side_B"]["power"])
        prettylist[gspread_index["actual_power"]] = '{}\n{}'.format(properties["side_A"]["actual_power"],
                                                                    properties["side_B"]["actual_power"])
        prettylist[gspread_index["power_tendency"]] = '{}\n{}'.format(properties["side_A"]["power_tendency"],
                                                                      properties["side_B"]["power_tendency"])
        prettylist[gspread_index["toughness"]] = '{}\n{}'.format(properties["side_A"]["toughness"],
                                                                 properties["side_B"]["toughness"])
        prettylist[gspread_index["actual_toughness"]] = '{}\n{}'.format(properties["side_A"]["actual_toughness"],
                                                                        properties["side_B"]["actual_toughness"])
        prettylist[gspread_index["toughness_tendency"]] = '{}\n{}'.format(properties["side_A"]["toughness_tendency"],
                                                                          properties["side_B"]["toughness_tendency"])
        prettylist[gspread_index["loyalty"]] = '{}\n{}'.format(properties["side_A"]["loyalty"],
                                                               properties["side_B"]["loyalty"])
        prettylist[gspread_index["actual_loyalty"]] = '{}\n{}'.format(properties["side_A"]["actual_loyalty"],
                                                                      properties["side_B"]["actual_loyalty"])
        prettylist[gspread_index["loyalty_tendency"]] = '{}\n{}'.format(properties["side_A"]["loyalty_tendency"],
                                                                        properties["side_B"]["loyalty_tendency"])
        prettylist[gspread_index["oracle"]] = '{}\n// {}'.format(properties["side_A"]["oracle"],
                                                                 properties["side_B"]["oracle"])
        prettylist[gspread_index["crop_image"]] = '{}\n{}'.format(properties["side_A"]["crop_image"],
                                                                  properties["side_B"]["crop_image"])

    elif properties["nominal"]["layout"] == 'Flip':
        prettylist[gspread_index["name"]] = '{}\n{}'.format(properties["side_A"]["name"],
                                                            properties["side_B"]["name"])
        prettylist[gspread_index["mana_cost"]] = symbolprettify(properties["nominal"]["mana_cost"])
        prettylist[gspread_index["alt_cost"]] = symbolprettify(properties["nominal"]["alt_cost"])
        prettylist[gspread_index["cmc"]] = properties["nominal"]["cmc"]
        prettylist[gspread_index["x_in_cmc"]] = properties["nominal"]["x_in_cmc"]
        prettylist[gspread_index["color"]] = ''.join(properties["nominal"]["color"])
        prettylist[gspread_index["actual_color"]] = ''.join(properties["nominal"]["actual_color"])
        prettylist[gspread_index["color_accessibility"]] = ','.join([''.join(item) for item in properties["nominal"]["color_accessibility"]])
        prettylist[gspread_index["supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["supertype"]),
                                                                 ' '.join(properties["side_B"]["supertype"]))
        prettylist[gspread_index["actual_supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_supertype"]),
                                                                        ' '.join(properties["side_B"]["actual_supertype"]))
        prettylist[gspread_index["subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["subtype"]),  # if properties["side_A"]["subtype"] != "" else ""),
                                                               ' '.join(properties["side_B"]["subtype"]))
        prettylist[gspread_index["actual_subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_subtype"]),
                                                                      ' '.join(properties["side_B"]["actual_subtype"]))
        prettylist[gspread_index["power"]] = '{}\n{}'.format(properties["side_A"]["power"],
                                                             properties["side_B"]["power"])
        prettylist[gspread_index["actual_power"]] = '{}\n{}'.format(properties["side_A"]["actual_power"],
                                                                    properties["side_B"]["actual_power"])
        prettylist[gspread_index["power_tendency"]] = '{}\n{}'.format(properties["side_A"]["power_tendency"],
                                                                      properties["side_B"]["power_tendency"])
        prettylist[gspread_index["toughness"]] = '{}\n{}'.format(properties["side_A"]["toughness"],
                                                                 properties["side_B"]["toughness"])
        prettylist[gspread_index["actual_toughness"]] = '{}\n{}'.format(properties["side_A"]["actual_toughness"],
                                                                        properties["side_B"]["actual_toughness"])
        prettylist[gspread_index["toughness_tendency"]] = '{}\n{}'.format(properties["side_A"]["toughness_tendency"],
                                                                          properties["side_B"]["toughness_tendency"])
        # prettylist[gspread_index["loyalty"]] = ''  # no flip planeswalker (지금까지는)
        prettylist[gspread_index["oracle"]] = '{}\n// {}'.format(properties["side_A"]["oracle"],
                                                                 properties["side_B"]["oracle"])
        prettylist[gspread_index["crop_image"]] = properties["nominal"]["crop_image"]

    elif properties["nominal"]["layout"] == 'Split':
        prettylist[gspread_index["name"]] = '{}\n{}\n{}'.format(properties["nominal"]["name"], properties["side_A"]["name"], properties["side_B"]["name"])
        prettylist[gspread_index["mana_cost"]] = '{}\n{}\n{}'.format(symbolprettify(properties["nominal"]["mana_cost"]),
                                                                     symbolprettify(properties["side_A"]["mana_cost"]),
                                                                     symbolprettify(properties["side_B"]["mana_cost"]))
        prettylist[gspread_index["alt_cost"]] = '{}\n{}\n{}'.format(symbolprettify(properties["nominal"]["alt_cost"]),
                                                                    symbolprettify(properties["side_A"]["alt_cost"]),
                                                                    symbolprettify(properties["side_B"]["alt_cost"]))
        prettylist[gspread_index["cmc"]] = '{}\n{}\n{}'.format(symbolprettify(properties["nominal"]["cmc"]),
                                                               symbolprettify(properties["side_A"]["cmc"]),
                                                               symbolprettify(properties["side_B"]["cmc"]))
        prettylist[gspread_index["x_in_cmc"]] = '{}\n{}\n{}'.format(symbolprettify(properties["nominal"]["x_in_cmc"]),
                                                                    symbolprettify(properties["side_A"]["x_in_cmc"]),
                                                                    symbolprettify(properties["side_B"]["x_in_cmc"]))
        prettylist[gspread_index["color"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["color"]),
                                                                 ''.join(properties["side_A"]["color"]),
                                                                 ''.join(properties["side_B"]["color"]))
        prettylist[gspread_index["actual_color"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["actual_color"]),
                                                                        ''.join(properties["side_A"]["actual_color"]),
                                                                        ''.join(properties["side_B"]["actual_color"]))
        prettylist[gspread_index["color_accessibility"]] = '{}\n{}\n{}'.format(','.join([''.join(item) for item in properties["nominal"]["color_accessibility"]]),
                                                                               ','.join([''.join(item) for item in properties["side_A"]["color_accessibility"]]),
                                                                               ','.join([''.join(item) for item in properties["side_B"]["color_accessibility"]]))  # if properties["side_B"]["color_accessibility"] != "" else "")
        prettylist[gspread_index["supertype"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["supertype"]),
                                                                     ''.join(properties["side_A"]["supertype"]),
                                                                     ''.join(properties["side_B"]["supertype"]))
        prettylist[gspread_index["actual_supertype"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["actual_supertype"]),
                                                                            ''.join(properties["side_A"]["actual_supertype"]),
                                                                            ''.join(properties["side_B"]["actual_supertype"]))
        prettylist[gspread_index["subtype"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["subtype"]),
                                                                   ''.join(properties["side_A"]["subtype"]),
                                                                   ''.join(properties["side_B"]["subtype"]))
        prettylist[gspread_index["actual_subtype"]] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["actual_subtype"]),
                                                                          ''.join(properties["side_A"]["actual_subtype"]),
                                                                          ''.join(properties["side_B"]["actual_subtype"]))
        # prettylist[gspread_index["power"]] = ""
        # prettylist[gspread_index["toughness"]] = ""
        # prettylist[gspread_index["loyalty"]] = ""  # No split creature nor planeswalker till now (지금까지는)
        prettylist[gspread_index["oracle"]] = '{}\n// {}'.format(properties["side_A"]["oracle"],
                                                                 properties["side_B"]["oracle"])
        prettylist[gspread_index["crop_image"]] = properties["nominal"]["crop_image"]

    elif properties["nominal"]["layout"] == 'Adventure':
        prettylist[gspread_index["name"]] = '{}\n{}'.format(properties["side_A"]["name"],
                                                            properties["side_B"]["name"])
        prettylist[gspread_index["mana_cost"]] = '{}\n{}'.format(symbolprettify(properties["side_A"]["mana_cost"]),
                                                                 symbolprettify(properties["side_B"]["mana_cost"]))
        prettylist[gspread_index["alt_cost"]] = '{}\n{}'.format(symbolprettify(properties["side_A"]["alt_cost"]),
                                                                symbolprettify(properties["side_B"]["alt_cost"]))
        prettylist[gspread_index["cmc"]] = '{}\n{}'.format(symbolprettify(properties["side_A"]["cmc"]),
                                                           symbolprettify(properties["side_B"]["cmc"]))
        prettylist[gspread_index["x_in_cmc"]] = '{}\n{}'.format(symbolprettify(properties["side_A"]["x_in_cmc"]),
                                                                symbolprettify(properties["side_B"]["x_in_cmc"]))
        prettylist[gspread_index["color"]] = ''.join(properties["nominal"]["color"])
        prettylist[gspread_index["actual_color"]] = ''.join(properties["nominal"]["actual_color"])
        prettylist[gspread_index["color_accessibility"]] = ','.join([''.join(item) for item in properties["nominal"]["color_accessibility"]])
        # 지금까지는 side 색이 다른 adventure카드 없음
        prettylist[gspread_index["supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["supertype"]),
                                                                 ' '.join(properties["side_B"]["supertype"]))
        prettylist[gspread_index["actual_supertype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_supertype"]),
                                                                        ' '.join(properties["side_B"]["actual_supertype"]))
        prettylist[gspread_index["subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["subtype"]),  # if properties["side_A"]["subtype"] != "" else ""),
                                                               ' '.join(properties["side_B"]["subtype"]))
        prettylist[gspread_index["actual_subtype"]] = '{}\n{}'.format(' '.join(properties["side_A"]["actual_subtype"]),
                                                                      ' '.join(properties["side_B"]["actual_subtype"]))
        prettylist[gspread_index["power"]] = '{}\n{}'.format(properties["side_A"]["power"],
                                                             properties["side_B"]["power"])
        prettylist[gspread_index["actual_power"]] = '{}\n{}'.format(properties["side_A"]["actual_power"],
                                                                    properties["side_B"]["actual_power"])
        prettylist[gspread_index["power_tendency"]] = '{}\n{}'.format(properties["side_A"]["power_tendency"],
                                                                      properties["side_B"]["power_tendency"])
        prettylist[gspread_index["toughness"]] = '{}\n{}'.format(properties["side_A"]["toughness"],
                                                                 properties["side_B"]["toughness"])
        prettylist[gspread_index["actual_toughness"]] = '{}\n{}'.format(properties["side_A"]["actual_toughness"],
                                                                        properties["side_B"]["actual_toughness"])
        prettylist[gspread_index["toughness_tendency"]] = '{}\n{}'.format(properties["side_A"]["toughness_tendency"],
                                                                          properties["side_B"]["toughness_tendency"])
        # prettylist[gspread_index["loyalty"]] = ''  # no Adventure planeswalker (지금까지는)
        prettylist[gspread_index["oracle"]] = '{}\n// {}'.format(properties["side_A"]["oracle"],
                                                                 properties["side_B"]["oracle"])
        prettylist[gspread_index["crop_image"]] = properties["nominal"]["crop_image"]
    else:
        prettylist[gspread_index["mana_cost"]] = symbolprettify(properties["nominal"]["mana_cost"])
        prettylist[gspread_index["alt_cost"]] = symbolprettify(properties["nominal"]["alt_cost"])
        prettylist[gspread_index["cmc"]] = properties["nominal"]["cmc"]
        prettylist[gspread_index["x_in_cmc"]] = properties["nominal"]["x_in_cmc"]
        prettylist[gspread_index["color"]] = ''.join(properties["nominal"]["color"])
        prettylist[gspread_index["actual_color"]] = ''.join(properties["nominal"]["actual_color"])
        prettylist[gspread_index["color_accessibility"]] = ','.join([''.join(item) for item in properties["nominal"]["color_accessibility"]])
        prettylist[gspread_index["supertype"]] = ' '.join(properties["nominal"]["supertype"])
        prettylist[gspread_index["actual_supertype"]] = ' '.join(properties["nominal"]["actual_supertype"])
        prettylist[gspread_index["subtype"]] = ' '.join(properties["nominal"]["subtype"])
        prettylist[gspread_index["actual_subtype"]] = ' '.join(properties["nominal"]["actual_subtype"])
        prettylist[gspread_index["power"]] = properties["nominal"]["power"]
        prettylist[gspread_index["actual_power"]] = properties["nominal"]["actual_power"]
        prettylist[gspread_index["power_tendency"]] = properties["nominal"]["power_tendency"]
        prettylist[gspread_index["toughness"]] = properties["nominal"]["toughness"]
        prettylist[gspread_index["actual_toughness"]] = properties["nominal"]["actual_toughness"]
        prettylist[gspread_index["toughness_tendency"]] = properties["nominal"]["toughness_tendency"]
        prettylist[gspread_index["loyalty"]] = properties["nominal"]["loyalty"]
        prettylist[gspread_index["actual_loyalty"]] = properties["nominal"]["actual_loyalty"]
        prettylist[gspread_index["loyalty_tendency"]] = properties["nominal"]["loyalty_tendency"]
        prettylist[gspread_index["oracle"]] = properties["nominal"]["oracle"]
        prettylist[gspread_index["crop_image"]] = properties["nominal"]["crop_image"]

    return prettylist


def uglify(cardlist):
    """gspread row to internal Card.Card edible data"""

    uglydict = {'nominal': {}}

    uglydict["nominal"]["buff"] = (cardlist[gspread_index["buff"]].split("\n")) if cardlist[gspread_index["buff"]] != "" else []  # buff(=list)
    uglydict["nominal"]["nerf"] = (cardlist[gspread_index["nerf"]].split("\n")) if cardlist[gspread_index["nerf"]] != "" else []  # nerf(=list)
    uglydict["nominal"]["tags"] = (cardlist[gspread_index["tags"]].split("\n")) if cardlist[gspread_index["tags"]] != "" else []  # tags(=list)

    uglydict["nominal"]["color_identity"] = tuple(cardlist[gspread_index["color_identity"]]) if cardlist[gspread_index["color_identity"]] != "C" else ()  # color_identity(=tuple)
    uglydict["nominal"]["set"] = cardlist[gspread_index["set"]]  # set(=str, upper()-ed)
    uglydict["nominal"]["rarity"] = cardlist[gspread_index["rarity"]]  # rarity(=str, title()-ed)
    uglydict["nominal"]["usd"] = float(cardlist[gspread_index["usd"]])  # usd(=float)
    uglydict["nominal"]["quantity"] = int(cardlist[gspread_index["quantity"]])  # quantity(=int)

    uglydict["nominal"]["layout"] = cardlist[gspread_index["layout"]]  # layout(=str)
    if uglydict["nominal"]["layout"] == 'Transform':
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}

        split_temp = cardlist[gspread_index["name"]].split("\n// ")
        uglydict["side_A"]["name"] = split_temp[0]  # name(=str)
        uglydict["side_B"]["name"] = split_temp[1]
        uglydict["nominal"]["name"] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["mana_cost"]], 1)
        uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["cmc"]], 1)
        uglydict["nominal"]["cmc"] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict["nominal"]["cmc"] = split_temp[1]

        split_temp = cardlist[gspread_index["color"]].split("\n")
        uglydict["side_A"]["color"] = tuple(split_temp[0]) if split_temp[0] != "C" else ()  # color(=tuple)
        uglydict["side_B"]["color"] = tuple(split_temp[1]) if split_temp[1] != "C" else ()

        split_temp = re.split(r',(?=[\-\+>])', cardlist[gspread_index["color_accessibility"]], 1)
        uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[0].split(',')]  # color accessibility(=list of tuple)
        if len(split_temp) > 1:
            uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[1].split(',')]

        split_temp = cardlist[gspread_index["supertype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["side_A"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # supertype(=list)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["supertype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_B"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["supertype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["subtype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["side_A"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # subtype(=tuple)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["subtype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_B"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["subtype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["power"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["side_A"]["power"] = split_subtemp[0]  # power(=str)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["power"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_B"]["power"] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["power"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["toughness"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["side_A"]["toughness"] = split_subtemp[0]  # toughness(=str)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["toughness"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_B"]["toughness"] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["toughness"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["loyalty"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["side_A"]["loyalty"] = split_subtemp[0]  # loyalty(=str)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["loyalty"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_B"]["loyalty"] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["loyalty"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["oracle"]].split("\n// ")
        uglydict["side_A"]["oracle"] = split_temp[0]  # oracle(=str)
        uglydict["side_B"]["oracle"] = split_temp[1]

        split_temp = cardlist[gspread_index["crop_image"]].split("\n")
        uglydict["side_A"]["crop_image"] = split_temp[0]  # crop_image(=str, url)
        uglydict["side_B"]["crop_image"] = split_temp[1]

    elif uglydict["nominal"]["layout"] == 'Flip':
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}

        split_temp = cardlist[gspread_index["name"]].split("\n// ")
        uglydict["side_A"]["name"] = split_temp[0]  # name(=str)
        uglydict["side_B"]["name"] = split_temp[1]
        uglydict["nominal"]["name"] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["mana_cost"]], 1)
        uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["cmc"]], 1)
        uglydict["nominal"]["cmc"] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict["nominal"]["cmc"] = split_temp[1]

        uglydict["nominal"]["color"] = tuple(cardlist[gspread_index["color"]]) if cardlist[gspread_index["color"]] != "C" else ()  # color(=tuple)

        split_temp = re.split(r',(?=[\-\+>])', cardlist[gspread_index["color_accessibility"]], 1)
        uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[0].split(',')]  # color accessibility(=list of tuple)
        if len(split_temp) > 1:
            uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[1].split(',')]

        split_temp = cardlist[gspread_index["supertype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["side_A"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # supertype(=list)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["supertype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_B"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["supertype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["subtype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["side_A"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # subtype(=list)
        if len(split_subtemp) > 1:
         uglydict["side_A"]["subtype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_B"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["subtype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["power"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["side_A"]["power"] = split_subtemp[0]  # power(=str)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["power"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_B"]["power"] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["power"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["toughness"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["side_A"]["toughness"] = split_subtemp[0]  # toughness(=str)
        if len(split_subtemp) > 1:
            uglydict["side_A"]["toughness"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_B"]["toughness"] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["toughness"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["oracle"]].split("\n// ")
        uglydict["side_A"]["oracle"] = split_temp[0]  # oracle(=str)
        uglydict["side_B"]["oracle"] = split_temp[1]

        uglydict["nominal"]["crop_image"] = cardlist[gspread_index["crop_image"]]  # crop_image(=str, url)

    elif uglydict["nominal"]["layout"] == 'Split':
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}
        uglydict["side_A"] = {}
        uglydict["side_B"] = {}

        split_temp = cardlist[gspread_index["name"]].split("\n// ")
        uglydict["side_A"]["name"] = split_temp[0]  # name(=str)
        uglydict["side_B"]["name"] = split_temp[1]
        uglydict["nominal"]["name"] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = cardlist[gspread_index["mana_cost"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["nominal"]["mana_cost"] = symbolprettify(split_subtemp[0], "reverse")  # mana_cost(=str)
        if len(split_subtemp) > 1:
            uglydict["nominal"]["mana_cost"] = symbolprettify(split_subtemp[1], "reverse")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_A"]["mana_cost"] = symbolprettify(split_subtemp[0], "reverse")
        if len(split_subtemp) > 1:
            uglydict["side_A"]["mana_cost"] = symbolprettify(split_subtemp[1], "reverse")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[2], 1)
        uglydict["side_B"]["mana_cost"] = symbolprettify(split_subtemp[0], "reverse")
        if len(split_subtemp) > 1:
            uglydict["side_B"]["mana_cost"] = symbolprettify(split_subtemp[1], "reverse")

        split_temp = cardlist[gspread_index["cmc"]].split("\n")
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[0], 1)
        uglydict["nominal"]["cmc"] = int(split_subtemp[0])  # CMC(=int)
        if len(split_subtemp) > 1:
            uglydict["nominal"]["cmc"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_A"]["cmc"] = int(split_subtemp[0])
        if len(split_subtemp) > 1:
            uglydict["side_A"]["cmc"] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+>])', split_temp[2], 1)
        uglydict["side_B"]["cmc"] = int(split_subtemp[0])
        if len(split_subtemp) > 1:
            uglydict["side_B"]["cmc"] = split_subtemp[1]

        split_temp = cardlist[gspread_index["color"]].split("\n")
        uglydict["nominal"]["color"] = tuple(split_temp[0]) if split_temp[0] != "C" else ()  # color(=tuple)
        uglydict["side_A"]["color"] = tuple(split_temp[1]) if split_temp[1] != "C" else ()
        uglydict["side_B"]["color"] = tuple(split_temp[2]) if split_temp[2] != "C" else ()

        split_temp = cardlist[gspread_index["color_accessibility"]].split("\n")
        split_subtemp = re.split(r',(?=[\-\+>])', split_temp[0], 1)
        uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_subtemp[0].split(',')]  # color accessibility(=list of tuple)
        if len(split_subtemp) > 1:
            uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_subtemp[1].split(',')]
        split_subtemp = re.split(r',(?=[\-\+>])', split_temp[1], 1)
        uglydict["side_A"]["color_accessibility"] = [tuple(item) for item in split_subtemp[0].split(',')]
        if len(split_subtemp) > 1:
            uglydict["side_A"]["color_accessibility"] = [tuple(item) for item in split_subtemp[1].split(',')]
        split_subtemp = re.split(r',(?=[\-\+>])', split_temp[2], 1)
        uglydict["side_B"]["color_accessibility"] = [tuple(item) for item in split_subtemp[0].split(',')]
        if len(split_subtemp) > 1:
            uglydict["side_B"]["color_accessibility"] = [tuple(item) for item in split_subtemp[1].split(',')]

        split_temp = cardlist[gspread_index["supertype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["nominal"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # supertype(=list)
        if len(split_subtemp) > 1:
            uglydict["nominal"]["supertype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_A"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_A"]["supertype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[2], 1)
        uglydict["side_B"]["supertype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["supertype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["subtype"]].split("\n")
        split_subtemp = re.split(r'[\-\+>]', split_temp[0], 1)
        uglydict["nominal"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []  # subtype(=list)
        if len(split_subtemp) > 1:
            uglydict["nominal"]["subtype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[1], 1)
        uglydict["side_A"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_A"]["subtype"] = split_subtemp[1].split(' ')
        split_subtemp = re.split(r'[\-\+>]', split_temp[2], 1)
        uglydict["side_B"]["subtype"] = split_subtemp[0].split(' ') if split_subtemp[0] != "" else []
        if len(split_subtemp) > 1:
            uglydict["side_B"]["subtype"] = split_subtemp[1].split(' ')

        split_temp = cardlist[gspread_index["oracle"]].split("\n// ")
        uglydict["side_A"]["oracle"] = split_temp[0]  # oracle(=str)
        uglydict["side_B"]["oracle"] = split_temp[1]

        uglydict["nominal"]["crop_image"] = cardlist[gspread_index["crop_image"]]  # crop_image(=str, url)

    else:
        uglydict["nominal"]["name"] = cardlist[gspread_index["name"]]  # name(=str)

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["mana_cost"]], 1)
        uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["mana_cost"] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["cmc"]], 1)
        uglydict["nominal"]["cmc"] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict["nominal"]["cmc"] = split_temp[1]

        uglydict["nominal"]["color"] = tuple(cardlist[gspread_index["color"]]) if cardlist[gspread_index["color"]] != "C" else ()  # color(=tuple)

        split_temp = re.split(r',(?=[\-\+>])', cardlist[gspread_index["color_accessibility"]], 1)
        uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[0].split(',')]  # color accessibility(=list of tuple)
        if len(split_temp) > 1:
            uglydict["nominal"]["color_accessibility"] = [tuple(item) for item in split_temp[1].split(',')]

        split_temp = re.split(r'[\-\+>]', cardlist[gspread_index["supertype"]], 1)
        uglydict["nominal"]["supertype"] = split_temp[0].split(' ') if split_temp[0] != "" else []  # supertype(=list)
        if len(split_temp) > 1:
            uglydict["nominal"]["supertype"] = split_temp[1].split(' ')

        split_temp = re.split(r'[\-\+>]', cardlist[gspread_index["subtype"]], 1)
        uglydict["nominal"]["subtype"] = split_temp[0].split(' ') if split_temp[0] != "" else []  # subtype(=list)
        if len(split_temp) > 1:
            uglydict["nominal"]["subtype"] = split_temp[1].split(' ')

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["power"]], 1)
        uglydict["nominal"]["power"] = split_temp[0]  # power(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["power"] = split_temp[1]

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["toughness"]], 1)
        uglydict["nominal"]["toughness"] = split_temp[0]  # toughness(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["toughness"] = split_temp[1]

        split_temp = re.split(r'(?=[\-\+>])', cardlist[gspread_index["loyalty"]], 1)
        uglydict["nominal"]["loyalty"] = split_temp[0]  # loyalty(=str)
        if len(split_temp) > 1:
            uglydict["nominal"]["loyalty"] = split_temp[1]

        uglydict["nominal"]["oracle"] = cardlist[gspread_index["oracle"]]
        uglydict["nominal"]["crop_image"] = cardlist[gspread_index["crop_image"]]

    return uglydict


while __name__ == '__main__':
    print('{}{}'.format(' '.join(""), "12345"))
    print('{}{}'.format(' '.join(['1','2','3','4','5']), "12345"))
    print(' 2345')
    break