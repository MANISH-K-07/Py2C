from py2c.parser import Py2CParser

def main():
    with open("examples/input.py") as f:
        source = f.read()

    parser = Py2CParser(source)
    print(parser.dump_ast())

if __name__ == "__main__":
    main()
