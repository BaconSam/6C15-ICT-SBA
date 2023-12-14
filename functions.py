def inputHouse(corr):
    while corr == False:
        Ihouse = str(input("input the house of the student. (R/G/B/Y) or input \"end\" to stop inputting  ")).lower()
        
        match Ihouse:
            case "r":
                Ihouse = "Red"
                corr = True
            case "g":
                Ihouse = "Green"
                corr = True
            case "b":
                Ihouse = "Blue"
                corr = True
            case "y":
                Ihouse = "Yellow"
                corr = True
            case "quit"|"end":
                Ihouse = "end"
                corr = True
                return Ihouse
            case _:
                print("Please input accordingly\nRed House: R\nGreen House: G\nBlue House: B\nYellow House: Y")
                corr = False

    print("The student is " + Ihouse)
    return Ihouse

def inputSeed():
    IsBool = False
    seed = "nil"
    while IsBool == False:
        seed = input("Is he/she a seed player? T/F  ").lower()

        match seed:
            case "t":
                seed = True
                IsBool = True
            case "f":
                seed = False
                IsBool = True
            case _:
                print("Enter a boolean value\nTrue: T / t\nFalse: F / f") 
    
    print("Seed: " + str(seed))
    return seed