from py2c.parser import Py2CParser
from py2c.codegen import CCodeGenerator
from py2c.optimizer import ConstantFolder
from py2c.dce import DeadCodeEliminator
import sys


def main():
    try:
        # ---------- Read source ----------
        with open("examples/input.py", "r") as f:
            source = f.read()

        # ---------- Parse ----------
        parser = Py2CParser(source)
        ir = parser.parse()

        # ---------- Optimize ----------
        ir = ConstantFolder().optimize(ir)
        ir = DeadCodeEliminator().eliminate(ir)

        # ---------- Codegen ----------
        codegen = CCodeGenerator()
        c_code = codegen.generate(ir)

        # ---------- Output ----------
        print("==== Generated C Code ====\n")
        print(c_code)
        print("")

    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        sys.exit(1)

    except NotImplementedError as e:
        print(f"NotImplementedError: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Internal Compiler Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
