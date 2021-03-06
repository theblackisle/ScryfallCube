from typing import Set, Any, Union

import ScryfallIO
import Card_to_Gspread
from Calculator import *

from collections import defaultdict

all_properties = {
    "name",
    "mana_cost",
    "alt_cost",
    "cmc",
    "x_in_cmc",
    "color",
    "actual_color",
    "color_identity",
    "color_accessibility",
    "supertype",
    "actual_supertype",
    "subtype",
    "actual_subtype",
    "set",
    "rarity",
    "layout",
    "power",
    "actual_power",
    "power_tendency",
    "toughness",
    "actual_toughness",
    "toughness_tendency",
    "loyalty",
    "actual_loyalty",
    "loyalty_tendency",
    "oracle",
    "buff",
    "nerf",
    "tags",
    "usd",
    "crop_image",
    "quantity",
}

special_layout = ("Transform", "Flip", "Split", "Adventure")
special_properties = {'name', 'oracle',
                      'mana_cost', 'alt_cost', 'cmc', 'x_in_cmc',
                      'color', 'actual_color', 'color_accessibility',
                      'supertype', 'actual_supertype', 'subtype', 'actual_subtype',
                      'power', 'actual_power', 'power_tendency',
                      'toughness', 'actual_toughness', 'toughness_tendency',
                      'loyalty', 'actual_loyalty', 'loyalty_tendency',
                      'crop_image'}

dangerous_properties = dict()
dangerous_properties["Transform"] = special_properties - {'mana_cost', 'alt_cost', 'cmc', 'x_in_cmc',
                                                             'color_accessibility'}
dangerous_properties["Flip"] = special_properties - {'mana_cost', 'alt_cost', 'cmc', 'x_in_cmc',
                                                     'color_accessibility', 'color', 'actual_color',
                                                     'loyalty', 'actual_loyalty', 'loyalty_tendency',
                                                     'crop_image'}
dangerous_properties["Split"] = special_properties - {"power", "actual_power", "power_tendency",
                                                      "toughness", "actual_toughness", "toughness_tendency",
                                                      'crop_image'}
dangerous_properties["Adventure"] = special_properties - {'color_accessibility', 'color', 'actual_color',
                                                          'loyalty', 'actual_loyalty', 'loyalty_tendency',
                                                          'crop_image'}


class Card():
    def __init__(self, data=None, reference="Scryfall", mode='default'):
        if data is None:  # empty initialization
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))  # layered data from a cube maker

        elif reference == "Gspread":  # data is Google spreadsheet row
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))

            data = Card_to_Gspread.uglify(data)  # "uglified"
            for first_key in data.keys():
                for second_key in data[first_key].keys():
                    for third_key in data[first_key][second_key].keys():
                        if data[first_key][second_key][third_key] != "":
                            getattr(self, first_key)[second_key][third_key] = data[first_key][second_key][third_key]

        elif reference == "Scryfall":  # data is JSON from Scryfall
            '''
            type of properties
            int = cmc, quantity
            float = usd
            tuple = color, color_identity
            string = set, rarity, layout
            list of tuples = color_accessibility
            list of strings = supertype, subtype, buff, nerf, tags
            int/string = power, toughness, loyalty
        
            ☆properties constant regardless to layout
            color_identity
            set
            rarity
            usd
            layout
            
            ☆properties only in 'nominal(=nominal)' dict
            color_identity
            set
            rarity
            usd
            layout
            supertype
            subtype
            
            ☆properties only in actual 'dict'
            buff
            nerf
            tags
            quantity
            '''
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.properties["nominal"]["buff"] = []
            self.properties["nominal"]["nerf"] = []  # hate for color, tribe, and else ...
            self.properties["nominal"]["tags"] = []  # fixing, infect, selfmill, big, small, ... ...
            self.properties["nominal"]["color_identity"] = tuple(data["color_identity"])  # split 카드의 활성화비용 identity..이런건 무시하기로.
            self.properties["nominal"]["set"] = data["set"].upper()
            if mode.lower() == 'cardkingdom':
                self.properties["nominal"]["set"] = data["set_name"]
            self.properties["nominal"]["rarity"] = data["rarity"].title()
            self.properties["nominal"]["usd"] = float(data.get('usd', 0))
            self.properties["nominal"]["layout"] = data["layout"].title()
            self.properties["nominal"]["quantity"] = 1

            if self.properties["nominal"]["layout"] == 'Transform':
                # Transform: nominal = side_A = 앞면
                # 무의미한 중복 데이터는 최대한 생성하지 말고 발생한 예외는 get_repr에서 기억하는 방향으로...
                # sided: color(+actual), supertype(+actual), subtype(+actual), power(+actual, tend), toughness(+actual, tend), loyalty(+actual, tend), oracle, image
                self.properties["side_A"]["name"] = data["card_faces"][0]["name"]
                self.properties["side_B"]["name"] = data["card_faces"][1]["name"]
                # self.properties["nominal"]["name"] = data["name"]

                self.properties["nominal"]["mana_cost"] = data["card_faces"][0]["mana_cost"]
                # transform 카드 뒷면은 mana_cost가 없음. face1 == nominal

                self.properties["nominal"]["cmc"] = int(data["cmc"])
                # transform 카드는 앞면 뒷면의 cmc가 같음. face1 == nominal

                self.properties["side_A"]["color"] = colorsort(data["card_faces"][0]["colors"])
                self.properties["side_B"]["color"] = colorsort(data["card_faces"][1]["colors"])

                self.properties["nominal"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][0]["mana_cost"])

                front_typeline = data["card_faces"][0]["type_line"].split(" — ")
                back_typeline = data["card_faces"][1]["type_line"].split(" — ")

                self.properties["side_A"]["supertype"] = front_typeline[0].split(" ")
                self.properties["side_B"]["supertype"] = back_typeline[0].split(" ")

                self.properties["side_A"]["subtype"] = front_typeline[1].split(" ") if len(front_typeline) > 1 else []
                self.properties["side_B"]["subtype"] = back_typeline[1].split(" ") if len(back_typeline) > 1 else []

                self.properties["side_A"]["power"] = toler_int(data["card_faces"][0].get('power', ""))
                self.properties["side_B"]["power"] = toler_int(data["card_faces"][1].get('power', ""))

                self.properties["side_A"]["toughness"] = toler_int(data["card_faces"][0].get('toughness', ""))
                self.properties["side_B"]["toughness"] = toler_int(data["card_faces"][1].get('toughness', ""))

                self.properties["side_A"]["loyalty"] = toler_int(data["card_faces"][0].get('loyalty', ""))
                self.properties["side_B"]["loyalty"] = toler_int(data["card_faces"][1].get('loyalty', ""))

                self.properties["side_A"]["oracle"] = data["card_faces"][0]["oracle_text"]
                self.properties["side_B"]["oracle"] = data["card_faces"][1]["oracle_text"]

                self.properties["side_A"]["crop_image"] = data["card_faces"][0]["image_uris"]["border_crop"]
                self.properties["side_B"]["crop_image"] = data["card_faces"][1]["image_uris"]["border_crop"]

            elif self.properties["nominal"]["layout"] == 'Flip':
                # Flip: nominal = side_A = 윗면
                # sided: supertype(+actual), subtype(+actual), power(+actual, tend), toughness(+actual, tend), loyalty(+actual, tend), oracle
                self.properties["side_A"]["name"] = data["card_faces"][0]["name"]
                self.properties["side_B"]["name"] = data["card_faces"][1]["name"]

                self.properties["nominal"]["mana_cost"] = data["card_faces"][0]["mana_cost"]
                self.properties["nominal"]["cmc"] = int(data["cmc"])
                # flip 카드는 cmc, mana cost가 하나 뿐

                self.properties["nominal"]["color"] = data["colors"]
                # flip 카드는 모든 면의 색이 같음 (지금까지는)

                self.properties["nominal"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][0]["mana_cost"])

                top_typeline = data["card_faces"][0]["type_line"].split(" — ")
                bottom_typeline = data["card_faces"][1]["type_line"].split(" — ")

                self.properties["side_A"]["supertype"] = top_typeline[0].split(" ")
                self.properties["side_B"]["supertype"] = bottom_typeline[0].split(" ")

                self.properties["side_A"]["subtype"] = top_typeline[1].split(" ") if len(top_typeline) > 1 else []
                self.properties["side_B"]["subtype"] = bottom_typeline[1].split(" ") if len(bottom_typeline) > 1 else []

                self.properties["side_A"]["power"] = toler_int(data["card_faces"][0].get('power', ""))
                self.properties["side_B"]["power"] = toler_int(data["card_faces"][1].get('power', ""))

                self.properties["side_A"]["toughness"] = toler_int(data["card_faces"][0].get('toughness', ""))
                self.properties["side_B"]["toughness"] = toler_int(data["card_faces"][1].get('toughness', ""))

                # self.properties["nominal"]["loyalty"] = ""  # no flip planeswalker (지금까지는)

                self.properties["side_A"]["oracle"] = data["card_faces"][0]["oracle_text"]
                self.properties["side_B"]["oracle"] = data["card_faces"][1]["oracle_text"]

                self.properties["nominal"]["crop_image"] = data["image_uris"]["border_crop"]
                # flip card는 앞면밖에 없음.

            elif self.properties["nominal"]["layout"] == 'Split':
                # Transform: nominal = side_A(왼면) + side_B(오른면)
                # sided: mama_cost(+alt), cmc(+x), color(+actual), color_accessibility, supertype(+actual), subtype(+actual), oracle
                self.properties["side_A"]["name"] = data["card_faces"][0]["name"]
                self.properties["side_B"]["name"] = data["card_faces"][1]["name"]
                self.properties["nominal"]["name"] = '{} // {}'.format(self.properties["side_A"]["name"], self.properties["side_B"]["name"])

                self.properties["side_A"]["mana_cost"] = data["card_faces"][0]["mana_cost"]
                self.properties["side_B"]["mana_cost"] = data["card_faces"][1]["mana_cost"]
                self.properties["nominal"]["mana_cost"] = mana_sum(self.properties["side_A"]["mana_cost"], self.properties["side_B"]["mana_cost"])

                self.properties["side_A"]["cmc"] = mana_to_cmc(self.properties["side_A"]["mana_cost"])
                self.properties["side_B"]["cmc"] = mana_to_cmc(self.properties["side_B"]["mana_cost"])
                self.properties["nominal"]["cmc"] = int(data["cmc"])

                self.properties["side_A"]["color"] = mana_to_color(data["card_faces"][0]["mana_cost"])
                self.properties["side_B"]["color"] = mana_to_color(data["card_faces"][1]["mana_cost"])
                self.properties["nominal"]["color"] = data["colors"]

                self.properties["side_A"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][0]["mana_cost"])
                self.properties["side_B"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][1]["mana_cost"])
                self.properties["nominal"]["color_accessibility"] = list(set(self.properties["side_A"]["color_accessibility"]) | set(self.properties["side_B"]["color_accessibility"]))

                left_typeline = data["card_faces"][0]["type_line"].split(" — ")
                right_typeline = data["card_faces"][1]["type_line"].split(" — ")

                self.properties["side_A"]["supertype"] = left_typeline[0].split(" ")
                self.properties["side_B"]["supertype"] = right_typeline[0].split(" ")
                supertype_set = list(set(self.properties["side_A"]["supertype"]) | set(self.properties["side_B"]["supertype"]))
                self.properties["nominal"]["supertype"] = sorted(supertype_set, key=typesort)

                self.properties["side_A"]["subtype"] = left_typeline[1].split(" ") if len(left_typeline) > 1 else []
                self.properties["side_B"]["subtype"] = right_typeline[1].split(" ") if len(right_typeline) > 1 else []
                subtype_set = list(set(self.properties["side_A"]["subtype"]) | set(self.properties["side_B"]["subtype"]))
                self.properties["nominal"]["subtype"] = subtypeSort(subtype_set)

                self.properties["side_A"]["power"] = toler_int(data["card_faces"][0].get('power', ""))
                self.properties["side_B"]["power"] = toler_int(data["card_faces"][1].get('power', ""))
                # self.properties["nominal"]["power"] = [self.properties["side_A"]["power"], self.properties["side_B"]["power"]]

                self.properties["side_A"]["toughness"] = toler_int(data["card_faces"][0].get('toughness', ""))
                self.properties["side_B"]["toughness"] = toler_int(data["card_faces"][1].get('toughness', ""))

                # self.properties["nominal"]["power"] = ""
                # self.properties["nominal"]["toughness"] = ""
                # self.properties["nominal"]["loyalty"] = ""
                # No split creature nor planeswalker till now (지금까지는)

                self.properties["side_A"]["oracle"] = data["card_faces"][0]["oracle_text"]
                self.properties["side_B"]["oracle"] = data["card_faces"][1]["oracle_text"]
                self.properties["nominal"]["oracle"] = '{}\n// {}'.format(self.properties["side_A"]["oracle"],
                                                                          self.properties["side_B"]["oracle"])

                self.properties["nominal"]["crop_image"] = data["image_uris"]["border_crop"]
                # split card는 앞면밖에 없음.

            elif self.properties["nominal"]["layout"] == 'Adventure':
                # Adventure: nominal = side_A = creature 파트
                # sided: mama_cost(+alt), cmc(+x), supertype(+actual), subtype(+actual), power(+actual, tend), toughness(+actual, tend), loyalty(+actual, tend), oracle, image
                self.properties["side_A"]["name"] = data["card_faces"][0]["name"]
                self.properties["side_B"]["name"] = data["card_faces"][1]["name"]
                # self.properties["nominal"]["name"] = data["name"]

                self.properties["side_A"]["mana_cost"] = data["card_faces"][0]["mana_cost"]
                self.properties["side_B"]["mana_cost"] = data["card_faces"][1]["mana_cost"]
                # self.properties["nominal"]["mana_cost"] = self.properties["side_A"]["mana_cost"]

                self.properties["side_A"]["cmc"] = mana_to_cmc(self.properties["side_A"]["mana_cost"])
                self.properties["side_B"]["cmc"] = mana_to_cmc(self.properties["side_B"]["mana_cost"])
                # self.properties["nominal"]["cmc"] = int(data["cmc"])

                self.properties["side_A"]["color"] = mana_to_color(data["card_faces"][0]["mana_cost"])
                self.properties["side_B"]["color"] = mana_to_color(data["card_faces"][1]["mana_cost"])
                # self.properties["nominal"]["color"] = data["colors"]

                self.properties["side_A"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][0]["mana_cost"])
                self.properties["side_B"]["color_accessibility"] = mana_to_accessibility(data["card_faces"][1]["mana_cost"])
                # self.properties["nominal"]["color_accessibility"] = list(set(self.properties["side_A"]["color_accessibility"]) | set(self.properties["side_B"]["color_accessibility"]))

                left_typeline = data["card_faces"][0]["type_line"].split(" — ")
                right_typeline = data["card_faces"][1]["type_line"].split(" — ")

                self.properties["side_A"]["supertype"] = left_typeline[0].split(" ")
                self.properties["side_B"]["supertype"] = right_typeline[0].split(" ")

                self.properties["side_A"]["subtype"] = left_typeline[1].split(" ") if len(left_typeline) > 1 else []
                self.properties["side_B"]["subtype"] = right_typeline[1].split(" ") if len(right_typeline) > 1 else []

                # self.properties["nominal"]["power"] = ""
                # self.properties["nominal"]["toughness"] = ""
                # self.properties["nominal"]["loyalty"] = ""
                # No adventure creature nor planeswalker till now (지금까지는)

                self.properties["side_A"]["oracle"] = data["card_faces"][0]["oracle_text"]
                self.properties["side_B"]["oracle"] = data["card_faces"][1]["oracle_text"]

                self.properties["nominal"]["crop_image"] = data["image_uris"]["border_crop"]

            else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
                self.properties["nominal"]["name"] = data["name"]
                self.properties["nominal"]["mana_cost"] = data["mana_cost"]
                self.properties["nominal"]["cmc"] = int(data["cmc"])
                self.properties["nominal"]["color"] = data["colors"]
                self.properties["nominal"]["color_accessibility"] = mana_to_accessibility(data["mana_cost"])

                types = data["type_line"].split(" — ")
                self.properties["nominal"]["supertype"] = types[0].split(" ")
                self.properties["nominal"]["subtype"] = types[1].split(" ") if len(types) > 1 else []
                self.properties["nominal"]["power"] = toler_int(data.get('power', ""))
                self.properties["nominal"]["toughness"] = toler_int(data.get('toughness', ""))
                self.properties["nominal"]["loyalty"] = toler_int(data.get('loyalty', ""))
                self.properties["nominal"]["oracle"] = data["oracle_text"]
                self.properties["nominal"]["crop_image"] = data["image_uris"]["border_crop"]

            self.properties["nominal"]["color"] = colorsort(self.properties["nominal"]["color"])
            self.properties["nominal"]["color_identity"] = colorsort(self.properties["nominal"]["color_identity"])

            # X발비 포함 카드 actual cmc에 "+X" 추가
            x = re.findall(r'{X}', self.properties["nominal"]["mana_cost"])
            if len(x) > 0:
                self.properties["nominal"]["x_in_cmc"] = "X" * len(x)
                if self.properties["nominal"]["layout"] == 'Split':
                    left_x = re.findall(r'{X}', self.properties["side_A"]["mana_cost"])
                    right_x = re.findall(r'{X}', self.properties["side_B"]["mana_cost"])
                    if len(left_x) > 0:
                        self.properties["side_A"]["x_in_cmc"] = "X" * len(left_x)
                    if len(right_x) > 0:
                        self.properties["side_B"]["x_in_cmc"] = "X" * len(right_x)


    def get_repr(self, index, side="nominal", actual=False):
            # getfunc = lambda x, y: self.properties[x][y]

        layout = self.properties["nominal"]["layout"]
        if layout in special_layout:
            if index not in dangerous_properties[layout]:
                side = "nominal"
        else:
            side = "nominal"

        value = self.properties[side][index]
        if actual is True:
            if index in {"color", "power", "toughness", "loyalty"}:
                index = "actual_" + index
                value = self.properties[side][index]
            elif index in {"supertype", "subtype"}:
                index = "actual_" + index
                value += self.properties[side][index]

        return value

    def set_property(self, index, value, side="nominal"):
        layout = self.properties["nominal"]["layout"]
        if layout in special_layout:
            if side == "nominal" and index in dangerous_properties[layout]:
                self.properties["side_A"][index] = value
            elif side != "nominal" and index not in dangerous_properties[layout]:
                self.properties["nominal"][index] = value
            else:
                self.properties[side][index] = value
        else:
            self.properties[side][index] = value

    def __str__(self):
        return "{0}, {1}".format(self.get_repr("name"), self.get_repr("set"))

    def __hash__(self):
        return hash((self.get_repr("name"), self.get_repr("set")))

    def __eq__(self, other):
        if self.properties == other.properties:
            return True
        else:
            return False

    def setter(self, data=None):
        raise NotImplementedError

    def changer(self, **kwargs):
        raise NotImplementedError

    def remover(self, **kwargs):
        raise NotImplementedError

    def showall(self):
        print("properites:")
        for first_key in self.properties.keys():
            print(" ", first_key)
            for second_key in self.properties[first_key].keys():
                print("    %s: %s" % (second_key, self.properties[first_key][second_key]))

        print("actual properites:")
        for first_key in self.properties.keys():
            print(" ", first_key)
            for second_key in self.properties[first_key].keys():
                print("    %s: %s" % (second_key, self.properties[first_key][second_key]))

    def show(self):
        print(
            """Name: {0}
            Mana cost: {1}
            CMC: {2}
            Color: {3}
            Color identity: {4}
            Color accessibility: {5}
            Type: {6}
            Set: {7}
            Rarity: {8}
            P/T: {9}
            Loyalty: {10}
            Price: {11}
            Oracle: {12}"""
            .format(self.get_repr("name", side="nominal"),
                    symbolprettify(self.get_repr("mana_cost")),
                    self.get_repr("cmc"),
                    ''.join(self.get_repr("color") if self.get_repr("color") != () else "C"),
                    ''.join(self.get_repr("color_identity") if self.get_repr("color_identity") != () else "C"),
                    ','.join([''.join(item) for item in self.get_repr("color_accessibility")]),
                    '{}{}'.format(' '.join(self.get_repr("supertype")), (' - ' + ' '.join(self.get_repr("subtype"))) if self.get_repr("subtype") != [] else ""),
                    self.get_repr("set"),
                    self.get_repr("rarity"),
                    '{}/{}'.format(self.get_repr("power"), self.get_repr("toughness")) if self.get_repr("power") != "" else "",
                    self.get_repr("loyalty"),
                    '${}'.format(self.get_repr("usd")),
                    self.get_repr("oracle")
                    )
        )


class SimpleCard(Card):
    def __init__(self, data=None, side="nominal", actual=False, opposite_name=True):
        """
        :param data: initial data source. could be from a Google spreadsheet row or a scryfallCube.Card, and not from Scryfall Json data directly
        :param side: in a multiple-sided card, determines information of which side of the card is stored
        :param actual: if True, actual(weighted) vaules are contained
        :param opposite_name: if True, a name of a multiple-sided card is presented as "AA (// BB)" form. otherwise, only a name of current side is presented.
        """
        if data is None:  # empty initialization
            self.properties = defaultdict(lambda: "")

        if type(data) == list:  # data is Google spreadsheet row
            data = Card(data)

        if type(data) == Card:
            self.properties = defaultdict(lambda: "")

            for index in all_properties:
                self.properties[index] = data.get_repr(index, side=side, actual=actual)

            if opposite_name is True and self.properties["layout"] not in {"Transform", "Flip", "Split", "Adventure"}:
                if side == "side_A":
                    self.properties["name"] = "{} (// {})".format(
                        data.get_repr('name', side="side_A"),
                        data.get_repr('name', side="side_B"))
                elif side == "side_B":
                    self.properties["name"] = "{} (// {})".format(
                        data.get_repr('name', side="side_B"),
                        data.get_repr('name', side="side_A"))
                elif side == "nominal":
                    if self.properties["layout"] != "Split":
                        self.properties["name"] = "{} (// {})".format(
                            data.get_repr('name', side="side_A"),
                            data.get_repr('name', side="side_B"))

    def get_repr(self, index, side="nominal", actual=False):
        return self.properties[index]

    def set_property(self, index, value, side="nominal"):
        self.properties[index] = value

    def showall(self):
        print("properites:")
        for key in self.properties.keys():
            print("  %s: %s" % (key, self.properties[key]))


while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    print(card.__hash__())
    card = SimpleCard(card, side='back', split=True)
    card.set_property('asdf', 200)
    card.showall()
