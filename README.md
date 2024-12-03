# Poker-AI
Alexander Hixson, Anosh Taraporavala, Aria Kafie, Colin Treziok, Vasista Dhyasani

install PyPokerEngine
    pip intall PyPoker Engine

Run code with
    python3 config.py

    Results print when the config parameter 'verbose' is set to 1
    The program will print to terminal the start of each round, each street, and show each decision each agent makes. 
    At the end of each round the chip count of each agent is printed.
    Optionally the cards of each agent can be printed so we can more easily understand each round.

        To interpret the results, simply watch the terminal command line. For each hand, it will show each player's 2 hole cards first. It will show each players chip total. If an agent has more chips, that means they are currently winning. You will then see the preflop betting. 
            EX: Street "preflop" started. (community card = [])
                "Goated Poker-AI4" declared "raise:6"
                "Goated Poker-AI2" declared "call:6"
            This example would happen if there are only 2 players left.

        Then, if it gets to the flop, it will display the flop. 
            EX: Street "flop" started. (community card = ['H7', 'DA', 'S6'])

        Then, the flop betting will commence. After that, the turn comes.
            EX: Street "turn" started. (community card = ['H7', 'DA', 'S6', 'D7'])

        Then the river betting will commence. After that, the river comes.
            EX: Street "river" started. (community card = ['H7', 'DA', 'S6', 'D7', 'HK'])
        
        Then, the final round of betting happens. If there are 2 or more players left, the players hands will be compared. Whoever has the strongest hand wins the amount of chips in the pot.

        If someone at any point in the hand wants to exit the hand, they can fold. They reliquish their chance of winning the pot but no longer have to put any more chips in the pot. In this example, player 2 checked, player 4 raised, and player 2 folded, indicating they had a weak hand.
            EX: "Goated Poker-AI2" declared "call:0"
                "Goated Poker-AI4" declared "raise:6"
                "Goated Poker-AI2" declared "fold:0"

    If you want to analyze the agent's play, you can put a hand into GTO wizard. There, you can analyze the hand to figure out the best moves in each position according to GTO, game theory optimal play. Keep in mind that the GoatedAgent plays exploitatively, so each move is not always going to be according to GTO.
