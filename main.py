from py2c.parser import Py2CParser
from py2c.codegen import CCodeGenerator
import sys


def main():
    try:
        with open("examples/input.py", "r") as f:
            source = f.read()

        parser = Py2CParser(source)
        ir = parser.parse()

        codegen = CCodeGenerator()
        c_code = codegen.generate(ir)

        print("=== Generated C Code ===")
        print("")
        print(c_code)
        print("")

    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        sys.exit(1)

    except NotImplementedError as e:
        print(f"NotImplementedError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
