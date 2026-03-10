#  =============================================
#  ==========     EMKO-ETAPSound     ===========
#  =============================================
#  Emko-EtapSound, Emkotech tahtalar için geliştirilmiş Pardus 23 Etap ses sürücülerini güncelleyen bir yazılımdır.

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import subprocess
import os

def on_activate(app):
    builder = Gtk.Builder()
    
    builder.add_from_file("emko-etapsound.ui")

    window = builder.get_object("pencere")
    window.set_application(app)
    
    box = builder.get_object("kutucuk")
    header = builder.get_object("baslik")
    desc = builder.get_object("aciklama")
    button = builder.get_object("buton")

    button.connect("clicked", lambda x: click(button,desc))

    box.append(header)
    box.append(desc)
    box.append(button)

    window.present()

def click(button,desc):
    button.set_sensitive(False)
    desc.set_text("Tüm işlemler terminal üzerinden işlenecektir. Lütfen kapatmayınız.")
    PATH = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(["gnome-terminal","--","python3",f"{PATH}/etapsound.py"])
    exit(0)

app = Gtk.Application(application_id="com.emxrwashere.emko-etapsound")
app.connect("activate", on_activate)
app.run(None)