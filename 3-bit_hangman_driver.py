# from https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Hangman incrementor
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Counter bit 1
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Counter bit 2
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Counter bit 3
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Counter bit 4
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Out 18 is PC (Program Counter)
GPIO.setup(18,GPIO.OUT)

# "Guess/store"
GPIO.setup(2, GPIO.OUT)

# 3-bit "keyboard" 1 of 3 - TOP input (output from Pi, INto breadboard)
GPIO.setup(25, GPIO.OUT)
# 3-bit "keyboard" 2 of 3 - MIDDLE input
GPIO.setup(8, GPIO.OUT)
# 3-bit "keyboard" 3 of 3 - BOTTOM input
GPIO.setup(7, GPIO.OUT)

# Test keyboard all on
GPIO.output(25, GPIO.HIGH)
GPIO.output(8, GPIO.HIGH)
GPIO.output(7, GPIO.HIGH)

# Test in guess/store mode
GPIO.output(2, GPIO.LOW)

# print "LED on"
# GPIO.output(18,GPIO.HIGH)
# time.sleep(.1)
# print "LED off"
GPIO.output(18,GPIO.LOW)
pcSwitch = False

counterState = 0

saveGuessState = False

keyBoardTop = True
keyBoardMiddle = True
keyBoardBottom = True

incorrectGuesses = 0

def encode(character):
    global keyBoardTop
    global keyBoardMiddle
    global keyBoardBottom

    numeric = ord(character) - 97

    print("char is: " + character)
    
    octal = '{0:03b}'.format(numeric)

    firstBit = int(octal[0])
    secondBit = int(octal[1])
    thirdBit = int(octal[2])

    keyBoardTop = True if firstBit == 1 else False
    GPIO.output(25, keyBoardTop)
    keyBoardMiddle = True if secondBit == 1 else False
    GPIO.output(8, keyBoardMiddle)
    keyBoardBottom = True if thirdBit == 1 else False
    GPIO.output(7, keyBoardBottom)

def stateSetOne():
    if (GPIO.input(22) == 0 and GPIO.input(27) == 0 and GPIO.input(17) == 0 and GPIO.input(4) == 0):
        return True
    return False

def guessingState():
    if (GPIO.input(22) == 1 and GPIO.input(27) == 1 and GPIO.input(17) == 0 and GPIO.input(4) == 0):
        return True
    return False

def toggle(switchState, pinNum):

    if switchState == True:
        switchState = False
        GPIO.output(pinNum, GPIO.LOW)
    else:
        switchState = True
        GPIO.output(pinNum, GPIO.HIGH)

    return switchState

def cyclePC():
    GPIO.output(18,GPIO.HIGH)
    time.sleep(.05)
    GPIO.output(18,GPIO.LOW)

    if (parsePcAsInt(parsePC()) >= 4):
        skipToBeginningState()

def parsePcAsInt(pc):
    return int(pc, 2)

def parsePC():
    return str(GPIO.input(4)) + str(GPIO.input(17)) + str(GPIO.input(27)) + str(GPIO.input(22))

def skipToBeginningState():
    global pcSwitch
    # Initialize the game to state "setOne"
    while not stateSetOne():
        pcSwitch = toggle(pcSwitch, 18)

skipToBeginningState()

while True:
    currentPc = parsePC()
    currentState = parsePcAsInt(currentPc)

    userPrompt = ""
    saveGuessLabel = "Store value"
    
    if currentState == 0:
        userPrompt = "Store letter 1"
    elif currentState == 1:
        userPrompt = "Store letter 2"
    elif currentState == 2:
        userPrompt = "Store letter 3"
    elif currentState == 3:
        userPrompt = "Make a guess"
        saveGuessLabel = "Submit guess"

    print("Program Counter: {}".format(currentPc))
    print("GAME PHASE: " + userPrompt + "\n")
    
    if currentState == 3:
        print("Incorrect Guesses: {}".format(incorrectGuesses))
    
    print("Databus: {}{}{}".format(int(keyBoardTop), int(keyBoardMiddle), int(keyBoardBottom)))
    
    selection = input("{}\n{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n{}{}\n".format(
        "1: Next (PC++)",
        "2: " + saveGuessLabel,
        "a: ", '{0:03b}'.format(0),
        "b: ", '{0:03b}'.format(1),
        "c: ", '{0:03b}'.format(2),
        "d: ", '{0:03b}'.format(3),
        "e: ", '{0:03b}'.format(4),
        "f: ", '{0:03b}'.format(5),
        "g: ", '{0:03b}'.format(6),
        "h: ", '{0:03b}'.format(7)
        ))

    if selection == '1':
        cyclePC()

    elif selection == '2':
        #saveGuessState = toggle(saveGuessState, 2)
        if guessingState():
            print("LED on")
            GPIO.output(2,GPIO.HIGH)
            time.sleep(.5)
            incorrectGuesses = (incorrectGuesses + 1) if GPIO.input(24) == 1 else incorrectGuesses
            time.sleep(.5)
            print("LED off")
            GPIO.output(2,GPIO.LOW)
        else:
            print("LED on")
            GPIO.output(2,GPIO.HIGH)
            time.sleep(1)
            print("LED off")
            GPIO.output(2,GPIO.LOW)
    elif len(selection) == 1 and selection[0] in 'abcdefgh':
        encode(selection[0])
    else:
        print("Invalid input")