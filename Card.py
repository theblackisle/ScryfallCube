import ScryfallIO
from Converter import typesort, colorsort, subtypeSort, tolerInt

class Card():
    def __init__(self, data=None):
        if data is None:  # empty initialization
            self.name = ""
            self.mana_cost = ""
            self.cmc = float(-1)
            self.color = []
            self.color_identity = []
            self.type_line = ""
            self.supertype = []
            self.subtype = []
            self.set = ""
            self.rarity = ""
            self.power = ""
            self.toughness = ""
            self.loyalty = ""
            self.oracle = ""
            self.layout = ""
            self.hate = []
            self.buff = []
            self.nerf = []
            self.tags = []
            self.usd = float(-1)
            self.crop_image = ""

        if type(data) == list:  # data is "reverse-prettified" Google spreadsheet row
            self.name = data[0]
            self.mana_cost = data[1]
            self.cmc = data[2]
            self.color = data[3]
            self.color_identity = data[4]
            self.type_line = data[5]
            self.supertype = data[6]
            self.subtype = data[7]
            self.set = data[8]
            self.rarity = data[9]
            self.oracle = data[10]
            self.layout = data[11]
            self.hate = data[12]
            self.buff = data[13]
            self.nerf = data[14]
            self.tags = data[15]
            self.usd = data[16]
            self.crop_image = data[17]

        if type(data) == dict:  # data is JSON from Scryfall
            self.hate = []
            self.buff = []
            self.nerf = []
            self.tags = []  # fixing, infect, selfmill, big, small, ... ...
            self.cmc = data['cmc']
            self.color_identity = data['color_identity']
            self.set = data['set'].upper()
            self.rarity = data['rarity']
            self.usd = float(data.get('usd', 0))

            self.layout = data['layout'].title()
            if self.layout == 'Transform':
                self.color = data['card_faces'][0]['colors']
                self.mana_cost = data['card_faces'][0]['mana_cost']
                self.name = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.crop_image = '{0}\n{1}'.format(data['card_faces'][0]['image_uris']['border_crop'], data['card_faces'][1]['image_uris']['border_crop'])  # 다름
                self.type_line = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.supertype = list(set(front_supertypes) | set(back_supertypes))
                self.subtype = list(set(front_subtypes) | set(back_subtypes))
                self.power = tolerInt(data['card_faces'][0].get('power', ""))
                self.toughness = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.loyalty = tolerInt(data['card_faces'][0].get('loyalty', data['card_faces'][1].get('loyalty', "")))
                self.oracle = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.layout == 'Split':
                self.color = self.color_identity  # 다름
                self.mana_cost = '{0} // {1}'.format(data['card_faces'][0]['mana_cost'], data['card_faces'][1]['mana_cost'])  # 다름
                self.name = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.crop_image = data['image_uris']['border_crop']  # 다름
                self.type_line = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.supertype = list(set(front_supertypes) | set(back_supertypes))
                self.subtype = list(set(front_subtypes) | set(back_subtypes))
                self.power = ""
                self.toughness = ""
                self.loyalty = ""  # No split creature nor planeswalker
                self.oracle = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.layout == 'Flip':
                self.color = data['colors']  # 다름
                self.mana_cost = data['card_faces'][0]['mana_cost']
                self.name = '{0} // {1}'.format(data['card_faces'][0]['name'], data['card_faces'][1]['name'])
                self.crop_image = data['image_uris']['border_crop']  # 다름
                self.type_line = '{0} // {1}'.format(data['card_faces'][0]['type_line'], data['card_faces'][1]['type_line'])
                front_types = data['card_faces'][0]['type_line'].split("—")
                front_supertypes = front_types[0].split()
                front_subtypes = front_types[1].split() if len(front_types) > 1 else []
                back_types = data['card_faces'][1]['type_line'].split("—")
                back_supertypes = back_types[0].split()
                back_subtypes = back_types[1].split() if len(back_types) > 1 else []
                self.supertype = list(set(front_supertypes) | set(back_supertypes))
                self.subtype = list(set(front_subtypes) | set(back_subtypes))
                self.power = tolerInt(data['card_faces'][0].get('power', ""))
                self.toughness = tolerInt(data['card_faces'][0].get('toughness', ""))
                self.loyalty = ""  # no flip planeswalker
                self.oracle = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
                self.name = data['name']
                self.mana_cost = data['mana_cost']
                self.color = data['colors']
                self.crop_image = data['image_uris']['border_crop']
                self.type_line = data['type_line']
                types = data['type_line'].split("—")
                self.supertype = types[0].split()
                self.subtype = types[1].split() if len(types) > 1 else []
                self.power = tolerInt(data.get('power', ""))
                self.toughness = tolerInt(data.get('toughness', ""))
                self.loyalty = tolerInt(data.get('loyalty', ""))
                self.oracle = data['oracle_text']

            self.color = colorsort(self.color)
            self.color_identity = colorsort(self.color_identity)
            self.supertype.sort(key=typesort)
            self.subtype = subtypeSort(self.subtype)

    def setter(self, data=None):
        pass

    def changer(self, **kwargs):
        if 'mana_cost' in kwargs:  # kwargs의 key는 str
            self.mana_cost = kwargs['mana_cost']
        if 'cmc' in kwargs:
            self.cmc = kwargs['cmc']
        if 'colors' in kwargs:
            self.color = kwargs['colors']
        if 'color_identity' in kwargs:
            self.color_identity = kwargs['color_identity']
        if 'type' in kwargs:
            self.type_line = kwargs['type']
        if 'supertype' in kwargs:
            self.supertype.append(kwargs['supertype'])
        if 'subtype' in kwargs:
            self.supertype.append(kwargs['subtype'])
        if 'set' in kwargs:
            self.set = kwargs['set'].upper()
            new_card = ScryfallIO.getCard(self.name, self.set)
            self.id = new_card['id']
            self.crop_image = new_card['image_uris']['border_crop']
            self.rarity = new_card['rarity']
        if 'hate' in kwargs:
            self.hate.append(kwargs['hate'])
        if 'buff' in kwargs:
            self.hate.append(kwargs['buff'])
        if 'nerf' in kwargs:
            self.hate.append(kwargs['nerf'])
        if 'tags' in kwargs:
            self.hate.append(kwargs['tags'])
        else:
            print("no such elements")

    def remover(self, **kwargs):
        if 'supertype' in kwargs:
            self.supertype.remove(kwargs['supertype'])
        if 'subtype' in kwargs:
            self.supertype.remove(kwargs['subtype'])
        if 'hate' in kwargs:
            self.hate.remove(kwargs['hate'])
        if 'buff' in kwargs:
            self.hate.remove(kwargs['buff'])
        if 'nerf' in kwargs:
            self.hate.remove(kwargs['nerf'])
        if 'tags' in kwargs:
            self.hate.remove(kwargs['tags'])
        else:
            print("no such elements")

    def gsExport(self):
        cardlist = [self.name, self.mana_cost, self.cmc, self.color, self.color_identity, self.type_line, self.supertype, self.subtype, self.set, self.rarity, self.power, self.toughness, self.loyalty, self.oracle, self.layout, self.hate, self.buff, self.nerf, self.tags, self.usd, self.crop_image]
        return cardlist

    def showCard(self):
        print("Name: {0}\nMana cost: {1}\nCMC: {2}\nColor: {3}\nColor_identity: {4}\nType: {5}\nSet: {6}\nRarity: {7}\nPower: {8}\nToughness: {9}\nLoyalty: {10}\nPrice: {11}\noracle: {12}".
              format(self.name, self.mana_cost, self.cmc, self.color, self.color_identity, self.type_line, self.set, self.rarity, self.power, self.toughness, self.loyalty, self.usd, self.oracle))

while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.showCard()


