import ScryfallIO

enchantment_subtypes = "Aura, Cartouche, Curse, Saga, Shrine".split(', ')
artifact_subtypes = "Clue, Contraption, Equipment, Fortification, Treasure, Vehicle".split(', ')
land_subtypes = "Desert, Forest, Gate, Island, Lair, Locus, Mine, Mountain, Plains, Power-Plant, Swamp, Tower, Urza’s".split(', ')
basic_land_subtypes = "Forest, Island, Mountain, Plains, Swamp".split(', ')
planeswalker_subtypes = "Ajani, Aminatou, Angrath, Arlinn, Ashiok, Bolas, Chandra, Dack, Daretti, Domri, Dovin, Elspeth, Estrid, Freyalise, Garruk, Gideon, Huatli, Jace, Jaya, Karn, Kaya, Kiora, Koth, Liliana, Nahiri, Narset, Nissa, Nixilis, Ral, Rowan, Saheeli, Samut, Sarkhan, Sorin, Tamiyo, Teferi, Tezzeret, Tibalt, Ugin, Venser, Vivien, Vraska, Will, Windgrace, Xenagos, Yanggu, Yanling".split(', ')
spell_subtypes = "Arcane, Trap".split(', ')
creature_subtypes = "Advisor, Aetherborn, Ally, Angel, Antelope, Ape, Archer, Archon, Artificer, Assassin, Assembly-Worker, Atog, Aurochs, Avatar, Azra, Badger, Barbarian, Basilisk, Bat, Bear, Beast, Beeble, Berserker, Bird, Blinkmoth, Boar, Bringer, Brushwagg, Camarid, Camel, Caribou, Carrier, Cat, Centaur, Cephalid, Chimera, Citizen, Cleric, Cockatrice, Construct, Coward, Crab, Crocodile, Cyclops, Dauthi, Demon, Deserter, Devil, Dinosaur, Djinn, Dragon, Drake, Dreadnought, Drone, Druid, Dryad, Dwarf, Efreet, Egg, Elder, Eldrazi, Elemental, Elephant, Elf, Elk, Eye, Faerie, Ferret, Fish, Flagbearer, Fox, Frog, Fungus, Gargoyle, Germ, Giant, Gnome, Goat, Goblin, God, Golem, Gorgon, Graveborn, Gremlin, Griffin, Hag, Harpy, Hellion, Hippo, Hippogriff, Homarid, Homunculus, Horror, Horse, Hound, Human, Hydra, Hyena, Illusion, Imp, Incarnation, Insect, Jackal, Jellyfish, Juggernaut, Kavu, Kirin, Kithkin, Knight, Kobold, Kor, Kraken, Lamia, Lammasu, Leech, Leviathan, Lhurgoyf, Licid, Lizard, Manticore, Masticore, Mercenary, Merfolk, Metathran, Minion, Minotaur, Mole, Monger, Mongoose, Monk, Monkey, Moonfolk, Mutant, Myr, Mystic, Naga, Nautilus, Nephilim, Nightmare, Nightstalker, Ninja, Noggle, Nomad, Nymph, Octopus, Ogre, Ooze, Orb, Orc, Orgg, Ouphe, Ox, Oyster, Pangolin, Pegasus, Pentavite, Pest, Phelddagrif, Phoenix, Pilot, Pincher, Pirate, Plant, Praetor, Prism, Processor, Rabbit, Rat, Rebel, Reflection, Rhino, Rigger, Rogue, Sable, Salamander, Samurai, Sand, Saproling, Satyr, Scarecrow, Scion, Scorpion, Scout, Serf, Serpent, Servo, Shade, Shaman, Shapeshifter, Sheep, Siren, Skeleton, Slith, Sliver, Slug, Snake, Soldier, Soltari, Spawn, Specter, Spellshaper, Sphinx, Spider, Spike, Spirit, Splinter, Sponge, Squid, Squirrel, Starfish, Surrakar, Survivor, Tetravite, Thalakos, Thopter, Thrull, Treefolk, Trilobite, Triskelavite, Troll, Turtle, Unicorn, Vampire, Vedalken, Viashino, Volver, Wall, Warrior, Weird, Werewolf, Whale, Wizard, Wolf, Wolverine, Wombat, Worm, Wraith, Wurm, Yeti, Zombie, Zubera".split(', ')
class_subtypes = "Advisor, Ally, Archer, Artificer, Assassin, Barbarian, Berserker, Cleric, Druid, Elder, Flagbearer, Knight, Mercenary, Minion, Monk, Mystic, Ninja, Nomad, Pilot, Pirate, Praetor, Rebel, Rigger, Rogue, Samurai, Scout, Shaman, Soldier, Spellshaper, Warrior, Wizard".split(', ')
race_subtypes = "Ape, Azra, Centaur, Cyclops, Dauthi, Dryad, Dwarf, Elf, Faerie, Giant, Gnome, Goblin, Gorgon, Hag, Human, Kithkin, Kobold, Kor, Merfolk, Metathran, Minotaur, Moonfolk, Naga, Noggle, Ogre, Orc, Ouphe, Satyr, Siren, Slith, Soltari, Surrakar, Thalakos, Troll, Vedalken, Viashino, Werewolf, Yeti, Ainok, Amphin, Aven, Khenra, Kitsune, Leonin, Loxodon, Nantuko/Kraul, Nezumi, Orochi, Rakshasas, Rhox, Wolfir, Aetherborn, Angel, Archon, Avatar, Bringer, Djinn, Efreet, God, Lamia, Nymph, Reflection, Shade, Shapeshifter, Skeleton, Sliver, Specter, Spirit, Thrull, Vampire, Wraith, Zombie, Beeble, Carrier, Cephalid, Demon, Devil, Dragon, Drone, Eldrazi, Elemental, Eye, Gremlin, Harpy, Homarid, Homunculus, Horror, Illusion, Imp, Incarnation, Kirin, Nephilim, Nightmare, Nightstalker, Spawn, Sphinx, Spirit, Thallid, Treefolk, Zubera, Phyrexian, Chimera, Mutant, Orgg, Volver, Weird, Antelope, Ape, Aurochs, Badger, Bat, Bear, Bird, Boar, Camel, Caribou, Cats, Crab, Crocodile, Dinosaur, Elephant, Elk, Ferret, Fish, Fox, Frog, Goat, Hippo, Horse, Hound, Hyena, Insect, Jackal, Jellyfish, Leech, Lizard, Mole, Mongoose, Monkey, Nautilus, Octopus, Ox, Oyster, Pangolin, Rabbit, Rat, Rhino, Sable, Salamander, Scorpion, Sheep, Slug, Snake, Spider, Sponge, Squid, Squirrel, Starfish, Trilobite, Turtle, Whale, Wolf, Wolverine, Wombat, Worm, Atog, Basilisk, Beast, Brushwagg, Camarid, Cockatrice, Drake, Gargoyle, Griffin, Hellion, Hippogriff, Hydra, Kavu, Kraken, Lammasu, Leviathan, Lhurgoyf, Licid, Manticore, Mutant, Pegasus, Phelddagrif, Phoenix, Serpent, Slith, Sliver, Spike, Unicorn, Wurm, Plant, Saproling, Treefolk, Fungus, Germ, Ooze, Assembly-Worker, Blinkmoth, Chimera, Construct, Dreadnought, Gnome, Golem, Juggernaut, Masticore, Myr, Pentavite, Pest, Prism, Servo, Scarecrow, Tetravite, Thopter, Triskelavite, Orb, Sand, Wall".split(', ')
race_subtypes.sort()

def _landsort(list):
    pass


def _colorsort(list):
    color_set = set(list)
    if color_set == set("WU"):
        return ['W', 'U']
    if color_set == set("UB"):
        return ['U', 'B']
    if color_set == set("BR"):
        return ['B', 'R']
    if color_set == set("RG"):
        return ['R', 'G']
    if color_set == set("GW"):
        return ['G', 'W']
    if color_set == set("WB"):
        return ['W', 'B']
    if color_set == set("BG"):
        return ['B', 'G']
    if color_set == set("GU"):
        return ['G', 'U']
    if color_set == set("UR"):
        return ['U', 'R']
    if color_set == set("RW"):
        return ['R', 'W']

    if color_set == set("WUB"):
        return ['W', 'U', 'B']
    if color_set == set("UBR"):
        return ['U', 'B', 'R']
    if color_set == set("BRG"):
        return ['B', 'R', 'G']
    if color_set == set("RGW"):
        return ['R', 'G', 'W']
    if color_set == set("GWU"):
        return ['G', 'W', 'U']

    if color_set == set("WBG"):
        return ['W', 'B', 'G']
    if color_set == set("URW"):
        return ['U', 'R', 'W']
    if color_set == set("BGU"):
        return ['B', 'G', 'U']
    if color_set == set("RWB"):
        return ['R', 'W', 'B']
    if color_set == set("GUR"):
        return ['G', 'U', 'R']

    if color_set == set("WUBR"):
        return ['W', 'U', 'B', 'R']
    if color_set == set("UBRG"):
        return ['U', 'B', 'R', 'G']
    if color_set == set("BRGW"):
        return ['B', 'R', 'G', 'W']
    if color_set == set("RGWU"):
        return ['R', 'G', 'W', 'U']
    if color_set == set("GWUB"):
        return ['G', 'W', 'U', 'B']

    if color_set == set("WUBRG"):
        return ['W', 'U', 'B', 'R', 'G']


def _typesort(string):  # case sensitive!
    if string == "Legendary":
        return "a" + string
    if string == ("Snow" or "Basic" or "World"):
        return "b" + string
    if string == "Tribal":
        return "c" + string
    if string == "Enchantment":
        return "d" + string
    if string == "Artifact":
        return "e" + string
    if string == "Land":
        return "f" + string
    if string == ("Instant" or "Sorcery"):
        return "g" + string
    if string == "Creature":
        return "h" + string
    if string in land_subtypes:
        return "i" + string
    if string in race_subtypes:
        return "j" + string
    if string in class_subtypes:
        return "k" + string
    else:  # nonland noncreature subtypes
        return "z" + string;


class Card():
    def __init__(self, data=None):
        if type(data) == None:  # empty initialization
            self.name = ""
            self.mana_cost = ""
            self.cmc = ""
            self.color = []
            self.color_identity = []
            self.type_line = ""
            self.supertype = []
            self.subtype = []
            self.set = ""
            self.rarity = ""
            self.crop_image = ""
            self.oracle = ""
            self.layout = ""
            self.hate = []
            self.buff = []
            self.nerf = []
            self.tags = []
            self.id = ""

        if type(data) == list:  # data is Google spreadsheet row
            self.name = data[0]
            self.mana_cost = data[1]
            self.cmc = data[2]
            self.color = eval(data[3])
            self.color_identity = eval(data[4])
            self.type_line = data[5]
            self.supertype = eval(data[6])
            self.subtype = eval(data[7])
            self.set = data[8]
            self.rarity = data[9]
            self.crop_image = data[10]
            self.oracle = data[11]
            self.layout = data[12]
            self.hate = eval(data[13])
            self.buff = eval(data[14])
            self.nerf = eval(data[15])
            self.tags = eval(data[16])
            self.id = data[17]

        if type(data) == dict:  # data is JSON from Scryfall
            self.layout = data['layout']
            if self.layout == 'transform':
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
                self.oracle = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.layout == 'split':
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
                self.oracle = '{0} \n// {1}'.format(data['card_faces'][0]['oracle_text'], data['card_faces'][1]['oracle_text'])

            elif self.layout == 'flip':
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
                self.oracle = data['oracle_text']

            self.hate = []
            self.buff = []
            self.nerf = []
            self.tags = []  # fixing, infect, selfmill, big, small, ... ...
            self.id = data['id']
            self.cmc = data['cmc']
            self.color_identity = data['color_identity']
            self.set = data['set'].upper()
            self.rarity = data['rarity']

            self.color_identity = _colorsort(self.color_identity)
            self.color = _colorsort(self.color)
            self.supertype.sort(key=_typesort)
            self.subtype.sort(key=_typesort)


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
        cardlist = [self.name, self.mana_cost, self.cmc, str(self.color), str(self.color_identity), self.type_line, str(self.supertype), str(self.subtype), self.set, self.rarity, self.crop_image, self.oracle, self.layout, str(self.hate), str(self.buff), str(self.nerf), str(self.tags), self.id]
        return cardlist

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


