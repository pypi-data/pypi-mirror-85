#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os

import yaml

DIR_FILE = os.path.dirname(__file__)
DATA_FILE = os.path.join(DIR_FILE, "data/demo.yaml")


def load_data():
    with open(DATA_FILE, "r") as fr:
        data = yaml.load(fr, Loader=yaml.FullLoader)
    print(data)


def main():
    print("This is the caller")


if __name__ == "__main__":
    main()
    load_data()
