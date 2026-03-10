# Checker Rules

## Piece Colors
White and Black
*Canonically checkers use many different colors for pieces, what matters is one color is darker than the other.*

## Start Play
The player with the darker pieces will start first.  Each player will place their pieces on exclusively dark squares.  Placing pieces on alternating squares, each player starts with a piece on their far left closest row.  The three closest rows to the player will contain their 12 pieces, with the middle row placement being offset to stay on the dark squares of the board.

Each player will start with 5 minutes on their clock, similar to chess.  When the game starts, each player will receive the board state and information about the game (TODO: doc link).  Black's clock will start and once they make a valid move on the board, black's clock will pause. Then white's clock will start and so on until the one player wins, a draw, or one player's clock runs out.  The exception to the clock moving from one player to the other is when one player must make multiple captures in a row.

## Rules
- Pieces can only make diagonal moves
- Pieces can only be on dark squares of the board
- Pieces can only move one diagonal square unless capturing
- Captures are made by jumping diagonally over an opposing piece into an empty square
  - If a capture is available, the player must capture.  If there are two or more capture choices, the player can freely decide what to capture.
  - Multiple capture jumps in a row is permitted.  This means one player will (in multi-capture situations) be forced to make multiple valid moves in a row.
- Pieces that reach the opposite side of their starting position will become kings and queens
  - Kings/Queens are allowed to move and capture both forward and backward (diagonally)
- The first player to eliminate all enemy pieces or completely block all enemy pieces will be victorious
- Draws
  - Both players agree to a draw (meme)
  - If the same position repeats three times during the game
  - If neither player has moved one of their normal pieces towards the opposing player in the last 40 moves
  - If no pieces have been captured in the last 40 moves

## QUESTIONS/RESEARCH
- Force jumping? Jumps are mandatory according to the ACF and WCDF
  - > All capturing moves are compulsory, whether offered actively or passively. If
there are two or more ways to jump, a player may select any one that they wish, not
necessarily that which gains the most pieces. Once started, a multiple jump must be
carried through to completion. A man can only be jumped once during a multiple
jumping sequence.

- In a multi-capture scenario -> one move includes all capture moves or each capture move is sent individually
- Allow player to send a draw request, allowing them to agree to a draw at anytime (so you can spam them xD)
- Draws?
    -  Definition of a Draw
    - The game is drawn if at any stage both players agree on such a result (v). A
    game shall also be declared drawn where:
    - At any stage of the game, a player can demonstrate to the satisfaction
    of the referee that with their next move they would create the same position
    for the third time during the game.
    - At any stage of the game, a player can demonstrate to the satisfaction
    of the referee that both the following conditions hold:
    a) Neither player has advanced an uncrowned man towards the king-row
    during their own previous 40 moves.
    b) No pieces have been removed from the board during their own
    previous 40 moves


## Sources
- American Checkers Federation (ACF) Tournament Rules (2012)
  - https://nccheckers.org/NCCA/ACF%20Rules%20for%20National%20Tournaments.htm
- World Checkers Draughts Federation (WCDF) Rules
  - https://wcdf.net/rules/rules_of_checkers_english.pdf