#!/usr/bin/env python3

import sys
from xfreerdpui import RDP

def main():
    app = RDP()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
