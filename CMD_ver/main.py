from items import Item
from functions import *
import csv, json
import PySimpleGUI as sg

sg.theme('Dark2')

# test commit

def main():
    list_item = []
    Ihouse = "-1"
    seed = "nil"

    for i in range(16):
        # House
        corr_info = False
        Ihouse = inputHouse(corr_info)

        if Ihouse == "end":
            return

        # Seed
        seed = inputSeed()

        # Store in item
        print(str(i))
        list_item.append(Item(Ihouse, seed, False))
        print(f"Done {list_item[i].House} {list_item[i].Seed}")


if __name__ == "__main__":
    main()
