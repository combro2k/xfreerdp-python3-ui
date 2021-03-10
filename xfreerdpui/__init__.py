#!/usr/bin/env python3

import os
import socket
import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import (
    Gio,
    Gtk,
    Gdk
)

try:
    from libqtile.command_interface import CommandInterface, IPCCommandInterface
    from libqtile.command_client import CommandClient
    from libqtile.ipc import Client, find_sockfile
    qtile_support = True
except:
    qtile_support = False

from subprocess import (
    Popen,
    STDOUT,
    PIPE,
    run,
)
from os.path import expanduser

class RDPWindow(Gtk.ApplicationWindow):
    _history_file = expanduser('~/.config/xfreerdpui/history')
    qtile = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'application' in kwargs:
            self.application = kwargs['application']
            self.qtile = self.application.qtile

        self.set_role('qtile-rdp')
        self.set_type_hint(Gdk.WindowTypeHint.TOOLBAR)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_accept_focus(True)
        self.stick()
        self.resize(600, 150)

        self.set_border_width(20)
        self.set_mnemonics_visible(True)

        self.connect('key-press-event', self._key_press_event)

    def _key_press_event(self, widget, event):
        if isinstance(widget, RDPWindow) and Gdk.keyval_name(event.keyval) == 'Escape':
            self.destroy()

        if isinstance(widget, Gtk.Entry) and Gdk.keyval_name(event.keyval) == 'Return':
            self.cmd_connect(widget)

        return False

    def present(self):
        from pprint import pprint

        if qtile_support is True:
            qscreen = self.qtile.navigate('screen', None)
            screen_info = qscreen.call('info')()
        else:
            r = run(['sh', '-c', '/usr/bin/xrandr | awk \'/\*/ {print $1}\''], stdout=PIPE, universal_newlines=True)
            s = r.stdout.lstrip().split('x', 2)
            screen_info = {
                'width': int(s[0]),
                'height': int(s[1]),
            }

        self.width = screen_info['width']
        # need to get bar yet, but its an start
        self.height = screen_info['height'] - 27

        host_entries = Gtk.ListStore(str)
        for i in self.history:
            if i not in host_entries:
                host_entries.append([i])

        completion = Gtk.EntryCompletion(
            model=host_entries,
            inline_completion=True,
        )
        completion.set_text_column(0)

        self.message = Gtk.Label(
            label="",
            visible=True,
        )

        self.host = Gtk.ComboBox(
            visible=True,
            has_entry=True,
            model=host_entries,
            entry_text_column=0,
        )

        self.host.get_child().set_completion(completion)
        self.host.get_child().set_placeholder_text('Hostname')

        self.username = Gtk.Entry(
            visible=True,
            placeholder_text='Administrator',
        )
        self.password = Gtk.Entry(
            visible=True,
            placeholder_text='Password',
            visibility=False,
        )
        self.btn_connect = Gtk.Button(
            visible=True,
            label='_Connect',
            use_underline=True,
        )
        self.fullscreen = Gtk.CheckButton(
            visible=True,
            label='_Fullscreen',
            use_underline=True,
        )
        self.password_reveal = Gtk.CheckButton(
            visible=True,
            label='_Reveal',
            use_underline=True,
        )

        self.btn_connect.connect("clicked", self.cmd_connect)
        self.host.connect('key-press-event', self._key_press_event)
        self.username.connect('key-press-event', self._key_press_event)
        self.password.connect('key-press-event', self._key_press_event)
        self.password_reveal.connect("clicked", self.cmd_password_reveal)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        hbox0 = Gtk.Box(spacing=10, visible=True)
        hbox1 = Gtk.Box(spacing=10, visible=True)
        hbox2 = Gtk.Box(spacing=10, visible=True)
        hbox3 = Gtk.Box(spacing=10, visible=True)
        hbox4 = Gtk.Box(spacing=10, visible=True)

        hbox0.pack_start(Gtk.Label(
            visible=True,
            label='_Hostname:',
            mnemonic_widget=self.host,
            use_underline=True,
            xalign=0,
        ), True, True, 0)
        hbox1.pack_start(self.host, True, True, 0)
        hbox2.pack_start(Gtk.Label(
            visible=True,
            label='_Username:',
            mnemonic_widget=self.username,
            use_underline=True,
            xalign=0,
        ), True, True, 0)
        hbox2.pack_start(Gtk.Label(
            label='_Password:',
            mnemonic_widget=self.password,
            use_underline=True,
            visible=True,
            xalign=0,
        ), True, True, 0)

        hbox3.pack_start(self.username, True, True, 0)
        hbox3.pack_start(self.password, True, True, 0)
        hbox3.pack_start(self.password_reveal, True, True, 0)
        hbox4.pack_start(self.fullscreen, True, True, 0)

        vbox.pack_start(self.message, True, True, 0)
        vbox.pack_start(hbox0, True, True, 0)
        vbox.pack_start(hbox1, True, True, 0)
        vbox.pack_start(hbox2, True, True, 0)
        vbox.pack_start(hbox3, True, True, 0)
        vbox.pack_start(hbox4, True, True, 0)
        vbox.pack_start(self.btn_connect, True, True, 0)
        vbox.show()

        self.add(vbox)

        super().present()

    def cmd_connect(self, button):
        try:
            host = self.host.get_child().get_text()

            socket.gethostbyname(host)

            self.add_history(host)

            username = self.username.get_text() or 'Administrator'
            password = self.password.get_text()

            if not (host and username and password):
                return False

            params = [
                '-decorations',
                '-offscreen-cache',
                '-glyph-cache',
                '+heartbeat',
                '+clipboard',
                '+async-update',
                '+gfx-small-cache',
                '+multitransport',
                # '+gfx-progressive',E4
                '/compression-level:2',
                '/gdi:sw',
                '/cert-ignore',
                '/drive:home,%s' % (expanduser('~')),
                '/v:%s' % (host),
                '/u:%s' % (username),
                '/p:%s' % (password),
            ]

            if self.fullscreen.get_active():
                cmd = f'/usr/bin/xfreerdp /f %s' % (' '.join(params))
            else:
                cmd = f'/usr/bin/xfreerdp %s /w:%s /h:%s' % (
                    ' '.join(params),
                    self.width,
                    self.height,
                )


            self.hide()

            try:
                FNULL = open(os.devnull, 'w')
                p = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE)
                outs, errs = p.communicate(timeout=None)
               
                print(outs.decode("utf-8"))
                print(errs.decode("utf-8"))

                if p.returncode == 131:
                    self.message.set_label('Username and/or password is wrong')
                    self.show()

                elif p.returncode == 133:
                    self.message.set_label('Host is not listening to RDP connection')
                    self.show()

                else:
                    self.destroy()

            except Exception as e:
                print(e)
                self.destroy()

        except Exception as e:
            print(e)
            self.destroy()

    def cmd_password_reveal(self, button):
        self.password.set_visibility(button.get_active())

    @property
    def history(self):
        history = []

        if not os.path.exists(self._history_file):
            return history

        with open(self._history_file, 'r') as f:
            for l in sorted(f.read().splitlines()):
                if l not in history:
                    history.append(l)

        return history

    def add_history(self, value):
        history = self.history

        if not value in history:
            basedir = os.path.dirname(self._history_file)

            history.append(value)
            history = sorted(history)

            if not os.path.exists(basedir):
                os.makedirs(basedir)

            with open(self._history_file, 'w') as f:
                for l in history:
                    f.write('%s\n' % (l))


class RDP(Gtk.Application):
    _qtile = None

    def __init__(self, qtile=None):
        Gtk.Application.__init__(self,
            application_id="org.qtile.rdp." + str(os.getpid()),
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        if qtile is not None:
            self._qtile = qtile

        self.window = None

    def do_activate(self):
        window = RDPWindow(application=self, title="Qtile RDP")
        window.present()

    @property
    def qtile(self):
        if self._qtile is None and qtile_support is True:
            self._qtile = CommandClient(command=IPCCommandInterface(Client(find_sockfile())))

        return self._qtile

if __name__ == "__main__":
    app = RDP()
    app.run(sys.argv)
