# imports
import platform
import random
import itertools
from os import system
import sys


# Fonctions
def clearwindows():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


def charsetchoice():
    global listchartype, uchoice, charset
    listchartype = []
    # Import des charsets
    with open(file='charset.lst') as charset:
        for chartype in charset:
            if '=' in chartype:
                # print(chartype)
                listchartype.append(chartype.strip().split('=', 1))

    # Ajout du numéro de la ligne
    i = 0
    while i < len(listchartype):
        listchartype[i].insert(0, i + 1)
        listchartype[i][2] = listchartype[i][2].lstrip().lstrip('[').rstrip(']')
        i += 1

    # Print les choix de caractères possibles
    for choice in listchartype:
        print("%s\t%s\t\t%s" % (choice[0], choice[1], choice[2]))

    # Choix du charset
    uchoice = input("Which charset do you wanna use [1-%s]: " % (len(listchartype)))
    while int(uchoice) < 1 or int(uchoice) > len(listchartype):
        uchoice = input("Which charset do you wanna use [1-%s]: " % (len(listchartype)))
    charset = str(listchartype[int(uchoice) - 1][2])
    print(charset)
    global numeric, lalpha, ualpha, special
    numeric = ""
    lalpha = ""
    ualpha = ""
    special = ""
    for char in list(charset):
        if char.isdigit():
            numeric = numeric + char
        elif char.islower():
            lalpha = lalpha + char
        elif char.isupper():
            ualpha = ualpha + char
        else:
            special = special + char


def wordchoice():
    global rword
    words = []
    # Import des password à trouver
    with open(file='passwords.txt') as wordlist:
        for word in wordlist:
            words.append(word.rstrip('\n'))

    # Choix random d'un password à chercher
    rword = random.choices(words)
    print(rword)


def crunchcommandline():
    # Generate the crunch commandline of your choices
    print("This is your crunch equivalent: crunch %s %s -f /PATH/TO/charset.lst %s" % (lenmin, lenmax, listchartype[int(uchoice) - 1][1]))
    input("Press any to continue...")


def generatepassword():
    global lenmin, lenmax, string
    types = []
    havepattern = input("Do you the pattern of the password [Y/n]: ")
    if havepattern in ["", "Y", "y"]:
        print("@\tlowercase\n,\tuppercase\n*\tnumber\n^\tspecial")
        pattern = input("Enter your pattern: ")
        while pattern == "":
            pattern = input("Enter your pattern: ")
        lenmin = len(pattern)
        lenmax = len(pattern)
        print("{} < {}".format(lenmin, lenmax))
        for x in pattern:
            if x == "@":
                types.append(lalpha)
            elif x == ",":
                types.append(ualpha)
            elif x == "*":
                types.append(numeric)
            elif x == "^":
                types.append(special)
        print(len(list(itertools.product(*types))))
        for xs in list(itertools.product(*types)):
            string = "".join(xs)
            if string == rword:
                clearwindows()
                print("******************************\n**{:^26}**\n******************************".format(string))
                sys.exit("You found the password.")
            else:
                print(string)
    else:
        lenmin = int(input("Minimum lenght of your password to guess: "))
        lenmax = int(input("Maximal lenght of your password to guess: "))
        for x in range(lenmin, lenmax + 1):
            for xs in list(itertools.product(charset,repeat=x)):
                string = "".join(xs)
                if string == rword:
                    clearwindows()
                    print("******************************\n**{:^26}**\n******************************".format(string))
                    sys.exit("You found the password.")
                else:
                    print(string)


wordchoice()
charsetchoice()
generatepassword()
