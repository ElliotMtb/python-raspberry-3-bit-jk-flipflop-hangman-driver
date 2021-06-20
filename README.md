# python-raspberry-3-bit-jk-flipflop-hangman-driver
A python command-line interface to drive raspberry pi GPIO interface to a 3-bit digital circuit game of 'hangman' (guessing game).

The game supports storing a secret word that is 3 letters long, with each letter being 1 of 8 possible characters i.e. an 8-character alphabet. In essence, this digital-circuit game has a 3-bit architecture (2^3 = 8 possible characters).

The actual digital circuit board was designed with basic logic gates (NAND, XOR, JK-FF etc.) on a bread board with an 8 character "keyboard", with inputs sent over a 3-bit bus to 3 sets of 3 (total of 9) JK Flip-Flop gates. So that's 3 memory locations of 3-bits each. Also, a decade counter is used as a means of providing a simple program state machine

The game has 2 Phases, the setup phase and the guessing phase. In the setup phase (Phase 1), the secret word is stored by incrementally looping through each of the 3 memory slots (i.e. "memory addresses") and simultaneously toggling the "store" input signals for the 3 JK Flip-Flops which store the 3-bits making up the letter. The decade counter is incremented each time a letter is stored.

Once each of the 3 letters has been stored, the game state reaches the guessing phase (Phase 2). At this point the 3-bit bus is used to match keyboard guesses against the stored secret word.
