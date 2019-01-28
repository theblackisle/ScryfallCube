import ScryfallIO
from Converter import *

from collections import defaultdict

class Card():
    def __init__(self, data=None, reference="Scryfall"):
        if data is None:  # empty initialization
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.actual = defaultdict(lambda: defaultdict(lambda: ""))  # layered data from a cube maker

        if reference == "Gspread":  # data is "uglified" Google spreadsheet row
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.actual = defaultdict(lambda: defaultdict(lambda: ""))
            self.properties["name"] = data[0]
            self.properties["mana_cost"] = data[1]
            self.properties["cmc"] = data[2]
            self.properties["color"] = data[3]
            self.properties["color_identity"] = data[4]
            self.properties["type_line"] = data[5]
            self.properties["supertype"] = data[6]
            self.properties["subtype"] = data[7]
            self.properties["set"] = data[8]
            self.properties["rarity"] = data[9]
            self.properties["power"] = data[10]
            self.properties["toughness"] = data[11]
            self.properties["loyalty"] = data[12]
            self.properties["oracle"] = data[13]
            self.properties["layout"] = data[14]
            self.properties["hate"] = data[15]
            self.properties["buff"] = data[16]
            self.properties["nerf"] = data[17]
            self.properties["tags"] = data[18]
            self.properties["usd"] = data[19]
            self.properties["crop_image"] = data[20]

        if reference == "Scryfall":  # data is JSON from Scryfall
            '''
            ☆properties constant to layout
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
            '''
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.actual = defaultdict(lambda: defaultdict(lambda: ""))
            self.actual["nominal"]["buff"] = []
            self.actual["nominal"]["nerf"] = []  # hate for color, tribe, and else ...
            self.actual["nominal"]["tags"] = []  # fixing, infect, selfmill, big, small, ... ...
            self.properties["nominal"]["color_identity"] = tuple(data['color_identity'])  # split 카드의 활성화비용 identity..이런건 무시하기로.
            self.properties["nominal"]["set"] = data['set'].upper()
            self.properties["nominal"]["rarity"] = data['rarity'].title()
            self.properties["nominal"]["usd"] = float(data.get('usd', 0))
            self.properties["nominal"]["layout"] = data['layout'].title()

            if self.properties["nominal"]["layout"] == 'Transform':
                # 무의미한 정보를 최대한 지우고 발생한 예외는 기억하는 방향으로...
                self.properties["front"]["name"] = data['card_faces'][0]['name']
                self.properties["back"]["name"] = data['card_faces'][1]['name']
                self.properties["nominal"]["name"] = data['name']

                self.properties["nominal"]["mana_cost"] = data['card_faces'][0]['mana_cost']
                # transform 카드 뒷면은 mana_cost가 없음. face1 == nominal

                self.properties["nominal"]["cmc"] = int(data['cmc'])
                # transform 카드는 앞면 뒷면의 cmc가 같음. face1 == nominal

                self.properties["front"]["color"] = colorsort(data['card_faces'][0]['colors'])
                # front == nominal
                self.properties["back"]["color"] = colorsort(data['card_faces'][1]['colors'])

                front_typeline = data['card_faces'][0]['type_line'].split("-")
                back_typeline = data['card_faces'][1]['type_line'].split("-")

                self.properties["front"]["supertype"] = front_typeline[0]
                self.properties["back"]["supertype"] = back_typeline[0]
                # self.properties["nominal"]["supertype"] = [self.properties["front"]["supertype"], self.properties["back"]["supertype"]]

                self.properties["front"]["subtype"] = front_typeline[1] if len(front_typeline) > 1 else ""
                self.properties["back"]["subtype"] = back_typeline[1] if len(back_typeline) > 1 else ""
                # self.properties["nominal"]["subtype"] = [self.properties["front"]["subtype"], self.properties["back"]["subtype"]]

                self.properties["front"]["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["back"]["power"] = tolerInt(data['card_faces'][1].get('power', ""))
                # self.properties["nominal"]["power"] = [self.properties["front"]["power"], self.properties["back"]["power"]]

                self.properties["front"]["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["back"]["toughness"] = tolerInt(data['card_faces'][1].get('toughness', ""))
                # self.properties["nominal"]["toughness"] = [self.properties["front"]["toughness"], self.properties["back"]["toughness"]]

                self.properties["front"]["loyalty"] = tolerInt(data['card_faces'][0].get('loyalty', ""))
                self.properties["back"]["loyalty"] = tolerInt(data['card_faces'][1].get('loyalty', ""))
                # self.properties["nominal"]["loyalty"] = [self.properties["front"]["loyalty"], self.properties["back"]["loyalty"]]

                self.properties["front"]["oracle"] = data['card_faces'][0]['oracle_text']
                self.properties["back"]["oracle"] = data['card_faces'][1]['oracle_text']
                # self.properties["nominal"]["oracle"] = [self.properties["front"]["oracle"], self.properties["back"]["oracle"]]

                self.properties["front"]["crop_image"] = data['card_faces'][0]['crop_image']
                self.properties["back"]["crop_image"] = data['card_faces'][1]['crop_image']
                # self.properties["nominal"]["crop_image"] = [self.properties["front"]["crop_image"], self.properties["back"]["crop_image"]]

            elif self.properties["nominal"]["layout"] == 'Split':
                self.properties["left"]["name"] = data['card_faces'][0]['name']
                self.properties["right"]["name"] = data['card_faces'][1]['name']
                self.properties["nominal"]["name"] = data['name']

                self.properties["left"]["mana_cost"] = data['card_faces'][0]['mana_cost']
                self.properties["right"]["mana_cost"] = data['card_faces'][1]['mana_cost']
                self.properties["nominal"]["mana_cost"] = mana_sum(self.properties["left"]["mana_cost"], self.properties["right"]["mana_cost"])

                self.properties["left"]["cmc"] = mana_to_cmc(self.properties["left"]["mana_cost"])
                self.properties["right"]["cmc"] = mana_to_cmc(self.properties["right"]["mana_cost"])
                self.properties["nominal"]["cmc"] = int(data['cmc'])

                self.properties["left"]["color"] = colorsort(data['card_faces'][0]['colors'])
                self.properties["right"]["color"] = colorsort(data['card_faces'][1]['colors'])
                self.properties["nominal"]["color"] = data['colors']

                left_typeline = data['card_faces'][0]['type_line'].split("-")
                right_typeline = data['card_faces'][1]['type_line'].split("-")

                self.properties["left"]["supertype"] = left_typeline[0]
                self.properties["right"]["supertype"] = right_typeline[0]
                supertype_set = list(set(self.properties["left"]["supertype"].split()) | set(self.properties["right"]["supertype"].split()))
                self.properties["nominal"]["supertype"] = tuple(sorted(supertype_set, key=typesort))

                self.properties["left"]["subtype"] = left_typeline[1] if len(left_typeline) > 1 else ""
                self.properties["right"]["subtype"] = right_typeline[1] if len(right_typeline) > 1 else ""
                subtype_set = list(set(self.properties["left"]["subtype"].split()) | set(self.properties["right"]["subtype"].split()))
                self.properties["nominal"]["subtype"] = subtypeSort(subtype_set)

                # self.properties["nominal"]["power"] = ""
                # self.properties["nominal"]["toughness"] = ""
                # self.properties["nominal"]["loyalty"] = ""
                # No split creature nor planeswalker till now

                self.properties["left"]["oracle"] = data['card_faces'][0]['oracle_text']
                self.properties["right"]["oracle"] = data['card_faces'][1]['oracle_text']
                self.properties["nominal"]["oracle"] = '{}\n// {}'.format(self.properties["left"]["oracle"],
                                                                          self.properties["right"]["oracle"])

                self.properties["nominal"]["crop_image"] = data['image_uris']['border_crop']
                # split/flip card는 앞면밖에 없음.

            elif self.properties["nominal"]["layout"] == 'Flip':
                self.properties["top"]["name"] = data['card_faces'][0]['name']
                self.properties["bottom"]["name"] = data['card_faces'][1]['name']
                self.properties["nominal"]["name"] = data['name']

                self.properties["nominal"]["mana_cost"] = data['card_faces'][0]['mana_cost']
                self.properties["nominal"]["cmc"] = int(data['cmc'])
                # flip 카드는 cmc, mana cost가 하나 뿐

                self.properties["nominal"]["color"] = data['colors']
                # flip 카드는 모든 면의 색이 같음

                top_typeline = data['card_faces'][0]['type_line'].split("-")
                bottom_typeline = data['card_faces'][1]['type_line'].split("-")

                self.properties["top"]["supertype"] = top_typeline[0]
                self.properties["bottom"]["supertype"] = bottom_typeline[0]
                # self.properties["nominal"]["supertype"] = [self.properties["top"]["supertype"], self.properties["bottom"]["supertype"]]

                self.properties["top"]["subtype"] = top_typeline[1] if len(top_typeline) > 1 else ""
                self.properties["bottom"]["subtype"] = bottom_typeline[1] if len(bottom_typeline) > 1 else ""
                # self.properties["nominal"]["subtype"] = [self.properties["top"]["subtype"], self.properties["bottom"]["subtype"]]

                self.properties["top"]["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["bottom"]["power"] = tolerInt(data['card_faces'][1].get('power', ""))
                # self.properties["nominal"]["power"] = [self.properties["top"]["power"], self.properties["bottom"]["power"]]

                self.properties["top"]["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["bottom"]["toughness"] = tolerInt(data['card_faces'][1].get('toughness', ""))
                # self.properties["nominal"]["toughness"] = [self.properties["top"]["toughness"], self.properties["bottom"]["toughness"]]

                # self.properties["nominal"]["loyalty"] = ""  no flip planeswalker

                self.properties["top"]["oracle"] = data['card_faces'][0]['oracle_text']
                self.properties["bottom"]["oracle"] = data['card_faces'][1]['oracle_text']
                # self.properties["nominal"]["oracle"] = [self.properties["top"]["oracle"], self.properties["bottom"]["oracle"]]

                self.properties["crop_image"] = data['image_uris']['border_crop']

            else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
                self.properties["nominal"]["name"] = data['name']
                self.properties["nominal"]["mana_cost"] = data['mana_cost']
                self.properties["nominal"]["color"] = data['colors']
                self.properties["nominal"]["crop_image"] = data['image_uris']['border_crop']

                types = data['type_line'].split("—")
                self.properties["nominal"]["supertype"] = types[0].split()
                self.properties["nominal"]["subtype"] = types[1].split() if len(types) > 1 else []
                self.properties["nominal"]["power"] = tolerInt(data.get('power', ""))
                self.properties["nominal"]["toughness"] = tolerInt(data.get('toughness', ""))
                self.properties["nominal"]["loyalty"] = tolerInt(data.get('loyalty', ""))
                self.properties["nominal"]["oracle"] = data['oracle_text']
                self.properties["nominal"]["crop_image"] = data['image_uris']['border_crop']

            self.properties["nominal"]["color"] = colorsort(self.properties["color"])
            self.properties["nominal"]["color_identity"] = colorsort(self.properties["color_identity"])
            x = re.findall(r'{X}', self.properties["nominal"]["cmc"])
            if len(x) > 0:
                self.actual["nominal"]["cmc"] = "+" + "X"*len(x)
                if self.properties["nominal"]["layout"] == 'Split':
                    left_x = re.findall(r'{X}', self.properties["nominal"]["left"])
                    right_x = re.findall(r'{X}', self.properties["nominal"]["right"])
                    if len(left_x) > 0:
                        self.actual["left"]["cmc"] = "+" + "X" * len(left_x)
                    if len(right_x) > 0:
                        self.actual["right"]["cmc"] = "+" + "X" * len(right_x)
            # X발비 포함 카드 actual cmc에 "+X" 추가

            # self.properties["nominal"]["supertype"] = tuple(sorted(self.properties["nominal"]["supertype"], key=typesort))
            # self.properties["nominal"]["subtype"] = subtypeSort(self.properties["nominal"]["subtype"])  # 모두 tuple

    def __str__(self):
        return "Scryfall Card object for: {0}, {1}".format(self.properties["nominal"]["name"], self.properties["nominal"]["set"])

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.properties["nominal"]["name"], self.properties["nominal"]["set"]))

    def setter(self, data=None):
        raise NotImplementedError

    def changer(self, **kwargs):
        raise NotImplementedError

    def remover(self, **kwargs):
        raise NotImplementedError

    def show(self):
        print("""Name: {0}
        Mana cost: {1}
        CMC: {2}
        Color: {3}
        Color identity: {4}
        Type: {5}
        Set: {6}
        Rarity: {7}
        Power: {8}
        Toughness: {9}
        Loyalty: {10}
        Price: {11}
        Oracle: {12}""".format(self.properties["nominal"]["name"],
                               self.properties["nominal"]["mana_cost"],
                               self.properties["nominal"]["cmc"],
                               self.properties["nominal"]["color"],
                               self.properties["nominal"]["color_identity"],
                               self.properties["nominal"]["type_line"],
                               self.properties["nominal"]["set"],
                               self.properties["nominal"]["rarity"],
                               self.properties["nominal"]["power"],
                               self.properties["nominal"]["toughness"],
                               self.properties["nominal"]["loyalty"],
                               self.properties["nominal"]["usd"],
                               self.properties["nominal"]["oracle"]))

while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.show()


