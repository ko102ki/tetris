import pygame

pygame.init()
pygame.joystick.init()
print(pygame.joystick.get_count())
joystick = pygame.joystick.Joystick(0)
joystick.init()

print('name:', joystick.get_name())
print('numaxes:', joystick.get_numaxes())

print('axes:', joystick.get_axis(0))
print('numbuttons:', joystick.get_numbuttons())
print('numhats:', joystick.get_numhats())
print('hat:', joystick.get_hat(0))

while True:
    for i in range(12):
        print('hat' + str(i).zfill(2) + ':', joystick.get_button(i))

