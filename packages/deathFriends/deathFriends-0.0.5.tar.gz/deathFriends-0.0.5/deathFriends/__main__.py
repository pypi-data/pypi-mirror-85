from .game import Game

def loop():
    g = Game()
    option = g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()


if __name__ == '__main__':
    loop()