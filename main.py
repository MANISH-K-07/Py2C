from py2c.parser import Py2CParser


def main():
    with open("examples/input.py") as f:
        source = f.read()

    parser = Py2CParser(source)
    ir = parser.parse()

    print(ir)


if __name__ == "__main__":
    main()
