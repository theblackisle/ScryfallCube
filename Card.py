import ScryfallIO
from Converter import *

from collections import defaultdict

class Card():
    def __init__(self, data=None):
        if data is None:  # empty initialization
            self.properties = defaultdict(lambda: defaultdict(lambda: ""))
            self.actual = defaultdict(lambda: defaultdict(lambda: ""))  # layered data from a cube maker

        if type(data) == list:  # data is "reverse-prettified" Google spreadsheet row
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

        if type(data) == dict:  # data is JSON from Scryfall
            '''
            ☆properties constant to layout
            color_identity
            set
            rarity
            usd
            layout
            
            ☆properties only in 'face0(=nominal)' dict
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
            self.actual["face0"]["buff"] = []
            self.actual["face0"]["nerf"] = []  # hate for color, tribe, and else ...
            self.actual["face0"]["tags"] = []  # fixing, infect, selfmill, big, small, ... ...
            self.properties["face0"]["color_identity"] = tuple(data['color_identity'])  # split 카드의 활성화비용 identity..이런건 무시하기로.
            self.properties["face0"]["set"] = data['set'].upper()
            self.properties["face0"]["rarity"] = data['rarity']
            self.properties["face0"]["usd"] = float(data.get('usd', 0))
            self.properties["face0"]["layout"] = data['layout'].title()

            if self.properties["face0"]["layout"] == 'Transform':
                self.properties["face1"]["color"] = data['card_faces'][0]['colors']
                self.properties["face2"]["color"] = data['card_faces'][1]['colors']
                self.properties["face0"]["color"] = self.properties["face1"]["color"]

                self.properties["face1"]["mana_cost"] = data['card_faces'][0]['mana_cost']
                # self.properties["mana_cost"]["face2"] = ""
                # transform 카드 뒷면은 mana_cost가 없음.
                self.properties["face0"]["mana_cost"] = self.properties["face1"]["mana_cost"]

                self.properties["face0"]["cmc"] = int(data['cmc'])
                self.properties["face1"]["cmc"] = self.properties["face0"]["cmc"]
                self.properties["face2"]["cmc"] = self.properties["face0"]["cmc"]
                # transform 카드는 앞면 뒷면의 cmc가 같음.

                self.properties["face1"]["name"] = data['card_faces'][0]['name']
                self.properties["face2"]["name"] = data['card_faces'][1]['name']
                self.properties["face0"]["name"] = '{0} // {1}'.format(self.properties["face1"]["name"], self.properties["face2"]["name"])

                self.properties["face1"]["type_line"] = data['card_faces'][0]['type_line']
                self.properties["face2"]["type_line"] = data['card_faces'][1]['type_line']
                self.properties["face0"]["type_line"] = '{0}\n{1}'.format(self.properties["face1"]["type_line"], self.properties["face2"]["type_line"])

                face1_types = data['card_faces'][0]['type_line'].split("—")
                face1_supertypes = face1_types[0].split()
                face1_subtypes = face1_types[1].split() if len(face1_types) > 1 else []

                face2_types = data['card_faces'][1]['type_line'].split("—")
                face2_supertypes = face2_types[0].split()
                face2_subtypes = face2_types[1].split() if len(face2_types) > 1 else []

                self.properties["face0"]["supertype"] = list(set(face1_supertypes) | set(face2_supertypes))
                self.properties["face0"]["subtype"] = list(set(face1_subtypes) | set(face2_subtypes))

                self.properties["face1"]["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["face2"]["power"] = tolerInt(data['card_faces'][1].get('power', ""))
                self.properties["face0"]["power"] = '{0}\n{1}'.format(self.properties["face1"]["power"], self.properties["face2"]["power"])

                self.properties["face1"]["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["face2"]["toughness"] = tolerInt(data['card_faces'][1].get('toughness', ""))
                self.properties["face0"]["toughness"] = '{0}\n{1}'.format(self.properties["face1"]["toughness"], self.properties["face2"]["toughness"])

                self.properties["face1"]["loyalty"] = tolerInt(data['card_faces'][0].get('loyalty', ""))
                self.properties["face2"]["loyalty"] = tolerInt(data['card_faces'][1].get('loyalty', ""))
                self.properties["face0"]["loyalty"] = '{0}\n{1}'.format(self.properties["face1"]["loyalty"], self.properties["face2"]["loyalty"])

                self.properties["face1"]["oracle"] = data['card_faces'][0]['oracle_text']
                self.properties["face2"]["oracle"] = data['card_faces'][1]['oracle_text']
                self.properties["face0"]["oracle"] = '{0}\n//\n{1}'.format(self.properties["face1"]["oracle"], self.properties["face2"]["oracle"])

                self.properties["face1"]["crop_image"] = data['card_faces'][0]['crop_image']
                self.properties["face2"]["crop_image"] = data['card_faces'][1]['crop_image']
                self.properties["face0"]["crop_image"] = '{0}\n{1}'.format(self.properties["face1"]["crop_image"], self.properties["face2"]["crop_image"])  # 다름

            elif self.properties["face0"]["layout"] == 'Split':
                self.properties["face1"]["color"] = data['card_faces'][0]['colors']
                self.properties["face2"]["color"] = data['card_faces'][1]['colors']
                self.properties["face0"]["color"] = tuple(set(data['card_faces'][0]['colors']) | set(data['card_faces'][1]['colors']))

                self.properties["face1"]["mana_cost"] = data['card_faces'][0]['mana_cost']
                self.properties["face2"]["mana_cost"] = data['card_faces'][1]['mana_cost']
                self.properties["face0"]["mana_cost"] = '{0}\n{1}'.format(self.properties["face1"]["mana_cost"], self.properties["face2"]["mana_cost"])

                self.properties["face1"]["cmc"] = mana_to_cmc(self.properties["face1"]["mana_cost"])
                self.properties["face2"]["cmc"] = mana_to_cmc(self.properties["face2"]["mana_cost"])
                self.properties["face0"]["cmc"] = int(data['cmc'])

                self.properties["face1"]["name"] = data['card_faces'][0]['name']
                self.properties["face2"]["name"] = data['card_faces'][1]['name']
                self.properties["face0"]["name"] = '{0} // {1}'.format(self.properties["face1"]["name"], self.properties["face2"]["name"])

                self.properties["face1"]["type_line"] = data['card_faces'][0]['type_line']
                self.properties["face2"]["type_line"] = data['card_faces'][1]['type_line']
                self.properties["face0"]["type_line"] = '{0}\n{1}'.format(self.properties["face1"]["type_line"], self.properties["face2"]["type_line"])

                face1_types = data['card_faces'][0]['type_line'].split("—")
                face1_supertypes = face1_types[0].split()
                face1_subtypes = face1_types[1].split() if len(face1_types) > 1 else []

                face2_types = data['card_faces'][1]['type_line'].split("—")
                face2_supertypes = face2_types[0].split()
                face2_subtypes = face2_types[1].split() if len(face2_types) > 1 else []

                self.properties["face0"]["supertype"] = list(set(face1_supertypes) | set(face2_supertypes))
                self.properties["face0"]["subtype"] = list(set(face1_subtypes) | set(face2_subtypes))

                # self.properties["face0"]["power"] = ""
                # self.properties["face0"]["toughness"] = ""
                # self.properties["face0"]["loyalty"] = ""
                # No split creature nor planeswalker till now

                self.properties["face1"]["oracle"] = data['card_faces'][0]['oracle_text']
                self.properties["face2"]["oracle"] = data['card_faces'][1]['oracle_text']
                self.properties["face0"]["oracle"] = '{0}\n//\n{1}'.format(self.properties["face1"]["oracle"], self.properties["face2"]["oracle"])

                self.properties["crop_image"] = data['image_uris']['border_crop']
                # split/flip card는 앞면밖에 없음.

            elif self.properties["face0"]["layout"] == 'Flip':
                self.properties["face0"]["color"] = data['colors']
                self.properties["face0"]["mana_cost"] = data['card_faces'][0]['mana_cost']

                self.properties["face0"]["name"] = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.properties["face0"]["type_line"] = '{0}\n{1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])

                face1_types = data['card_faces'][0]['type_line'].split("—")
                face1_supertypes = face1_types[0].split()
                face1_subtypes = face1_types[1].split() if len(face1_types) > 1 else []

                face2_types = data['card_faces'][1]['type_line'].split("—")
                face2_supertypes = face2_types[0].split()
                face2_subtypes = face2_types[1].split() if len(face2_types) > 1 else []

                self.properties["face0"]["supertype"] = list(set(face1_supertypes) | set(face2_supertypes))
                self.properties["face0"]["subtype"] = list(set(face1_subtypes) | set(face2_subtypes))

                self.properties["face1"]["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["face2"]["power"] = tolerInt(data['card_faces'][1].get('power', ""))
                self.properties["face0"]["power"] = '{0}\n{1}'.format(self.properties["face1"]["power"], self.properties["face2"]["power"])

                self.properties["face1"]["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["face2"]["toughness"] = tolerInt(data['card_faces'][1].get('toughness', ""))
                self.properties["face0"]["toughness"] = '{0}\n{1}'.format(self.properties["face1"]["toughness"], self.properties["face2"]["toughness"])

                # self.properties["face0"]["loyalty"] = ""  no flip planeswalker

                self.properties["oracle"] = '{0}\n//\n{1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

                self.properties["crop_image"] = data['image_uris']['border_crop']

            else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
                self.properties["face0"]["name"] = data['name']
                self.properties["face0"]["mana_cost"] = data['mana_cost']
                self.properties["face0"]["color"] = data['colors']
                self.properties["face0"]["crop_image"] = data['image_uris']['border_crop']
                self.properties["face0"]["type_line"] = data['type_line']
                types = data['type_line'].split("—")
                self.properties["face0"]["supertype"] = types[0].split()
                self.properties["face0"]["subtype"] = types[1].split() if len(types) > 1 else []
                self.properties["face0"]["power"] = tolerInt(data.get('power', ""))
                self.properties["face0"]["toughness"] = tolerInt(data.get('toughness', ""))
                self.properties["face0"]["loyalty"] = tolerInt(data.get('loyalty', ""))
                self.properties["face0"]["oracle"] = data['oracle_text']

            self.properties["face0"]["color"] = colorsort(self.properties["color"])
            self.properties["face0"]["color_identity"] = colorsort(self.properties["color_identity"])
            self.properties["face0"]["supertype"] = tuple(sorted(self.properties["supertype"], key=typesort))
            self.properties["face0"]["subtype"] = subtypeSort(self.properties["subtype"])  # 모두 tuple

    def __str__(self):
        return "Scryfall Card object for: {0}, {1}".format(self.properties["face0"]["name"], self.properties["face0"]["set"].upper())

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.properties["face0"]["name"], self.properties["face0"]["set"]))

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
        Oracle: {12}""".format(self.properties["face0"]["name"],
                               self.properties["face0"]["mana_cost"],
                               self.properties["face0"]["cmc"],
                               self.properties["face0"]["color"],
                               self.properties["face0"]["color_identity"],
                               self.properties["face0"]["type_line"],
                               self.properties["face0"]["set"],
                               self.properties["face0"]["rarity"],
                               self.properties["face0"]["power"],
                               self.properties["face0"]["toughness"],
                               self.properties["face0"]["loyalty"],
                               self.properties["face0"]["usd"],
                               self.properties["face0"]["oracle"]))

while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.show()


