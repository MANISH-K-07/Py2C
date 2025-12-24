from py2c.parser import Py2CParser
from py2c.optimizer import ConstantFolder
from py2c.codegen import CCodeGenerator


def main():
    with open("examples/input.py") as f:
        source = f.read()

    parser = Py2CParser(source)
    ir = parser.parse()

    optimizer = ConstantFolder()
    optimized_ir = optimizer.optimize(ir)

    codegen = CCodeGenerator()
    c_code = codegen.generate(optimized_ir)

    print("=== Generated C Code ===")
    print(c_code)


if __name__ == "__main__":
    main()
