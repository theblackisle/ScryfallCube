import ScryfallIO
from Converter import typesort, colorsort, subtypeSort, tolerInt

class Card():
    def __init__(self, data=None):
        if data is None:  # empty initialization
            self.properties = {}
            self.properties["name"] = ""
            self.properties["mana_cost"] = ""
            self.properties["cmc"] = int(-1)
            self.properties["color"] = ()
            self.properties["color_identity"] = ()
            self.properties["type_line"] = ""
            self.properties["supertype"] = ()
            self.properties["subtype"] = ()
            self.properties["set"] = ""
            self.properties["rarity"] = ""
            self.properties["power"] = ""
            self.properties["toughness"] = ""
            self.properties["loyalty"] = ""
            self.properties["oracle"] = ""
            self.properties["layout"] = ""
            self.properties["hate"] = []
            self.properties["buff"] = []
            self.properties["nerf"] = []
            self.properties["tags"] = []
            self.properties["usd"] = float(-1)
            self.properties["crop_image"] = ""

        if type(data) == list:  # data is "reverse-prettified" Google spreadsheet row
            self.properties = {}
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
            self.properties = {}
            self.properties["hate"] = []
            self.properties["buff"] = []
            self.properties["nerf"] = []
            self.properties["tags"] = []  # fixing, infect, selfmill, big, small, ... ...
            self.properties["cmc"] = int(data['cmc'])
            self.properties["color_identity"] = tuple(data['color_identity'])
            self.properties["set"] = data['set'].upper()
            self.properties["rarity"] = data['rarity']
            self.properties["usd"] = float(data.get('usd', 0))

            self.properties["layout"] = data['layout'].title()
            if self.properties["layout"] == 'Transform':
                self.properties["color"] = data['card_faces'][0]['colors']
                self.properties["mana_cost"] = data['card_faces'][0]['mana_cost']
                self.properties["name"] = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.properties["crop_image"] = '{0}\n{1}'.format(data['card_faces'][0]['image_uris']['border_crop'], data['card_faces'][1]['image_uris']['border_crop'])  # 다름
                self.properties["type_line"] = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.properties["supertype"] = list(set(front_supertypes) | set(back_supertypes))
                self.properties["subtype"] = list(set(front_subtypes) | set(back_subtypes))
                self.properties["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["loyalty"] = tolerInt(data['card_faces'][0].get('loyalty', data['card_faces'][1].get('loyalty', "")))
                self.properties["oracle"] = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.properties["layout"] == 'Split':
                self.properties["color"] = self.properties["color_identity"]  # 다름
                self.properties["mana_cost"] = '{0} // {1}'.format(data['card_faces'][0]['mana_cost'], data['card_faces'][1]['mana_cost'])  # 다름
                self.properties["name"] = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.properties["crop_image"] = data['image_uris']['border_crop']  # 다름
                self.properties["type_line"] = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.properties["supertype"] = list(set(front_supertypes) | set(back_supertypes))
                self.properties["subtype"] = list(set(front_subtypes) | set(back_subtypes))
                self.properties["power"] = ""
                self.properties["toughness"] = ""
                self.properties["loyalty"] = ""  # No split creature nor planeswalker
                self.properties["oracle"] = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.properties["layout"] == 'Flip':
                self.properties["color"] = data['colors']  # 다름
                self.properties["mana_cost"] = data['card_faces'][0]['mana_cost']
                self.properties["name"] = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.properties["crop_image"] = data['image_uris']['border_crop']  # 다름
                self.properties["type_line"] = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.properties["supertype"] = list(set(front_supertypes) | set(back_supertypes))
                self.properties["subtype"] = list(set(front_subtypes) | set(back_subtypes))
                self.properties["power"] = tolerInt(data['card_faces'][0].get('power', ""))
                self.properties["toughness"] = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.properties["loyalty"] = ""  # no flip planeswalker
                self.properties["oracle"] = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
                self.properties["name"] = data['name']
                self.properties["mana_cost"] = data['mana_cost']
                self.properties["color"] = data['colors']
                self.properties["crop_image"] = data['image_uris']['border_crop']
                self.properties["type_line"] = data['type_line']
                types = data['type_line'].split("—")
                self.properties["supertype"] = types[0].split()
                self.properties["subtype"] = types[1].split() if len(types) > 1 else []
                self.properties["power"] = tolerInt(data.get('power', ""))
                self.properties["toughness"] = tolerInt(data.get('toughness', ""))
                self.properties["loyalty"] = tolerInt(data.get('loyalty', ""))
                self.properties["oracle"] = data['oracle_text']

            self.properties["color"] = colorsort(self.properties["color"])
            self.properties["color_identity"] = colorsort(self.properties["color_identity"])
            self.properties["supertype"] = tuple(sorted(self.properties["supertype"], key=typesort))
            self.properties["subtype"] = subtypeSort(self.properties["subtype"])  # 모두 tuple

    def __str__(self):
        return "Scryfall Card object for: {0}, {1}".format(self.properties["name"], self.properties["set"].upper())

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.properties["name"], self.properties["set"]))

    def setter(self, data=None):
        pass

    def changer(self, **kwargs):
        if 'mana_cost' in kwargs:  # kwargs의 key는 str
            self.properties["mana_cost"] = kwargs['mana_cost']
        if 'cmc' in kwargs:
            self.properties["cmc"] = kwargs['cmc']
        if 'colors' in kwargs:
            self.properties["color"] = kwargs['colors']
        if 'color_identity' in kwargs:
            self.properties["color_identity"] = kwargs['color_identity']
        if 'type' in kwargs:
            self.properties["type_line"] = kwargs['type']
        if 'supertype' in kwargs:
            self.properties["supertype"].append(kwargs['supertype'])
        if 'subtype' in kwargs:
            self.properties["supertype"].append(kwargs['subtype'])
        if 'set' in kwargs:
            self.properties["set"] = kwargs['set'].upper()
            new_card = ScryfallIO.getCard(self.properties["name"], self.properties["set"])
            self.properties["crop_image"] = new_card['image_uris']['border_crop']
            self.properties["rarity"] = new_card['rarity']
        if 'hate' in kwargs:
            self.properties["hate"].append(kwargs['hate'])
        if 'buff' in kwargs:
            self.properties["hate"].append(kwargs['buff'])
        if 'nerf' in kwargs:
            self.properties["hate"].append(kwargs['nerf'])
        if 'tags' in kwargs:
            self.properties["hate"].append(kwargs['tags'])
        else:
            print("no such elements")

    def remover(self, **kwargs):
        if 'supertype' in kwargs:
            self.properties["supertype"].remove(kwargs['supertype'])
        if 'subtype' in kwargs:
            self.properties["supertype"].remove(kwargs['subtype'])
        if 'hate' in kwargs:
            self.properties["hate"].remove(kwargs['hate'])
        if 'buff' in kwargs:
            self.properties["hate"].remove(kwargs['buff'])
        if 'nerf' in kwargs:
            self.properties["hate"].remove(kwargs['nerf'])
        if 'tags' in kwargs:
            self.properties["hate"].remove(kwargs['tags'])
        else:
            print("no such elements")

    def showCard(self):
        print("Name: {0}\nMana cost: {1}\nCMC: {2}\nColor: {3}\nColor_identity: {4}\nType: {5}\nSet: {6}\nRarity: {7}\nPower: {8}\nToughness: {9}\nLoyalty: {10}\nPrice: {11}\noracle: {12}".
              format(self.properties["name"], self.properties["mana_cost"], self.properties["cmc"], self.properties["color"], self.properties["color_identity"], self.properties["type_line"], self.properties["set"], self.properties["rarity"], self.properties["power"], self.properties["toughness"], self.properties["loyalty"], self.properties["usd"], self.properties["oracle"]))

while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.showCard()


