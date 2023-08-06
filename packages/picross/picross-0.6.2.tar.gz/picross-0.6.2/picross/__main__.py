def run():
    from . import conf
    from .gui.controller import Controller

    conf.init()

    # Actually start the program
    c = Controller()
    c.run()


if __name__ == "__main__":
    run()
