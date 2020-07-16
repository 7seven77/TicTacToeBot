# NaCMatch

# NOTES
# Turn 1 means it is the opponents turn
# Turn -1 means it is the challengers turn
# x is the marker for the opponent
# o is the marker for the challenger

# Stores information about a Noughts and Crosses match
class NaCMatch():

    winConditions = [[1, 2, 3], [4, 5, 6], [7, 8, 9],
           [1, 4, 7], [2, 5, 8], [3, 6, 9],
           [1, 5, 9], [3, 5, 7]]
    
    # Create a match between two players
    def __init__(self, challenger, opponent):
        self.board = '.........'
        self.validMoves = ['1', '2' ,'3', '4', '5', '6', '7', '8', '9']
        self.challenger = challenger
        self.opponent = opponent
        self.turn = 1

    # Place a token on the board
    def takeTurn(self, player, move):
        if self.getCurrentPlayer() != player:
            return 'Player'
        if not move in self.validMoves:
            return 'Move'
        self.validMoves.remove(move)
        index = int(move) - 1
        board = self.board
        board = board[:index] + self.getCurrentToken() + board[index + 1:]
        self.board = board
        self.nextTurn()
        return self.board

    # Get the current player's token
    def getCurrentToken(self):
        if self.turn == 1:
            return 'x'
        else:
            return 'o'

    # Get the player who's turn it is
    def getCurrentPlayer(self):
        if self.turn == 1:
            return self.opponent
        else:
            return self.challenger

    # Get the player who's turn it is next
    def getNextPlayer(self):
        if self.turn == 1:
            return self.challenger
        else:
            return self.opponent
    
    # Returns the victor if there is one
    # Returns '.' if there isn't
    def getVictor(self):
        for combo in self.winConditions:
            board = self.board
            symbol = board[combo[0] - 1]
            if symbol != '.' and symbol == board[combo[1] - 1] and symbol == board[combo[2] - 1]:
                    if symbol == 'x':
                        return self.opponent
                    else:
                        return self.challenger
        return '.'

    # Returns a list with the players in the match
    def getPlayers(self):
        return [self.challenger, self.opponent]
    
    # Returns True if the game is complete
    def isOver(self):
        return len(self.validMoves) == 0 or self.getVictor() != '.'
    
    # Moves the game forward by one turn   
    def nextTurn(self):
        self.turn *= -1

    # Use only for tests
    # Does not affect validMoves
    def setBoard(self, newBoard):
        self.board = newBoard

#######################################################

### Test Cases

def runAllTests():
    testRegularPlay()
    testInvalidPlayer()
    testInvalidMove()
    testVictory()
    testIsOver()
        
## Check that a valid player can make a valid move
def testRegularPlay():
    match = NaCMatch('q','p')
    assert match.takeTurn('p', '1') == 'x........'
    assert match.takeTurn('q', '3') == 'x.o......'
    assert match.takeTurn('p', '9') == 'x.o.....x'

## Check that an invalid player cannot make a move
def testInvalidPlayer():
    match = NaCMatch('q','p')
    assert match.takeTurn('g','1') == 'Player'
    assert match.takeTurn('q','1') == 'Player'

## Check a valid player cannot make an invalid move
def testInvalidMove():
    match = NaCMatch('q','p')
    assert match.takeTurn('p', '90') == 'Move'
    assert match.takeTurn('p', '1.6') == 'Move'
    assert match.takeTurn('p', 'h') == 'Move'

def testVictory():
    match = NaCMatch('p', 'q')
    match.setBoard('abcdefghj')
    assert match.getVictor() == '.'
    match.setBoard('xxx......')
    assert match.getVictor() == 'q'
    match.setBoard('xxxooo...')
    assert match.getVictor() == 'q'

def testIsOver():
    match = NaCMatch('p', 'q')
    assert match.isOver() == False
    match.takeTurn('q', '1')
    match.takeTurn('p', '2')
    match.takeTurn('q', '3')
    match.takeTurn('p', '4')
    match.takeTurn('q', '5')
    match.takeTurn('p', '6')
    match.takeTurn('q', '7')
    match.takeTurn('p', '8')
    match.takeTurn('q', '9')
    assert match.isOver() == True
    match = NaCMatch('p', 'q')
    match.setBoard('xxxoooooo')
    assert match.isOver() == True
    
