from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import Queue # on importe ceci pour utiliser la queue dans bfs car dans une queue on peut à l'aide de ".push()" sortir le premier élément


def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    
    # TODO
    return (state.getPacmanPosition(), state.getFood(), tuple(state.getCapsules()))
    # getFood est une matrice non modifiable, "tuple" permet de rendfre la liste getCapsules non modifiable (afin de différencier les tuples de capsules entre eux)


class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.moves:
            self.moves = self.bfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def bfs(self, state): #breadth first search, on fait par couche
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        
        # TODO
        path = [] # le chemin
        fringe = Queue()
        fringe.push((state, path))
        closed = set() # set avec les noeuds déjà parcouru

        while True:
            if fringe.isEmpty():
                return [] # pacman ne bouge pas

            current, path = fringe.pop()

            current_key = key(current)

            if current.isWin(): # si on trouve la case objectif, on retourne le chemin
                return path 

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    fringe.push((next_state, path + [action]))