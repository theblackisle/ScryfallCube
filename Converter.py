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
        return basic_types + other_types
    else:
        return sorted(type_list, key=typesort)


def colorsort(color_list):
    result = cyclicOrder(color_list)
    if result == ():
        return 'C',
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

    else:
        print("method cyclicOrder: check the input again")
        raise ValueError


def color_to_nick(color_set):
    nick = ""
    priority = -1

    if color_set == ():
        priority = 0
        nick = "Colorless"

    if color_set == ('W',):
        priority = 1
        nick = "White"
    if color_set == ('U',):
        priority = 2
        nick = "Blue"
    if color_set == ('B',):
        priority = 3
        nick = "Black"
    if color_set == ('R',):
        priority = 4
        nick = "Red"
    if color_set == ('G',):
        priority = 5
        nick = "Green"

    if color_set == ('W', 'U'):
        priority = 6
        nick = "Azorius"
    if color_set == ('U', 'B'):
        priority = 7
        nick = "Dimir"
    if color_set == ('B', 'R'):
        priority = 8
        nick = 'Rakdos'
    if color_set == ('R', 'G'):
        priority = 9
        nick = "Gruul"
    if color_set == ('G', 'W'):
        priority = 10
        nick = "Selesnya"

    if color_set == ('W', 'B'):
        priority = 11
        nick = "Orzhov"
    if color_set == ('B', 'G'):
        priority = 12
        nick = "Golgari"
    if color_set == ('G', 'U'):
        priority = 13
        nick = "Simic"
    if color_set == ('U', 'R'):
        priority = 14
        nick = "Izzet"
    if color_set == ('R', 'W'):
        priority = 15
        nick = "Boros"

    if color_set == ('W', 'U', 'B'):
        priority = 16
        nick = "Esper"
    if color_set == ('U', 'B', 'R'):
        priority = 17
        nick = "Grixis"
    if color_set == ('B', 'R', 'G'):
        priority = 18
        nick = "Jund"
    if color_set == ('R', 'G', 'W'):
        priority = 19
        nick = "Naya"
    if color_set == ('G', 'W', 'U'):
        priority = 20
        nick = "Bant"

    if color_set == ('W', 'B', 'G'):
        priority = 21
        nick = "Abzan"
    if color_set == ('U', 'R', 'W'):
        priority = 22
        nick = "Jeskai"
    if color_set == ('B', 'G', 'U'):
        priority = 23
        nick = "Sultai"
    if color_set == ('R', 'W', 'B'):
        priority = 24
        nick = "Mardu"
    if color_set == ('G', 'U', 'R'):
        priority = 25
        nick = "Temur"

    if color_set == ('W', 'U', 'B', 'R'):
        priority = 26
        nick = "Greenless"
    if color_set == ('U', 'B', 'R', 'G'):
        priority = 27
        nick = "Whiteless"
    if color_set == ('B', 'R', 'G', 'W'):
        priority = 28
        nick = "Blueless"
    if color_set == ('R', 'G', 'W', 'U'):
        priority = 29
        nick = "Blackless"
    if color_set == ('G', 'W', 'U', 'B'):
        priority = 30
        nick = "Redless"

    if color_set == ('W', 'U', 'B', 'R', 'G'):
        priority = 31
        nick = "5C"

    return (priority, nick)


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


def mana_to_cmc(mana):
    """
    :param mana: uglyfied mana cost from Scryfall JSON
    :return: cmc(int) is cmc calculated for param
    """
    if mana is "":
        return 0

    generic = re.findall(r'{\d+}', mana)
    if len(generic) != 0:
        generic_cmc = int(re.sub(r'{|}', '', generic[0]))
    else:
        generic_cmc = 0

    colored_cmc = len(re.findall(r'{W/U}|{U/B}|{B/R}|{R/G}|{G/W}|{W/B}|{B/G}|{G/U}|{U/R}|{R/W}|{2/W}|{2/U}|{2/B}|{2/R}|{2/G}|{W/P}|{U/P}|{B/P}|{R/P}|{G/P}|{W}|{U}|{B}|{R}|{G}|{C}', mana))

    return generic_cmc + colored_cmc

def mana_sum(mana1, mana2):
    """
    :param mana1, mana2: uglyfied mana cost from Scryfall JSON
    :return: sum(str) is mana added
    """
    mana = mana1+mana2
    x = re.findall(r'{X}', mana)
    x_sum = ""
    for item in x:
        x_sum += item

    generic = re.findall(r'{\d+}', mana)
    generic_sum = 0
    if len(generic) > 0:
        for item in generic:
            generic_sum += int(re.sub(r'{|}', '', item))
        generic_sum = "{%d}" % (generic_sum)
    if len(generic) == 0 or (generic_sum == "{0}" and len(x) > 0):
        generic_sum = ""

    # 아직 hybrid, twobrid, pyrexian mana를 color sort할 필요가 있는 카드(=split)가 mtg 내에 없음. 미구현
    hybrid = re.findall(r'{W/U}|{U/B}|{B/R}|{R/G}|{G/W}|{W/B}|{B/G}|{G/U}|{U/R}|{R/W}|{2/W}|{2/U}|{2/B}|{2/R}|{2/G}|{W/P}|{U/P}|{B/P}|{R/P}|{G/P}|{C}', mana)
    hybrid_sum = ""
    for item in hybrid:
        hybrid_sum += item

    color = {}
    color["W"] = re.findall(r'{W}', mana)
    color["U"] = re.findall(r'{U}', mana)
    color["B"] = re.findall(r'{B}', mana)
    color["R"] = re.findall(r'{R}', mana)
    color["G"] = re.findall(r'{G}', mana)
    present_color = cyclicOrder([item for item in ('W', 'U', 'B', 'R', 'G') if len(color[item]) > 0])

    color_sum = ""
    for item in present_color:
        color_sum += ("{%s}" % item) * len(color[item])

    return x_sum + generic_sum + hybrid_sum + color_sum

def mana_to_color(mana):
    color = {}
    color["W"] = re.findall(r'{W}', mana)
    color["U"] = re.findall(r'{U}', mana)
    color["B"] = re.findall(r'{B}', mana)
    color["R"] = re.findall(r'{R}', mana)
    color["G"] = re.findall(r'{G}', mana)
    return cyclicOrder([item for item in ('W', 'U', 'B', 'R', 'G') if len(color[item]) > 0])

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

        string = re.sub(r'^([A-Z]|[0-9]+)$', r'{\1}', string)  # 단일위치
        string = re.sub(r'^([A-Z]|[0-9]+)', r'{\1}', string)  # 선위치
        string = re.sub(r'([A-Z]|[0-9]+)$', r'{\1}', string)  # 후위치
        new_string = re.sub(r'([^{])([A-Z]|[0-9]+)([^}])', r'\1{\2}\3', string)  # 중위치
        while new_string != string:  # lookahead assertion 지원X: loop으로 구현
            string = new_string
            new_string = re.sub(r'([^{])([A-Z]|[0-9]+)([^}])', r'\1{\2}\3', string)

    return string


def prettify(card):
    """Card.card to displable gspread row"""

    properties = card.properties
    actual = card.actual

    prettylist = [""]*19
    prettylist[14] = '\n'.join(actual["nominal"]["buff"])
    prettylist[15] = '\n'.join(actual["nominal"]["nerf"])
    prettylist[16] = '\n'.join(actual["nominal"]["tags"])
    prettylist[4] = ''.join(properties["nominal"]["color_identity"])
    prettylist[7] = properties["nominal"]["set"]
    prettylist[8] = properties["nominal"]["rarity"]
    prettylist[17] = "{:.2f}".format(properties["nominal"]["usd"])
    prettylist[13] = properties["nominal"]["layout"]

    if properties["nominal"]["layout"] == 'Transform':
        prettylist[0] = '{}\n// {}'.format(properties["front"]["name"], properties["back"]["name"])
        print(prettylist[0])
        # nominal name은 전달X; 재구성해서 사용
        prettylist[1] = '{}{}'.format(symbolprettify(properties["nominal"]["mana_cost"]), symbolprettify(actual["nominal"]["mana_cost"]))
        prettylist[2] = '{}{}'.format(properties["nominal"]["cmc"], actual["nominal"]["cmc"])
        prettylist[3] = '{}\n{}'.format(''.join(properties["front"]["color"]),
                                        ''.join(properties["back"]["color"]))
        prettylist[5] = '{}{}\n{}{}'.format(' '.join(properties["front"]["supertype"]),
                                            '+'+' '.join(actual["front"]["supertype"]) if actual["front"]["supertype"] != "" else "",
                                            ' '.join(properties["back"]["supertype"]),
                                            '+'+' '.join(actual["back"]["supertype"]) if actual["back"]["supertype"] != "" else "")
        prettylist[6] = '{}{}\n{}{}'.format(' '.join(properties["front"]["subtype"]),
                                            '+'+' '.join(actual["front"]["subtype"]) if actual["front"]["subtype"] != "" else "",
                                            ' '.join(properties["back"]["subtype"]),
                                            '+'+' '.join(actual["back"]["subtype"]) if actual["back"]["subtype"] != "" else "")
        prettylist[9] = '{}{}\n{}{}'.format(properties["front"]["power"], actual["front"]["power"],
                                            properties["back"]["power"], actual["back"]["power"])
        prettylist[10] = '{}{}\n{}{}'.format(properties["front"]["toughness"], actual["front"]["toughness"],
                                             properties["back"]["toughness"], actual["back"]["toughness"])
        prettylist[11] = '{}{}\n{}{}'.format(properties["front"]["loyalty"], actual["front"]["loyalty"],
                                             properties["back"]["loyalty"], actual["back"]["loyalty"])
        prettylist[12] = '{}\n// {}'.format(properties["front"]["oracle"],
                                            properties["back"]["oracle"])
        prettylist[18] = '{}\n{}'.format(properties["front"]["crop_image"],
                                         properties["back"]["crop_image"])

    elif properties["nominal"]["layout"] == 'Split':
        prettylist[0] = '{}\n// {}'.format(properties["left"]["name"], properties["right"]["name"])
        # nominal name은 전달X; 재구성해서 사용
        prettylist[1] = '{}{}\n{}{}\n{}{}'.format(symbolprettify(properties["nominal"]["mana_cost"]), symbolprettify(actual["nominal"]["mana_cost"]),
                                                  symbolprettify(properties["left"]["mana_cost"]), symbolprettify(actual["left"]["mana_cost"]),
                                                  symbolprettify(properties["right"]["mana_cost"]), symbolprettify(actual["right"]["mana_cost"]))
        prettylist[2] = '{}{}\n{}{}\n{}{}'.format(properties["nominal"]["cmc"], actual["nominal"]["cmc"],
                                                  properties["left"]["cmc"], actual["left"]["cmc"],
                                                  properties["right"]["cmc"], actual["right"]["cmc"])
        prettylist[3] = '{}\n{}\n{}'.format(''.join(properties["nominal"]["color"]),
                                            ''.join(properties["left"]["color"]),
                                            ''.join(properties["right"]["color"]))
        prettylist[5] = '{}{}\n{}{}\n{}{}'.format(' '.join(properties["nominal"]["supertype"]),
                                                  '+'+' '.join(actual["nominal"]["supertype"]) if actual["nominal"]["supertype"] != "" else "",
                                                  ' '.join(properties["left"]["supertype"]),
                                                  '+'+' '.join(actual["left"]["supertype"]) if actual["left"]["supertype"] != "" else "",
                                                  ' '.join(properties["right"]["supertype"]),
                                                  '+'+' '.join(actual["right"]["supertype"]) if actual["right"]["supertype"] != "" else "")
        prettylist[6] = '{}{}\n{}{}\n{}{}'.format(' '.join(properties["nominal"]["subtype"]),
                                                  '+'+' '.join(actual["nominal"]["subtype"]) if actual["nominal"]["subtype"] != "" else "",
                                                  ' '.join(properties["left"]["subtype"]),
                                                  '+'+' '.join(actual["left"]["subtype"]) if actual["left"]["subtype"] != "" else "",
                                                  ' '.join(properties["right"]["subtype"]),
                                                  '+'+' '.join(actual["right"]["subtype"]) if actual["right"]["subtype"] != "" else "")
        # Split card의 nominal supertype/subtype은 전달x; 재구성해서 사용

        prettylist[9] = ""  # power
        prettylist[10] = ""  # toughness
        prettylist[11] = ""  # loyalty
        prettylist[12] = '{}\n// {}'.format(properties["left"]["oracle"],
                                            properties["right"]["oracle"])
        prettylist[18] = properties["nominal"]["crop_image"]

    elif properties["nominal"]["layout"] == 'Flip':
        prettylist[0] = '{}\n// {}'.format(properties["top"]["name"], properties["bottom"]["name"])
        # nominal name은 전달X; 재구성해서 사용
        prettylist[1] = symbolprettify(properties["nominal"]["mana_cost"])
        prettylist[2] = properties["nominal"]["cmc"]
        prettylist[3] = ''.join(properties["nominal"]["color"])
        prettylist[5] = '{}{}\n{}{}'.format(' '.join(properties["top"]["supertype"]),
                                            '+'+' '.join(actual["top"]["supertype"]) if actual["top"]["supertype"] != "" else "",
                                            ' '.join(properties["bottom"]["supertype"]),
                                            '+'+' '.join(actual["bottom"]["supertype"]) if actual["bottom"]["supertype"] != "" else "",)
        prettylist[6] = '{}{}\n{}{}'.format(' '.join(properties["top"]["subtype"]),
                                            '+'+' '.join(actual["top"]["subtype"]) if actual["top"]["subtype"] != "" else "",
                                            ' '.join(properties["bottom"]["subtype"]),
                                            '+'+' '.join(actual["bottom"]["subtype"]) if actual["top"]["subtype"] != "" else "",)
        prettylist[9] = '{}{}\n{}{}'.format(properties["top"]["power"], actual["top"]["power"],
                                            properties["bottom"]["power"], actual["bottom"]["power"])
        prettylist[10] = '{}{}\n{}{}'.format(properties["top"]["toughness"], actual["top"]["toughness"],
                                             properties["bottom"]["toughness"], actual["bottom"]["toughness"])
        prettylist[11] = ''
        prettylist[12] = '{}\n// {}'.format(properties["top"]["oracle"],
                                            properties["bottom"]["oracle"])
        prettylist[18] = properties["nominal"]["crop_image"]

    else:
        prettylist[0] = properties["nominal"]["name"]
        prettylist[1] = '{}{}'.format(symbolprettify(properties["nominal"]["mana_cost"]), symbolprettify(actual["nominal"]["mana_cost"]))
        prettylist[2] = '{}{}'.format(properties["nominal"]["cmc"], actual["nominal"]["cmc"])
        prettylist[3] = ''.join(properties["nominal"]["color"])
        prettylist[5] = '{}{}'.format(' '.join(properties["nominal"]["supertype"]),
                                      '+'+' '.join(actual["nominal"]["supertype"]) if actual["nominal"]["supertype"] != "" else "")
        prettylist[6] = '{}{}'.format(' '.join(properties["nominal"]['subtype']),
                                      '+'+' '.join(actual["nominal"]["subtype"]) if actual["nominal"]["subtype"] != "" else "")
        prettylist[9] = '{}{}'.format(properties["nominal"]["power"], actual["nominal"]["power"])
        prettylist[10] = '{}{}'.format(properties["nominal"]["toughness"], actual["nominal"]["toughness"])
        prettylist[11] = '{}{}'.format(properties["nominal"]["loyalty"], actual["nominal"]["loyalty"])
        prettylist[12] = properties["nominal"]["oracle"]
        prettylist[18] = properties["nominal"]["crop_image"]

    return prettylist

def uglify(cardlist):
    """gspread row to internal Card.Card eatable data"""

    uglydict = {'properties': {'nominal': {}}, 'actual': {'nominal': {}}}

    uglydict['actual']['nominal']["buff"] = (cardlist[14].split("\n"))  # buff(=list)
    uglydict['actual']['nominal']["nerf"] = (cardlist[15].split("\n"))  # nerf(=list)
    uglydict['actual']['nominal']["tags"] = (cardlist[16].split("\n"))  # tags(=list)

    uglydict['properties']['nominal']['color_identity'] = tuple(cardlist[4]) if cardlist[4] != "C" else ()  # color_identity(=tuple)
    uglydict['properties']['nominal']['set'] = cardlist[7]  # set(=str, upper()-ed)
    uglydict['properties']['nominal']['rarity'] = cardlist[8]  # rarity(=str, title()-ed)
    uglydict['properties']['nominal']['usd'] = float(cardlist[17])  # usd(=float)

    uglydict['properties']['nominal']['layout'] = cardlist[13]  # layout(=str)
    if uglydict['properties']['nominal']['layout'] == 'Transform':
        uglydict['properties']['front'] = uglydict['properties']['back'] = {}
        uglydict['actual']['front'] = uglydict['actual']['back'] = {}

        split_temp = cardlist[0].split("\n// ")
        uglydict['properties']['front']['name'] = split_temp[0]  # name(=str)
        uglydict['properties']['back']['name'] = split_temp[1]
        uglydict['properties']['nominal']['name'] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = re.split(r'(?=[\-\+])', cardlist[1])
        uglydict['properties']['nominal']['mana_cost'] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['mana_cost'] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+])', cardlist[2])
        uglydict['properties']['nominal']['cmc'] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['cmc'] = split_temp[1]

        split_temp = cardlist[3].split("\n")
        uglydict['properties']['front']['color'] = tuple(split_temp[0]) if split_temp[0] != "C" else ()  # color(=tuple)
        uglydict['properties']['back']['color'] = tuple(split_temp[1]) if split_temp[1] != "C" else ()

        split_temp = cardlist[5].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['front']['supertype'] = tuple(split_subtemp[0].split(' '))  # supertype(=tuple)
        if len(split_subtemp) > 1:
            uglydict['actual']['front']['supertype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['back']['supertype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['back']['supertype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[6].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['front']['subtype'] = tuple(split_subtemp[0].split(' '))  # subtype(=tuple)
        if len(split_subtemp) > 1:
            uglydict['actual']['front']['subtype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['back']['subtype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['back']['subtype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[9].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['front']['power'] = split_subtemp[0]  # power(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['front']['power'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['back']['power'] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict['actual']['back']['power'] = split_subtemp[1]

        split_temp = cardlist[10].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['front']['toughness'] = split_subtemp[0]  # toughness(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['front']['toughness'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['back']['toughness'] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict['actual']['back']['toughness'] = split_subtemp[1]

        split_temp = cardlist[11].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['front']['loyalty'] = split_subtemp[0]  # loyalty(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['front']['loyalty'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['back']['loyalty'] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict['actual']['back']['loyalty'] = split_subtemp[1]

        split_temp = cardlist[12].split("\n// ")
        uglydict['properties']['front']['oracle'] = split_temp[0]  # oracle(=str)
        uglydict['properties']['back']['oracle'] = split_temp[1]

        split_temp = cardlist[18].split("\n")
        uglydict['properties']['front']['crop_image'] = split_temp[0]  # crop_image(=str, url)
        uglydict['properties']['back']['crop_image'] = split_temp[1]

    elif uglydict['properties']['nominal']['layout'] == 'Split':
        uglydict['properties']['left'] = uglydict['properties']['right'] = {}
        uglydict['actual']['left'] = uglydict['actual']['right'] = {}

        split_temp = cardlist[0].split("\n// ")
        uglydict['properties']['left']['name'] = split_temp[0]  # name(=str)
        uglydict['properties']['right']['name'] = split_temp[1]
        uglydict['properties']['nominal']['name'] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = cardlist[1].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['nominal']['mana_cost'] = symbolprettify(split_subtemp[0], "reverse")  # mana_cost(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['nominal']['mana_cost'] = symbolprettify(split_subtemp[1], "reverse")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['left']['mana_cost'] = symbolprettify(split_subtemp[0], "reverse")
        if len(split_subtemp) > 1:
            uglydict['actual']['left']['mana_cost'] = symbolprettify(split_subtemp[1], "reverse")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[2])
        uglydict['properties']['right']['mana_cost'] = symbolprettify(split_subtemp[0], "reverse")
        if len(split_subtemp) > 1:
            uglydict['actual']['right']['mana_cost'] = symbolprettify(split_subtemp[1], "reverse")

        split_temp = cardlist[2].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['nominal']['cmc'] = int(split_subtemp[0])  # CMC(=int)
        if len(split_subtemp) > 1:
            uglydict['actual']['nominal']['cmc'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['left']['cmc'] = int(split_subtemp[0])
        if len(split_subtemp) > 1:
            uglydict['actual']['left']['cmc'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[2])
        uglydict['properties']['right']['cmc'] = int(split_subtemp[0])
        if len(split_subtemp) > 1:
            uglydict['actual']['right']['cmc'] = split_subtemp[1]

        split_temp = cardlist[3].split("\n")
        uglydict['properties']['nominal']['color'] = tuple(split_temp[0]) if split_temp[0] != "C" else ()  # color(=tuple)
        uglydict['properties']['left']['color'] = tuple(split_temp[1]) if split_temp[1] != "C" else ()
        uglydict['properties']['right']['color'] = tuple(split_temp[2]) if split_temp[2] != "C" else ()

        split_temp = cardlist[5].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['nominal']['supertype'] = tuple(split_subtemp[0].split(' '))  # supertype(=tuple)
        if len(split_subtemp) > 1:
            uglydict['actual']['nominal']['supertype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['left']['supertype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['left']['supertype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[2])
        uglydict['properties']['right']['supertype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['right']['supertype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[6].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['nominal']['subtype'] = tuple(split_subtemp[0].split(' '))  # subtype(=tuple)
        if len(split_subtemp) > 1:
            uglydict['actual']['nominal']['subtype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['left']['subtype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['left']['subtype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[2])
        uglydict['properties']['right']['subtype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['right']['subtype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[12].split("\n// ")
        uglydict['properties']['left']['oracle'] = split_temp[0]  # oracle(=str)
        uglydict['properties']['right']['oracle'] = split_temp[1]

        uglydict['properties']['nominal']['crop_image'] = cardlist[18]  # crop_image(=str, url)

    elif uglydict['properties']['nominal']['layout'] == 'Flip':
        uglydict['properties']['top'] = uglydict['properties']['bottom'] = {}
        uglydict['actual']['top'] = uglydict['actual']['bottom'] = {}

        split_temp = cardlist[0].split("\n// ")
        uglydict['properties']['top']['name'] = split_temp[0]  # name(=str)
        uglydict['properties']['bottom']['name'] = split_temp[1]
        uglydict['properties']['nominal']['name'] = "{} // {}".format(split_temp[0], split_temp[1])

        split_temp = re.split(r'(?=[\-\+])', cardlist[1])
        uglydict['properties']['nominal']['mana_cost'] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['mana_cost'] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+])', cardlist[2])
        uglydict['properties']['nominal']['cmc'] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['cmc'] = split_temp[1]

        uglydict['properties']['nominal']['color'] = tuple(cardlist[3]) if cardlist[3] != "C" else ()  # color(=tuple)

        split_temp = cardlist[5].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['top']['supertype'] = tuple(split_subtemp[0].split(' '))  # supertype(=tuple)
        if len(split_subtemp) > 1:
            uglydict['actual']['top']['supertype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['bottom']['supertype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['bottom']['supertype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[6].split("\n")
        split_subtemp = re.split(r'[\-\+]', split_temp[0])
        uglydict['properties']['top']['subtype'] = tuple(split_subtemp[0].split(' '))  # subtype(=tuple)
        if len(split_subtemp) > 1:
         uglydict['actual']['top']['subtype'] = tuple(split_subtemp[1].split(' '))
        split_subtemp = re.split(r'[\-\+]', split_temp[1])
        uglydict['properties']['bottom']['subtype'] = tuple(split_subtemp[0].split(' '))
        if len(split_subtemp) > 1:
            uglydict['actual']['bottom']['subtype'] = tuple(split_subtemp[1].split(' '))

        split_temp = cardlist[9].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['top']['power'] = split_subtemp[0]  # power(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['top']['power'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['bottom']['power'] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict['actual']['bottom']['power'] = split_subtemp[1]

        split_temp = cardlist[10].split("\n")
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[0])
        uglydict['properties']['top']['toughness'] = split_subtemp[0]  # toughness(=str)
        if len(split_subtemp) > 1:
            uglydict['actual']['top']['toughness'] = split_subtemp[1]
        split_subtemp = re.split(r'(?=[\-\+])', split_temp[1])
        uglydict['properties']['bottom']['toughness'] = split_subtemp[0]
        if len(split_subtemp) > 1:
            uglydict['actual']['bottom']['toughness'] = split_subtemp[1]

        split_temp = cardlist[12].split("\n// ")
        uglydict['properties']['top']['oracle'] = split_temp[0]  # oracle(=str)
        uglydict['properties']['bottom']['oracle'] = split_temp[1]

        uglydict['properties']['nominal']['crop_image'] = cardlist[18]  # crop_image(=str, url)

    else:
        uglydict['properties']['nominal']['name'] = cardlist[0]  # name(=str)

        split_temp = re.split(r'(?=[\-\+])', cardlist[1])
        uglydict['properties']['nominal']['mana_cost'] = symbolprettify(split_temp[0], "reverse")  # mana_cost(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['mana_cost'] = symbolprettify(split_temp[1], "reverse")

        split_temp = re.split(r'(?=[\-\+])', cardlist[2])
        uglydict['properties']['nominal']['cmc'] = int(split_temp[0])  # CMC(=int)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['cmc'] = split_temp[1]

        uglydict['properties']['nominal']['color'] = tuple(cardlist[3]) if cardlist[3] != "C" else ()  # color(=tuple)

        split_temp = re.split(r'[\-\+]', cardlist[5])
        uglydict['properties']['nominal']['supertype'] = tuple(split_temp[0].split(' '))  # supertype(=tuple)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['supertype'] = tuple(split_temp[1].split(' '))

        split_temp = re.split(r'[\-\+]', cardlist[6])
        uglydict['properties']['nominal']['subtype'] = tuple(split_temp[0].split(' '))  # subtype(=tuple)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['subtype'] = tuple(split_temp[1].split(' '))

        split_temp = re.split(r'(?=[\-\+])', cardlist[9])
        uglydict['properties']['nominal']['power'] = split_temp[0]  # power(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['power'] = split_temp[1]

        split_temp = re.split(r'(?=[\-\+])', cardlist[10])
        uglydict['properties']['nominal']['toughness'] = split_temp[0]  # toughness(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['toughness'] = split_temp[1]

        split_temp = re.split(r'(?=[\-\+])', cardlist[11])
        uglydict['properties']['nominal']['loyalty'] = split_temp[0]  # loyalty(=str)
        if len(split_temp) > 1:
            uglydict['actual']['nominal']['loyalty'] = split_temp[1]

        uglydict['properties']['nominal']['oracle'] = cardlist[12]
        uglydict['properties']['nominal']['crop_image'] = cardlist[18]

    return uglydict


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
