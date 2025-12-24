from py2c.parser import Py2CParser
from py2c.optimizer import ConstantFolder


def main():
    with open("examples/input.py") as f:
        source = f.read()

    parser = Py2CParser(source)
    ir = parser.parse()

    print("=== Original IR ===")
    print(ir)

    optimizer = ConstantFolder()
    optimized_ir = optimizer.optimize(ir)

    print("\n=== Optimized IR ===")
    print(optimized_ir)


if __name__ == "__main__":
    main()
