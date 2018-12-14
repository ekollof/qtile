
import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from Xlib import X, display
from Xlib.ext import randr
from pprint import pprint


d = display.Display()
s = d.screen()
r = s.root
res = r.xrandr_get_screen_resources()._data

num_screens = 0
for output in res['outputs']:
    print("Output %d:" % (output))
    mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
    print("%s: %d" % (mon['name'], mon['num_preferred']))
    if mon['num_preferred']:
        num_screens += 1

print("%d screens found!" % (num_screens))

try:
    from typing import List  # noqa: F401
except ImportError:
    pass


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("sakura")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "p", lazy.spawn("rofi -show run")),
    Key([mod, "shift"], "p", lazy.spawn("rofi-pass")),
    Key(["mod1", "control"], "l", lazy.spawn("slock")),


]

groups = [Group(i) for i in "12345678"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.MonadTall(name='Tall'),
    layout.VerticalTile(name='VerticalTile'),
    layout.Max(name='Full'),
]

widget_defaults = dict(
    font='Fira Code',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = []
for screen in range(0, num_screens):
    screens.append(
        Screen(
            top=bar.Bar(
                [
                    widget.Sep(),
                    widget.GroupBox(),
                    widget.Sep(),
                    widget.Prompt(),
                    widget.Sep(),
                    widget.WindowName(),
                    widget.Systray(),
                    widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
                    widget.CurrentLayout(),
                ],
                24,
            ),
        )
    )

#screens = [
#   Screen(
#       top=bar.Bar(
#           [
#               widget.Sep(),
#               widget.GroupBox(),
#               widget.Sep(),
#               widget.Prompt(),
#               widget.Sep(),
#               widget.WindowName(),
#               widget.Systray(),
#               widget.Clock(format='%Y-%m-%d %a %H:%M:%S'),
#               widget.CurrentLayout(),
#           ],
#           24,
#       ),
#   ),
#

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
