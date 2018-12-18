import ScryfallIO

class Card():
    def __init__(self, scryfallJSON):
        self.name = scryfallJSON['name']
        self.mana_cost = scryfallJSON['mana_cost']
        self.cmc = scryfallJSON['cmc']
        self.color = scryfallJSON['colors']
        self.color_identity = scryfallJSON['color_identity']
        self.crop_image = scryfallJSON['image_uris']['border_crop']
        self.type = scryfallJSON['type_line']
        self.set = scryfallJSON['set']
        self.rarity = scryfallJSON['rarity']
        self.oracle = scryfallJSON['oracle_text']
        self.hate = []
        self.buff = []
        self.nerf = []
        self.tags = [] #fixing, infect, selfmill, big, small, ... ...

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
            self.type = kwargs['type']

        if 'set' in kwargs:
            self.set = kwargs['set']
            new_card = ScryfallIO.getCard(self.name, self.set)
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
        if 3 in kwargs:
            print("key can be integer")

    def remover(self, **kwargs):
        pass

    def showCard(self):
        print('''name: {0}
mana cost: {1}
cmc: {2}
color: {3}
color_identity: {4}
type: {5}
set: {6}
rarity: {7}
image: {8}'''.format(self.name,
                     self.mana_cost,
                     self.cmc,
                     self.color,
                     self.color_identity,
                     self.type,
                     self.set,
                     self.rarity,
                     self.crop_image
                     )
        )

    def showType(self):
        print('''name: {0}
mana cost: {1}
cmc: {2}
color: {3}
color_identity: {4}
type: {5}
set: {6}
rarity: {7}'''.format(type(self.name),
                      type(self.mana_cost),
                      type(self.cmc),
                      type(self.color),
                      type(self.color_identity),
                      type(self.type),
                      type(self.set),
                      type(self.rarity)
                      )
        )




while __name__ == '__main__':
    searchquery = input("search for: ")
    if searchquery == "quit":
        break
    card = Card(ScryfallIO.getCard(searchquery))
    card.showCard()
    card.setter(cmc = 9.0) # if "set", SyntaxError: keyword can't be an expression
    card.showCard()

