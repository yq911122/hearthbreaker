from hsgame.constants import CHARACTER_CLASS

__author__ = 'Daniel'
import curses

card_abbreviations = {
    'Mark of the Wild': 'Mrk Wild',
    'Power of the Wild': 'Pow Wild',
    'Wild Growth': 'Wld Grth',
    'Healing Touch': 'Hlng Tch',
    'Mark of Nature': 'Mrk Ntr',
    'Savage Roar': 'Svg Roar',
    'Soul of the Forest': 'Sol Frst',
    'Force of Nature': 'Frce Nat',
    'Keeper of the Grove': 'Kpr Grve',
    'Druid of the Claw': 'Drd Claw',
    'Stonetusk Boar': 'Stntsk Br',
    'Raging Worgen': 'Rgng Wrgn',
}
# Color pairs:
# - 1: Nothing
# - 2: Active


def abbreviate(card_name):
    return card_abbreviations.get(card_name, card_name)


def draw_minion(minion, window, y, x):
    status_array = []
    if minion.can_attack():
        status_array.append("*")
        color = curses.color_pair(2)
    else:
        color = curses.color_pair(1)
    if "attack" in minion.events:
        status_array.append("a")
    if "turn_start" in minion.events:
        status_array.append("b")
    if minion.charge:
        status_array.append("c")
    if minion.deathrattle is not None:
        status_array.append("d")
    if minion.enraged:
        status_array.append("e")
    if minion.frozen:
        status_array.append("f")
    if minion.immune:
        status_array.append("i")
    if minion.stealth:
        status_array.append("s")
    if minion.taunt:
        status_array.append("t")
    if minion.exhausted:
        status_array.append("z")

    name = abbreviate(minion.card.name)[:9]
    status = ''.join(status_array)
    power_line = "({0}) ({1})".format(minion.calculate_attack(), minion.health)
    window.addstr(y + 0, x, "{0:^9}".format(name), color)
    window.addstr(y + 1, x, "{0:^9}".format(power_line), color)
    window.addstr(y + 2, x, "{0:^9}".format(status), color)


def draw_card(card, player, window, y, x):
    if card.can_use(player, player.game):
        status = "*"
        color = curses.color_pair(2)
    else:
        status = " "
        color = curses.color_pair(1)
    name = card.name[:15]
    window.addstr(y + 0, x, " {0:>2} mana ({1})   ".format(card.mana_cost(player), status), color)
    window.addstr(y + 1, x, "{0:^15}".format(name), color)


def draw_hero(hero, window, x, y):
    if hero.weapon is not None:
        weapon_power = "({0}) ({1})".format(hero.weapon.base_attack, hero.weapon.durability)
        window.addstr(y, x, "{0:^20}".format(hero.weapon.card.name))
        window.addstr(y + 1, x, "{0:^20}".format(weapon_power))

    hero_power = "({0}) ({1})".format(hero.calculate_attack(), hero.health)
    window.addstr(y, x + 20, "{0:^20}".format(CHARACTER_CLASS.to_str(hero.character_class)))
    window.addstr(y + 1, x + 20, "{0:^20}".format(hero_power))

    window.addstr(y, x + 40, "{0:^20}".format("Hero Power"))
    if hero.power.can_use():
        window.addstr(y + 1, x + 40, "{0:^20}".format("*"))


def game_to_string(game):
    pass


def draw_game(window, game, viewing_player):
    if viewing_player is game.players[0]:
        top_player = game.players[1]
        bottom_player = game.players[0]
    else:
        top_player = game.players[0]
        bottom_player = game.players[1]

    def draw_minions(minions, window):
        l_offset = int((80 - 10 * len(minions)) / 2)
        index = 0
        for minion in minions:
            draw_minion(minion, window, 0, l_offset + index * 10)
            index += 1

    def draw_cards(cards, player, window, y):
        l_offset = int((80 - 16 * len(cards)) / 2)
        index = 0
        for card in cards:
            draw_card(card, player, window, y, l_offset + index * 16)
            index += 1

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)

    top_minion_window = window.derwin(3, 80, 4, 0)
    draw_minions(top_player.minions, top_minion_window)
    bottom_minion_window = window.derwin(3, 80, 8, 0)
    draw_minions(bottom_player.minions, bottom_minion_window)

    card_window = window.derwin(5, 80, 16, 0)
    draw_cards(viewing_player.hand[:5], viewing_player, card_window, 0)
    draw_cards(viewing_player.hand[5:], viewing_player, card_window, 3)

    draw_hero(top_player.hero, window, 10, 0)
    draw_hero(bottom_player.hero, window, 10, 12)
