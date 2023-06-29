from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue # on importe ceci pour utiliser la PriorityQueue dans ucs car on veut sortir l'élément de coût minimum


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

def step_cost(prev_state, next_state): # ajouté pour ucs afin d'éviter de manger la grosse capsule
    if len(prev_state.getCapsules()) > len(next_state.getCapsules()):
        return 6 # 6 pts perdu pour le mouvement + la grosse capsule mangée
    else:
        return 1 # 1 pt perdu pour le mouvement


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
            self.moves = self.ucs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP

    def ucs(self, state): #uniform cost search, coût minimum en premier
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
        fringe = PriorityQueue()
        fringe.push((state, path, 0.), 0.)
        closed = set() # set avec les noeuds déjà parcouru

        while True:
            if fringe.isEmpty():
                return [] # pacman ne bouge pas

            _, (current, path, cost) = fringe.pop() # le "_" notifie que la première variable est inutile

            current_key = key(current)

            if current.isWin(): # si on trouve la case objectif, on retourne le chemin
                return path 

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    next_cost = cost + step_cost(current, next_state)
                    fringe.push((next_state, path + [action], next_cost), next_cost)