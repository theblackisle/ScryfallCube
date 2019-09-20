import re

enchantment_subtypes = tuple("Aura, Cartouche, Curse, Saga, Shrine".split(', '))
artifact_subtypes = tuple("Clue, Contraption, Equipment, Fortification, Treasure, Vehicle".split(', '))
land_subtypes = tuple("Desert, Forest, Gate, Island, Lair, Locus, Mine, Mountain, Plains, Power-Plant, Swamp, Tower, Urza’s".split(', '))
basic_land_subtypes = tuple("Plains, Island, Swamp, Mountain, Forest".split(', '))
planeswalker_subtypes = tuple("Ajani, Aminatou, Angrath, Arlinn, Ashiok, Bolas, Chandra, Dack, Daretti, Domri, Dovin, Elspeth, Estrid, Freyalise, Garruk, Gideon, Huatli, Jace, Jaya, Karn, Kaya, Kiora, Koth, Liliana, Nahiri, Narset, Nissa, Nixilis, Ral, Rowan, Saheeli, Samut, Sarkhan, Sorin, Tamiyo, Teferi, Tezzeret, Tibalt, Ugin, Venser, Vivien, Vraska, Will, Windgrace, Xenagos, Yanggu, Yanling".split(', '))
spell_subtypes = tuple("Adventure, Arcane, Trap".split(', '))
class_subtypes = tuple("Advisor, Ally, Archer, Artificer, Army, Assassin, Barbarian, Berserker, Cleric, Druid, Elder, Flagbearer, Knight, Mercenary, Minion, Monk, Mystic, Ninja, Noble, Nomad, Peasant, Pilot, Pirate, Praetor, Rebel, Rigger, Rogue, Samurai, Scout, Shaman, Soldier, Spellshaper, Warlock, Warrior, Wizard".split(', '))
race_subtypes = tuple("Ape, Azra, Centaur, Cyclops, Dauthi, Dryad, Dwarf, Elf, Faerie, Giant, Gnome, Goblin, Gorgon, Hag, Human, Kithkin, Kobold, Kor, Merfolk, Metathran, Minotaur, Moonfolk, Mouse, Naga, Noggle, Ogre, Orc, Ouphe, Satyr, Sculpture, Siren, Slith, Soltari, Surrakar, Thalakos, Troll, Vedalken, Viashino, Werewolf, Yeti, Ainok, Amphin, Aven, Khenra, Kitsune, Leonin, Loxodon, Nantuko/Kraul, Nezumi, Orochi, Rakshasas, Rhox, Wolfir, Aetherborn, Angel, Archon, Avatar, Bringer, Djinn, Efreet, God, Lamia, Nymph, Reflection, Shade, Shapeshifter, Skeleton, Sliver, Specter, Spirit, Thrull, Vampire, Wraith, Zombie, Beeble, Carrier, Cephalid, Demon, Devil, Dragon, Drone, Eldrazi, Elemental, Eye, Gremlin, Harpy, Homarid, Homunculus, Horror, Illusion, Imp, Incarnation, Kirin, Nephilim, Nightmare, Nightstalker, Spawn, Sphinx, Spirit, Thallid, Treefolk, Zubera, Phyrexian, Chimera, Mutant, Orgg, Volver, Weird, Antelope, Ape, Aurochs, Badger, Bat, Bear, Bird, Boar, Camel, Caribou, Cats, Crab, Crocodile, Dinosaur, Elephant, Elk, Ferret, Fish, Fox, Frog, Goat, Hippo, Horse, Hound, Hyena, Insect, Jackal, Jellyfish, Leech, Lizard, Mole, Mongoose, Monkey, Nautilus, Octopus, Ox, Oyster, Pangolin, Rabbit, Rat, Rhino, Sable, Salamander, Scorpion, Sheep, Slug, Snake, Spider, Sponge, Squid, Squirrel, Starfish, Trilobite, Turtle, Whale, Wolf, Wolverine, Wombat, Worm, Atog, Basilisk, Beast, Brushwagg, Camarid, Cockatrice, Drake, Gargoyle, Griffin, Hellion, Hippogriff, Hydra, Kavu, Kraken, Lammasu, Leviathan, Lhurgoyf, Licid, Manticore, Mutant, Pegasus, Phelddagrif, Phoenix, Serpent, Slith, Sliver, Spike, Unicorn, Wurm, Plant, Saproling, Treefolk, Fungus, Germ, Ooze, Assembly-Worker, Blinkmoth, Chimera, Construct, Dreadnought, Gnome, Golem, Juggernaut, Masticore, Myr, Pentavite, Pest, Prism, Servo, Scarecrow, Tetravite, Thopter, Triskelavite, Orb, Sand, Wall".split(', '))
creature_subtypes = class_subtypes + race_subtypes


def toler_int(string):
    if string.isdigit():
        return int(string)
    else:
        return string


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
    value = value.upper()
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
    isC = False
    if 'C' in color_set:
        isC = True
        color_set = color_set - {'C'}
    ordered_set = ('Error')

    if color_set == set(): ordered_set = []

    if color_set == {W}: ordered_set = [W]
    if color_set == {U}: ordered_set = [U]
    if color_set == {B}: ordered_set = [B]
    if color_set == {R}: ordered_set = [R]
    if color_set == {G}: ordered_set = [G]

    if color_set == {W,U}: ordered_set = [W,U]
    if color_set == {U,B}: ordered_set = [U,B]
    if color_set == {B,R}: ordered_set = [B,R]
    if color_set == {R,G}: ordered_set = [R,G]
    if color_set == {G,W}: ordered_set = [G,W]

    if color_set == {W,B}: ordered_set = [W,B]
    if color_set == {B,G}: ordered_set = [B,G]
    if color_set == {G,U}: ordered_set = [G,U]
    if color_set == {U,R}: ordered_set = [U,R]
    if color_set == {R,W}: ordered_set = [R,W]

    if color_set == {W,U,B}: ordered_set = [W,U,B]
    if color_set == {U,B,R}: ordered_set = [U,B,R]
    if color_set == {B,R,G}: ordered_set = [B,R,G]
    if color_set == {R,G,W}: ordered_set = [R,G,W]
    if color_set == {G,W,U}: ordered_set = [G,W,U]

    if color_set == {W,B,G}: ordered_set = [W,B,G]
    if color_set == {U,R,W}: ordered_set = [U,R,W]
    if color_set == {B,G,U}: ordered_set = [B,G,U]
    if color_set == {R,W,B}: ordered_set = [R,W,B]
    if color_set == {G,U,R}: ordered_set = [G,U,R]

    if color_set == {W,U,B,R}: ordered_set = [W,U,B,R]
    if color_set == {U,B,R,G}: ordered_set = [U,B,R,G]
    if color_set == {B,R,G,W}: ordered_set = [B,R,G,W]
    if color_set == {R,G,W,U}: ordered_set = [R,G,W,U]
    if color_set == {G,W,U,B}: ordered_set = [G,W,U,B]

    if color_set == {W,U,B,R,G}: ordered_set = [W,U,B,R,G]

    if isC:
        ordered_set.append('C')

    return tuple(ordered_set)


def nick_to_color(nick):
    if nick.title() == "Colorless": return ()

    if nick.title() == "White": return 'W',
    if nick.title() == "Blue": return 'U',
    if nick.title() == "Black": return 'B',
    if nick.title() == "Red": return 'R',
    if nick.title() == "Green": return 'G',

    if nick.title() == "Azorius": return 'W', 'U'
    if nick.title() == "Dimir": return 'U', 'B'
    if nick.title() == 'Rakdos': return 'B', 'R'
    if nick.title() == "Gruul": return 'R', 'G'
    if nick.title() == "Selesnya": return 'G', 'W'
    if nick.title() == "Orzhov": return 'W', 'B'
    if nick.title() == "Golgari": return 'B', 'G'
    if nick.title() == "Simic": return 'G', 'U'
    if nick.title() == "Izzet": return 'U', 'R'
    if nick.title() == "Boros": return 'R', 'W'

    if nick.title() == "Esper": return 'W', 'U', 'B'
    if nick.title() == "Grixis": return 'U', 'B', 'R'
    if nick.title() == "Jund": return 'B', 'R', 'G'
    if nick.title() == "Naya": return 'R', 'G', 'W'
    if nick.title() == "Bant": return 'G', 'W', 'U'
    if nick.title() == "Abzan": return 'W', 'B', 'G'
    if nick.title() == "Jeskai": return 'U', 'R', 'W'
    if nick.title() == "Sultai": return 'B', 'G', 'U'
    if nick.title() == "Mardu": return 'R', 'W', 'B'
    if nick.title() == "Temur": return 'G', 'U', 'R'

    if nick.title() == "Greenless": return 'W', 'U', 'B', 'R'
    if nick.title() == "Whiteless": return 'U', 'B', 'R', 'G'
    if nick.title() == "Blueless": return 'B', 'R', 'G', 'W'
    if nick.title() == "Blackless": return 'R', 'G', 'W', 'U'
    if nick.title() == "Redless": return 'G', 'W', 'U', 'B'

    if nick.title() == "5C": return 'W', 'U', 'B', 'R', 'G'


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


if __name__ == '__main__':
    '''
    print(symbolprettify("{11}{B}{R}{G}{W/B}{R/W}{2/B}{G/P} // {R}{R}{R}{R}"))
    print(symbolprettify("11BRGOS(2/B)(G/P) // RRRR", "reverse"))

    alist = ["Swamp', 'Knight', 'Island"]
    print(alist)
    alist = subtypeSort(alist)
    print(alist)
    '''
    mana1 = "{11}{B}{R}{G}{W/B}{R/W}{2/B}{G/P}"
    mana2 = "{W/U}{U/B}{U/R}"