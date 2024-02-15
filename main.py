#!/usr/bin/python3
import curses
import os

emotes = [
    ('shrug', '¯\\_(ツ)_/¯'),
]

def get_previous_pos(stdscr: curses.window):
    cursor = stdscr.getyx()
    return cursor[0], max(cursor[1] - 1, 0)

def get_next_pos(stdscr: curses.window, length):
    cursor = stdscr.getyx()
    return cursor[0], min(cursor[1] + 1, length)

def main(stdscr: curses.window):
    curses.set_escdelay(1)
    stdscr.clear()
    stdscr.addstr(1, 0, '──' * curses.LINES)
    stdscr.move(0, 0)
    search = []
    emotes_space = stdscr.subpad(2, 0)
    selected = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_emote_color = curses.color_pair(1)
    while True:
        emotes_space.clear()
        str_search = ''.join(search)
        found_emotes = []
        for name, emote in emotes:
            if str_search in name:
                found_emotes.append((name, emote))
        selected = max(0, min(len(found_emotes) - 1, selected))
        for i, (name, emote) in enumerate(found_emotes):
            if i == selected:
                emotes_space.addstr(f'{name} ({emote})\n', selected_emote_color)
            else:
                emotes_space.addstr(f'{name} ({emote})\n')
        emotes_space.refresh()
        key = stdscr.getkey()
        if key == 'KEY_BACKSPACE':
            pos = get_previous_pos(stdscr)
            stdscr.delch(*pos)
            if len(search) > 0:
                del search[pos[1]]
        elif key == 'KEY_DC':
            pos = stdscr.getyx()
            stdscr.delch(*pos)
            if len(search) > pos[1]:
                del search[pos[1]]
        elif key == 'KEY_LEFT':
            stdscr.move(*get_previous_pos(stdscr))
        elif key == 'KEY_RIGHT':
            stdscr.move(*get_next_pos(stdscr, len(search)))
        elif key == 'KEY_UP':
            selected = max(selected - 1, 0)
        elif key == 'KEY_DOWN':
            selected = min(selected + 1, len(found_emotes) - 1)
        elif key == '\n':
            os.system(f'echo "{found_emotes[selected][1]}" | xclip -selection clipboard -r')
            return
        elif key == '':
            return
        else:
            pos = stdscr.getyx()
            stdscr.addstr(key)
            if pos[1] > len(search) - 1:
                search.append(key)
            else:
                search[pos[1]] = key


curses.wrapper(main)
