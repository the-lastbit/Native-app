import dearpygui.dearpygui as dpg
import asyncio
from API import access
import webbrowser
from server import app
from config.conf import tags
from os import getcwd, path, environ
import pathlib
from time import sleep
from app.heatmap import deploy_main_content


environ["FLASK_ENV"] = "server"
environ["FLASK_RUN_PORT"] = "8000"


def hyperlink(address):
    webbrowser.open_new(address)


class DeployWeb:
    def __init__(self):
        self.up = True

    def terminate(self):
        self.up = False

    def run(self, up_time: int):
        app.deploy()
        while self.up and up_time > 0:
            up_time -= 1
            time.sleep(1)


def try_login():
    response = asyncio.run(access())
    if response:
        dpg.delete_item(item=tags["main"]["welcomescreen"])
        dpg.show_item(item=tags["main"]["loadingscreen"])
        deploy_main_content()
    else:
        print()
        print("Primer intento de login fallido")
        print()
        server()


def server():
    from threading import Thread

    print()
    print("Local server UP!")
    print()
    deploy_web = DeployWeb()
    thread = Thread(target=deploy_web.run, args=(30,))
    thread.start()
    dpg.set_value(
        item=tags["main"]["welcometext"],
        value="Es necesario renovar la sesión en el siguiente \nenlace: ",
    )
    dpg.delete_item(item=tags["main"]["welcomebutton"])
    dpg.configure_item(item=tags["main"]["webpage"], show=True)
    hyperlink(
        address="localhost:8000/",
    )
    while True:
        response = asyncio.run(access())
        print(f"Reintentando")
        sleep(1)
        if response:
            print("Logueado!")
            dpg.delete_item(item=tags["main"]["welcomescreen"])
            dpg.show_item(item=tags["main"]["loadingscreen"])
            deploy_web.terminate()
            thread._delete()
            print("Bienvenido")
            deploy_main_content()
            return False
