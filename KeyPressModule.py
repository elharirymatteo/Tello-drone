import pygame


def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


def get_key(key_name):
    ans = False
    for eve in pygame.event.get():
        pass
    key_input = pygame.key.get_pressed()
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    if key_input[my_key]:
        ans = True
    pygame.display.update()

    return ans


def main():
    if get_key("LEFT"):
        print("Left key pressed")
    if get_key("RIGHT"):
        print("Right key pressed")


if __name__ == '__main__':
    init()
