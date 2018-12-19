import re

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

def landsort(list):
    pass


def determineBlock(setCode):
    if


def colorsort(color_set):
    if color_set == set():
        return 'Colorless'

    if color_set == set("W"):
        return 'W'
    if color_set == set("U"):
        return 'U'
    if color_set == set("B"):
        return 'B'
    if color_set == set("R"):
        return 'R'
    if color_set == set("G"):
        return 'G'

    if color_set == set("WU"):
        return 'WU'
    if color_set == set("UB"):
        return 'UB'
    if color_set == set("BR"):
        return 'BR'
    if color_set == set("RG"):
        return 'RG'
    if color_set == set("GW"):
        return 'GW'
    if color_set == set("WB"):
        return 'WB'
    if color_set == set("BG"):
        return 'BG'
    if color_set == set("GU"):
        return 'GU'
    if color_set == set("UR"):
        return 'UR'
    if color_set == set("RW"):
        return 'RW'

    if color_set == set("WUB"):
        return 'WUB'
    if color_set == set("UBR"):
        return 'UBR'
    if color_set == set("BRG"):
        return 'BRG'
    if color_set == set("RGW"):
        return 'RGW'
    if color_set == set("GWU"):
        return 'GWU'

    if color_set == set("WBG"):
        return 'WBG'
    if color_set == set("URW"):
        return 'URW'
    if color_set == set("BGU"):
        return 'BGU'
    if color_set == set("RWB"):
        return 'RWB'
    if color_set == set("GUR"):
        return 'GUR'

    if color_set == set("WUBR"):
        return 'WUBR'
    if color_set == set("UBRG"):
        return 'UBRG'
    if color_set == set("BRGW"):
        return 'BRGW'
    if color_set == set("RGWU"):
        return 'RGWU'
    if color_set == set("GWUB"):
        return 'GWUB'

    if color_set == set("WUBRG"):
        return 'WUBRG'


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
        return "z" + string;


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
        oldstring = "dump"
        while(oldstring != string):  # lookahead assertion 지원X
            oldstring = string
            string = re.sub(r'([^{])([A-Z])([^}])', r'\1{\2}\3', string)

    return string


def prettify(cardlist, mode=None):

    if mode != "reverse":
        prettylist = [None]*len(cardlist)
        prettylist[0] = cardlist[0]  # name
        prettylist[1] = symbolprettify(cardlist[1])  # mana_cost
        prettylist[2] = cardlist[2]  # CMC
        prettylist[3] = colorsort(cardlist[3])  # color(=set)
        prettylist[4] = colorsort(cardlist[4])  # color_identity(=set)
        prettylist[5] = cardlist[5]  #type_line
        prettylist[6] = '\n'.join(cardlist[6])  # supertype(=list)
        prettylist[7] = '\n'.join(cardlist[7])  # subtype(=list)
        prettylist[8] = cardlist[8].upper()  # set
        prettylist[9] = cardlist[9].title()  # rarity
        prettylist[10] = cardlist[10]  # oracle
        prettylist[11] = cardlist[11]  # layout
        prettylist[12] = '\n'.join(cardlist[12])  # hate(=list)
        prettylist[13] = '\n'.join(cardlist[13])  # buff(=list)
        prettylist[14] = '\n'.join(cardlist[14])  # nerf(=list)
        prettylist[15] = '\n'.join(cardlist[15])  # tags(=list)
        prettylist[16] = cardlist[16]  # crop_image

    if mode == "reverse":
        prettylist = [None]*len(cardlist)
        prettylist[0] = cardlist[0]  # name
        prettylist[1] = symbolprettify(cardlist[1], "reverse")  # mana_cost
        prettylist[2] = cardlist[2]  # CMC
        prettylist[3] = set(cardlist[3]) if cardlist[3] != "Colorless" else set()  # color(=set)
        prettylist[4] = set(cardlist[4]) if cardlist[4] != "Colorless" else set()  # color_identity(=set)
        prettylist[5] = cardlist[5]  #type_line
        prettylist[6] = cardlist[6].split("\n")  # supertype(=list)
        prettylist[7] = cardlist[7].split("\n")  # subtype(=list)
        prettylist[8] = cardlist[8].lower()  # set
        prettylist[9] = cardlist[9].lower()  # rarity
        prettylist[10] = cardlist[10]  # oracle
        prettylist[11] = cardlist[11]  # layout
        prettylist[12] = cardlist[12].split("\n")  # hate(=list)
        prettylist[13] = cardlist[13].split("\n")  # buff(=list)
        prettylist[14] = cardlist[14].split("\n")  # nerf(=list)
        prettylist[15] = cardlist[15].split("\n")  # tags(=list)
        prettylist[16] = cardlist[16]  # crop_image

    return prettylist


if __name__ == '__main__':
    print(symbolprettify("{11}{B}{R}{G}{W/B}{R/W}{2/B}{G/P}"))
    print(symbolprettify("11BRGOS(2/B)(G/P)", "reverse"))


    alist = ['W', 'U', 'B']
    print("set: %s" % set(alist))
    string = '\n'.join(alist)
    print(string)
    print(string.split("\n"))

    emptylist = []
    string = '\n'.join(emptylist)
    print("printed: %s" % string)

    setlist = {'B', 'U', 'W'}
    print(type(setlist))