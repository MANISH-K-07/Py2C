from py2c.parser import Py2CParser
from py2c.optimizer import ConstantFolder
from py2c.dce import DeadCodeEliminator
from py2c.codegen import CCodeGenerator


def main():
    with open("examples/input.py") as f:
        source = f.read()

    parser = Py2CParser(source)
    ir = parser.parse()

    ir = ConstantFolder().optimize(ir)
    #ir = DeadCodeEliminator().eliminate(ir)

    codegen = CCodeGenerator()
    c_code = codegen.generate(ir)

    print("=== Generated C Code ===")
    print(c_code)


if __name__ == "__main__":
    main()
