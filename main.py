from firmware import Firmware
from GUI.app import App

def main():

    App(Firmware())

    # f = Firmware()
    # names = f.get_controllers_names()
    # print(names)
    # # log = f.get_controllers_log(names[0])
    # # print(log)
    # data = f.get_controller_data(names[0])
    # print(data)
    # errors = f.get_controller_errors(names[0])
    # print(errors)


if __name__ == '__main__':
    main()
