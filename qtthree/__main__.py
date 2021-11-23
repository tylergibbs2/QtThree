import argparse
import sys

from qtthree.app import create_application

parser = argparse.ArgumentParser(description="QtThree")
parser.add_argument("--data-file", type=str, default="data.json", help="Persistent data storage")


if __name__ == '__main__':
    args = parser.parse_args()
    app = create_application(args.data_file)
    sys.exit(app.exec_())
