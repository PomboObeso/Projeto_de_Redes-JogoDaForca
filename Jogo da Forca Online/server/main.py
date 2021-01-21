from interface.interface import Interface


def main():
    interface = Interface("localhost", 20)
    interface.start_server()


if __name__ == '__main__':
    main()
