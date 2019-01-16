import re

enchantment_subtypes = tuple("Aura, Cartouche, Curse, Saga, Shrine".split(', '))
artifact_subtypes = tuple("Clue, Contraption, Equipment, Fortification, Treasure, Vehicle".split(', '))
land_subtypes = tuple("Desert, Forest, Gate, Island, Lair, Locus, Mine, Mountain, Plains, Power-Plant, Swamp, Tower, Urza’s".split(', '))
basic_land_subtypes = tuple("Plains, Island, Swamp, Mountain, Forest".split(', '))
planeswalker_subtypes = tuple("Ajani, Aminatou, Angrath, Arlinn, Ashiok, Bolas, Chandra, Dack, Daretti, Domri, Dovin, Elspeth, Estrid, Freyalise, Garruk, Gideon, Huatli, Jace, Jaya, Karn, Kaya, Kiora, Koth, Liliana, Nahiri, Narset, Nissa, Nixilis, Ral, Rowan, Saheeli, Samut, Sarkhan, Sorin, Tamiyo, Teferi, Tezzeret, Tibalt, Ugin, Venser, Vivien, Vraska, Will, Windgrace, Xenagos, Yanggu, Yanling".split(', '))
spell_subtypes = tuple("Arcane, Trap".split(', '))
creature_subtypes = tuple("Advisor, Aetherborn, Ally, Angel, Antelope, Ape, Archer, Archon, Artificer, Assassin, Assembly-Worker, Atog, Aurochs, Avatar, Azra, Badger, Barbarian, Basilisk, Bat, Bear, Beast, Beeble, Berserker, Bird, Blinkmoth, Boar, Bringer, Brushwagg, Camarid, Camel, Caribou, Carrier, Cat, Centaur, Cephalid, Chimera, Citizen, Cleric, Cockatrice, Construct, Coward, Crab, Crocodile, Cyclops, Dauthi, Demon, Deserter, Devil, Dinosaur, Djinn, Dragon, Drake, Dreadnought, Drone, Druid, Dryad, Dwarf, Efreet, Egg, Elder, Eldrazi, Elemental, Elephant, Elf, Elk, Eye, Faerie, Ferret, Fish, Flagbearer, Fox, Frog, Fungus, Gargoyle, Germ, Giant, Gnome, Goat, Goblin, God, Golem, Gorgon, Graveborn, Gremlin, Griffin, Hag, Harpy, Hellion, Hippo, Hippogriff, Homarid, Homunculus, Horror, Horse, Hound, Human, Hydra, Hyena, Illusion, Imp, Incarnation, Insect, Jackal, Jellyfish, Juggernaut, Kavu, Kirin, Kithkin, Knight, Kobold, Kor, Kraken, Lamia, Lammasu, Leech, Leviathan, Lhurgoyf, Licid, Lizard, Manticore, Masticore, Mercenary, Merfolk, Metathran, Minion, Minotaur, Mole, Monger, Mongoose, Monk, Monkey, Moonfolk, Mutant, Myr, Mystic, Naga, Nautilus, Nephilim, Nightmare, Nightstalker, Ninja, Noggle, Nomad, Nymph, Octopus, Ogre, Ooze, Orb, Orc, Orgg, Ouphe, Ox, Oyster, Pangolin, Pegasus, Pentavite, Pest, Phelddagrif, Phoenix, Pilot, Pincher, Pirate, Plant, Praetor, Prism, Processor, Rabbit, Rat, Rebel, Reflection, Rhino, Rigger, Rogue, Sable, Salamander, Samurai, Sand, Saproling, Satyr, Scarecrow, Scion, Scorpion, Scout, Serf, Serpent, Servo, Shade, Shaman, Shapeshifter, Sheep, Siren, Skeleton, Slith, Sliver, Slug, Snake, Soldier, Soltari, Spawn, Specter, Spellshaper, Sphinx, Spider, Spike, Spirit, Splinter, Sponge, Squid, Squirrel, Starfish, Surrakar, Survivor, Tetravite, Thalakos, Thopter, Thrull, Treefolk, Trilobite, Triskelavite, Troll, Turtle, Unicorn, Vampire, Vedalken, Viashino, Volver, Wall, Warrior, Weird, Werewolf, Whale, Wizard, Wolf, Wolverine, Wombat, Worm, Wraith, Wurm, Yeti, Zombie, Zubera".split(', '))
class_subtypes = tuple("Advisor, Ally, Archer, Artificer, Assassin, Barbarian, Berserker, Cleric, Druid, Elder, Flagbearer, Knight, Mercenary, Minion, Monk, Mystic, Ninja, Nomad, Pilot, Pirate, Praetor, Rebel, Rigger, Rogue, Samurai, Scout, Shaman, Soldier, Spellshaper, Warrior, Wizard".split(', '))
race_subtypes = tuple("Ape, Azra, Centaur, Cyclops, Dauthi, Dryad, Dwarf, Elf, Faerie, Giant, Gnome, Goblin, Gorgon, Hag, Human, Kithkin, Kobold, Kor, Merfolk, Metathran, Minotaur, Moonfolk, Naga, Noggle, Ogre, Orc, Ouphe, Satyr, Siren, Slith, Soltari, Surrakar, Thalakos, Troll, Vedalken, Viashino, Werewolf, Yeti, Ainok, Amphin, Aven, Khenra, Kitsune, Leonin, Loxodon, Nantuko/Kraul, Nezumi, Orochi, Rakshasas, Rhox, Wolfir, Aetherborn, Angel, Archon, Avatar, Bringer, Djinn, Efreet, God, Lamia, Nymph, Reflection, Shade, Shapeshifter, Skeleton, Sliver, Specter, Spirit, Thrull, Vampire, Wraith, Zombie, Beeble, Carrier, Cephalid, Demon, Devil, Dragon, Drone, Eldrazi, Elemental, Eye, Gremlin, Harpy, Homarid, Homunculus, Horror, Illusion, Imp, Incarnation, Kirin, Nephilim, Nightmare, Nightstalker, Spawn, Sphinx, Spirit, Thallid, Treefolk, Zubera, Phyrexian, Chimera, Mutant, Orgg, Volver, Weird, Antelope, Ape, Aurochs, Badger, Bat, Bear, Bird, Boar, Camel, Caribou, Cats, Crab, Crocodile, Dinosaur, Elephant, Elk, Ferret, Fish, Fox, Frog, Goat, Hippo, Horse, Hound, Hyena, Insect, Jackal, Jellyfish, Leech, Lizard, Mole, Mongoose, Monkey, Nautilus, Octopus, Ox, Oyster, Pangolin, Rabbit, Rat, Rhino, Sable, Salamander, Scorpion, Sheep, Slug, Snake, Spider, Sponge, Squid, Squirrel, Starfish, Trilobite, Turtle, Whale, Wolf, Wolverine, Wombat, Worm, Atog, Basilisk, Beast, Brushwagg, Camarid, Cockatrice, Drake, Gargoyle, Griffin, Hellion, Hippogriff, Hydra, Kavu, Kraken, Lammasu, Leviathan, Lhurgoyf, Licid, Manticore, Mutant, Pegasus, Phelddagrif, Phoenix, Serpent, Slith, Sliver, Spike, Unicorn, Wurm, Plant, Saproling, Treefolk, Fungus, Germ, Ooze, Assembly-Worker, Blinkmoth, Chimera, Construct, Dreadnought, Gnome, Golem, Juggernaut, Masticore, Myr, Pentavite, Pest, Prism, Servo, Scarecrow, Tetravite, Thopter, Triskelavite, Orb, Sand, Wall".split(', '))


def number_to_colchar(value):

    div = int(value)
    column_label = ''

    while div:
        (div, mod) = divmod(div, 26)
        if mod == 0:
            mod = 26
            div -= 1
        column_label += chr(mod + 64)

    return column_label[::-1]

def colchar_to_number(value):

    col = 0
    for index, item in enumerate(value[::-1]):
        col += (ord(item) - 64) * (26 ** index)

    return col


def determineBlock(setCode):
    pass


def subtypeSort(type_list):
    basic_types = set(type_list) & set(basic_land_subtypes)
    if len(basic_types) >= 2:
        other_types = sorted(list(set(type_list) - set(basic_land_subtypes)), key=typesort)
        basic_types = cyclicOrder(basic_types, basic_land_subtypes)
        return tuple(basic_types + other_types)
    else:
        return tuple(sorted(type_list, key=typesort))


def colorsort(color_list):
    result = cyclicOrder(color_list)
    if result == []:
        return 'Colorless',
    else:
        return result


def cyclicOrder(color_list, sortstd=('W', 'U', 'B', 'R', 'G')):
    W = sortstd[0]
    U = sortstd[1]
    B = sortstd[2]
    R = sortstd[3]
    G = sortstd[4]
    color_set = set(color_list)

    if color_set == set():
        return ()

    if color_set == {W}:
        return W,
    if color_set == {U}:
        return U,
    if color_set == {B}:
        return B,
    if color_set == {R}:
        return R,
    if color_set == {G}:
        return G,

    if color_set == {W,U}:
        return W,U
    if color_set == {U,B}:
        return U,B
    if color_set == {B,R}:
        return B,R
    if color_set == {R,G}:
        return R,G
    if color_set == {G,W}:
        return G,W

    if color_set == {W,B} :
        return W,B
    if color_set == {B,G}:
        return B,G
    if color_set == {G,U}:
        return G,U
    if color_set == {U,R}:
        return U,R
    if color_set == {R,W}:
        return R,W

    if color_set == {W,U,B}:
        return W,U,B
    if color_set == {U,B,R}:
        return U,B,R
    if color_set == {B,R,G}:
        return B,R,G
    if color_set == {R,G,W}:
        return R,G,W
    if color_set == {G,W,U}:
        return G,W,U

    if color_set == {W,B,G}:
        return W,B,G
    if color_set == {U,R,W}:
        return U,R,W
    if color_set == {B,G,U}:
        return B,G,U
    if color_set == {R,W,B}:
        return R,W,B
    if color_set == {G,U,R}:
        return G,U,R

    if color_set == {W,U,B,R}:
        return W,U,B,R
    if color_set == {U,B,R,G}:
        return U,B,R,G
    if color_set == {B,R,G,W}:
        return B,R,G,W
    if color_set == {R,G,W,U}:
        return R,G,W,U
    if color_set == {G,W,U,B}:
        return G,W,U,B

    if color_set == {W,U,B,R,G}:
        return W,U,B,R,G


def typesort(string):  # case sensitive!
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
        return "z" + string


def symbolprettify(string, mode=None):
    if mode != "reverse":
        string = re.sub(r'{W/U}', r'{A}', string)
        string = re.sub(r'{U/B}', r'{D}', string)
        string = re.sub(r'{B/R}', r'{K}', string)
        string = re.sub(r'{R/G}', r'{L}', string)
        string = re.sub(r'{G/W}', r'{E}', string)
        string = re.sub(r'{W/B}', r'{O}', string)
        string = re.sub(r'{B/G}', r'{I}', string)
        string = re.sub(r'{G/U}', r'{M}', string)
        string = re.sub(r'{U/R}', r'{Z}', string)
        string = re.sub(r'{R/W}', r'{S}', string)

        string = re.sub(r'{2/W}', r'{(2/W)}', string)
        string = re.sub(r'{2/U}', r'{(2/U)}', string)
        string = re.sub(r'{2/B}', r'{(2/B)}', string)
        string = re.sub(r'{2/R}', r'{(2/R)}', string)
        string = re.sub(r'{2/G}', r'{(2/G)}', string)

        string = re.sub(r'{W/P}', r'{(W/P)}', string)
        string = re.sub(r'{U/P}', r'{(U/P)}', string)
        string = re.sub(r'{B/P}', r'{(B/P)}', string)
        string = re.sub(r'{R/P}', r'{(R/P)}', string)
        string = re.sub(r'{G/P}', r'{(G/P)}', string)

        string = re.sub(r'{', r'', string)
        string = re.sub(r'}', r'', string)

    if mode == "reverse":
        string = re.sub(r'\(W/P\)', r'{W/P}', string)
        string = re.sub(r'\(U/P\)', r'{U/P}', string)
        string = re.sub(r'\(B/P\)', r'{B/P}', string)
        string = re.sub(r'\(R/P\)', r'{R/P}', string)
        string = re.sub(r'\(G/P\)', r'{G/P}', string)

        string = re.sub(r'\(2/W\)', r'{2/W}', string)
        string = re.sub(r'\(2/U\)', r'{2/U}', string)
        string = re.sub(r'\(2/B\)', r'{2/B}', string)
        string = re.sub(r'\(2/R\)', r'{2/R}', string)
        string = re.sub(r'\(2/G\)', r'{2/G}', string)

        string = re.sub(r'A', r'{W/U}', string)
        string = re.sub(r'D', r'{U/B}', string)
        string = re.sub(r'K', r'{B/R}', string)
        string = re.sub(r'L', r'{R/G}', string)
        string = re.sub(r'E', r'{G/W}', string)
        string = re.sub(r'O', r'{W/B}', string)
        string = re.sub(r'I', r'{B/G}', string)
        string = re.sub(r'M', r'{G/U}', string)
        string = re.sub(r'Z', r'{U/R}', string)
        string = re.sub(r'S', r'{R/W}', string)

        string = re.sub(r'([0-9]+)([^/])', r'{\1}\2', string)
        string = re.sub(r'^([A-Z])([^}])', r'{\1}\2', string)
        string = re.sub(r'([^{])([A-Z])$', r'\1{\2}', string)
        oldstring = ""  # dump value
        count = 0
        while(oldstring != string):  # lookahead assertion 지원X
            oldstring = string
            string = re.sub(r'([^{])([A-Z])([^}])', r'\1{\2}\3', string)

    return string


def prettify(carddict):
    """Card.card to displable gspread row"""

    prettylist = []
    prettylist.append(carddict["name"])
    prettylist.append(symbolprettify(carddict["mana_cost"]))
    prettylist.append(carddict["cmc"])
    prettylist.append(''.join(carddict["color"]))
    prettylist.append(''.join(carddict["color_identity"]))
    prettylist.append(carddict["type_line"])
    prettylist.append('\n'.join(carddict["supertype"]))
    prettylist.append('\n'.join(carddict['subtype']))
    prettylist.append(carddict["set"].upper())
    prettylist.append(carddict["rarity"].title())
    prettylist.append(carddict["power"])
    prettylist.append(carddict["toughness"])
    prettylist.append(carddict["loyalty"])
    prettylist.append(carddict["oracle"])
    prettylist.append(carddict["layout"])
    prettylist.append('\n'.join(carddict["hate"]))
    prettylist.append('\n'.join(carddict["buff"]))
    prettylist.append('\n'.join(carddict["nerf"]))
    prettylist.append('\n'.join(carddict["tags"]))
    prettylist.append("{:.2f}".format(carddict["usd"]))
    prettylist.append(carddict["crop_image"])
    return prettylist


def uglify(cardlist):
    """gspread row to internal Card.Card eatable data"""

    uglylist = []
    uglylist.append(cardlist[0])  # name
    uglylist.append(symbolprettify(cardlist[1], "reverse"))  # mana_cost
    uglylist.append(float(cardlist[2]))  # CMC(=float)
    uglylist.append(tuple(cardlist[3]) if cardlist[3] != "Colorless" else ())  # color(=tuple)
    uglylist.append(tuple(cardlist[4]) if cardlist[4] != "Colorless" else ())  # color_identity(=tuple)
    uglylist.append(cardlist[5])  # type_line
    uglylist.append(tuple(cardlist[6].split("\n")))  # supertype(=tuple)
    uglylist.append(tuple(cardlist[7].split("\n")))  # subtype(=tuple)
    uglylist.append(cardlist[8].lower())  # set
    uglylist.append(cardlist[9].lower())  # rarity
    uglylist.append(tolerInt(cardlist[10]))  # power
    uglylist.append(tolerInt(cardlist[11]))  # toughness
    uglylist.append(tolerInt(cardlist[12]))  # loyalty
    uglylist.append(cardlist[13])  # oracle
    uglylist.append(cardlist[14])  # layout
    uglylist.append(cardlist[15].split("\n"))  # hate(=list)
    uglylist.append(cardlist[16].split("\n"))  # buff(=list)
    uglylist.append(cardlist[17].split("\n"))  # nerf(=list)
    uglylist.append(cardlist[18].split("\n"))  # tags(=list)
    uglylist.append(float(cardlist[19]))  # usd(=float)
    uglylist.append(cardlist[20])  # crop_image

    return uglylist

def tolerInt(string):
    if string.isdigit():
        return int(string)
    else:
        return string


if __name__ == '__main__':
    print(symbolprettify("{11}{B}{R}{G}{W/B}{R/W}{2/B}{G/P} // {R}{R}{R}{R}"))
    print(symbolprettify("11BRGOS(2/B)(G/P) // RRRR", "reverse"))

    alist = ['Swamp', 'Knight', 'Island']
    print(alist)
    alist = subtypeSort(alist)
    print(alist)
