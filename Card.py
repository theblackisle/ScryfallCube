import ScryfallIO

class Card():
    def __init__(self, scryfallJSON):
        self.hate = []
        self.buff = []
        self.nerf = []
        self.tags = []  # fixing, infect, selfmill, big, small, ... ...
        self.id = scryfallJSON['id']
        self.cmc = scryfallJSON['cmc']
        self.color_identity = scryfallJSON['color_identity']
        self.set = scryfallJSON['set'].upper()
        self.rarity = scryfallJSON['rarity']

        self.layout = scryfallJSON['layout']
        if self.layout == 'transform':
            self.color = scryfallJSON['card_faces'][0]['colors']
            self.mana_cost = scryfallJSON['card_faces'][0]['mana_cost']
            self.name = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['name'], scryfallJSON['card_faces'][1]['name'])
            self.crop_image = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['image_uris']['border_crop'], scryfallJSON['card_faces'][1]['image_uris']['border_crop'])  # 다름
            self.type_line = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['type_line'], scryfallJSON['card_faces'][1]['type_line'])
            front_types = scryfallJSON['card_faces'][0]['type_line'].split("—")
            front_supertypes = front_types[0].split()
            front_subtypes = front_types[1].split() if len(front_types) > 1 else []
            back_types = scryfallJSON['card_faces'][1]['type_line'].split("—")
            back_supertypes = back_types[0].split()
            back_subtypes = back_types[1].split() if len(back_types) > 1 else []
            self.supertype = list(set(front_supertypes) | set(back_supertypes))
            self.subtype = list(set(front_subtypes) | set(back_subtypes))
            self.oracle = '{0} \n// {1}'.format(scryfallJSON['card_faces'][0]['oracle_text'], scryfallJSON['card_faces'][1]['oracle_text'])

        elif self.layout == 'split':
            self.color = self.color_identity  # 다름
            self.mana_cost = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['mana_cost'], scryfallJSON['card_faces'][1]['mana_cost'])  # 다름
            self.name = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['name'], scryfallJSON['card_faces'][1]['name'])
            self.crop_image = scryfallJSON['image_uris']['border_crop']  # 다름
            self.type_line = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['type_line'], scryfallJSON['card_faces'][1]['type_line'])
            front_types = scryfallJSON['card_faces'][0]['type_line'].split("—")
            front_supertypes = front_types[0].split()
            front_subtypes = front_types[1].split() if len(front_types) > 1 else []
            back_types = scryfallJSON['card_faces'][1]['type_line'].split("—")
            back_supertypes = back_types[0].split()
            back_subtypes = back_types[1].split() if len(back_types) > 1 else []
            self.supertype = list(set(front_supertypes) | set(back_supertypes))
            self.subtype = list(set(front_subtypes) | set(back_subtypes))
            self.oracle = '{0} \n// {1}'.format(scryfallJSON['card_faces'][0]['oracle_text'], scryfallJSON['card_faces'][1]['oracle_text'])

        elif self.layout == 'flip':
            self.color = scryfallJSON['colors']  # 다름
            self.mana_cost = scryfallJSON['card_faces'][0]['mana_cost']
            self.name = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['name'], scryfallJSON['card_faces'][1]['name'])
            self.crop_image = scryfallJSON['image_uris']['border_crop']  # 다름
            self.type_line = '{0} // {1}'.format(scryfallJSON['card_faces'][0]['type_line'], scryfallJSON['card_faces'][1]['type_line'])
            front_types = scryfallJSON['card_faces'][0]['type_line'].split("—")
            front_supertypes = front_types[0].split()
            front_subtypes = front_types[1].split() if len(front_types) > 1 else []
            back_types = scryfallJSON['card_faces'][1]['type_line'].split("—")
            back_supertypes = back_types[0].split()
            back_subtypes = back_types[1].split() if len(back_types) > 1 else []
            self.supertype = list(set(front_supertypes) | set(back_supertypes))
            self.subtype = list(set(front_subtypes) | set(back_subtypes))
            self.oracle = '{0} \n// {1}'.format(scryfallJSON['card_faces'][0]['oracle_text'], scryfallJSON['card_faces'][1]['oracle_text'])

        else:  # normal, meld, saga, token, double_faced_token, emblem, planar, scheme, vanguard, augment, host
            self.name = scryfallJSON['name']
            self.mana_cost = scryfallJSON['mana_cost']
            self.color = scryfallJSON['colors']
            self.crop_image = scryfallJSON['image_uris']['border_crop']
            self.type_line = scryfallJSON['type_line']
            types = scryfallJSON['type_line'].split("—")
            self.supertype = types[0].split()
            self.subtype = types[1].split() if len(types) > 1 else []
            self.oracle = scryfallJSON['oracle_text']

    def setter(self, **kwargs):
        if 'mana_cost' in kwargs: # kwargs의 key는 str
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

    def showCard(self):
        print("name: {0}\nmana cost: {1}\ncmc: {2}\ncolor: {3}\ncolor_identity: {4}\ntype_line: {5}\nsupertype: {6}\nsubtype: {7}\nset: {8}\nrarity: {9}\nimage: {10}\noracle: {11}".
              format(self.name, self.mana_cost, self.cmc, self.color, self.color_identity, self.type_line, self.supertype, self.subtype, self.set, self.rarity, self.crop_image, self.oracle)
              )


while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.showCard()


