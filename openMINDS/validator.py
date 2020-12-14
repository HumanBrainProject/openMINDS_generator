import sys
import jsonschema


def main():
    print("Validator")

def verify_parameters(argv):
    if len(argv) != 2:
        print("Wrong number of arguments")
        help()
        sys.exit(1)

if __name__ == "__main__":
    main()
