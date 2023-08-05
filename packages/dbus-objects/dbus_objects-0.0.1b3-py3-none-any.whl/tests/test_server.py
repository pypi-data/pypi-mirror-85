# SPDX-License-Identifier: MIT
"""
import textwrap

import jeepney
import jeepney.integrate.blocking
import jeepney.wrappers


def test_introspectable(jeepney_one_time_server, jeepney_connection):
    client = jeepney.DBusAddress(
        '/io/github/ffy00/dbus_objects',
        bus_name='io.github.ffy00.dbus-objects.tests',
        interface='org.freedesktop.DBus.Introspectable',
    )

    msg = jeepney.new_method_call(client, 'Introspect', '', tuple())
    reply = jeepney_connection.send_and_get_reply(msg)
    assert reply[0] == textwrap.dedent('''
    <!DOCTYPE node PUBLIC
    "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
    "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd" >
    <node xmlns:doc="http://www.freedesktop.org/dbus/1.0/doc.dtd"><interface name="org.freedesktop.DBus.Peer"><method name="Ping" /></interface><interface name="org.freedesktop.DBus.Introspectable"><method name="Introspect"><arg direction="out" type="s" name="xml" /></method></interface><node name="example" /></node>
    ''').strip()


def test_ping(jeepney_one_time_server, jeepney_connection):
    client = jeepney.DBusAddress(
        '/io/github/ffy00/dbus_objects',
        bus_name='io.github.ffy00.dbus-objects.tests',
        interface='org.freedesktop.DBus.Peer',
    )

    print('sending message')
    msg = jeepney.new_method_call(client, 'Ping', '', tuple())
    jeepney_connection.send_and_get_reply(msg)
"""
