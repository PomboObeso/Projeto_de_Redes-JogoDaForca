from interface.main import Interface


def main():
    interface = Interface("localhost", 20)
    interface.start()


if __name__ == '__main__':
    main()
