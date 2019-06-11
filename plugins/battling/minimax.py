
inf = 0x3f3f3f3f

class BattleMon: 
  def __init__(self, species, moves, item, ability, level, health, status, volatile_status, boosts, active):
    self.species = species
    self.moves = moves
    self.item = item
    self.ability = ability
    self.level = level
    self.health = health
    self.status = status
    self.volatile_status = volatile_status
    self.boosts = boosts
    self.active = active
  

def minimax(player_team, enemy_team, agent_id, depth, max_depth, alpha=-inf, beta=inf, action):
  """
  """
  if depth == max_depth || check_for_terminal():
    return utility()
  else: 
    # simulate player moves
    if agent_id == 0:
      moves = []
      for move in moves:
        pt, et = update(player_team, enemy_team, move)
        res = minimax(pt, et, 1, depth+1, max_depth, alpha, beta)
        alpha = max(alpha, res)
        if alpha >= beta:
          break
      if depth == 0:
        action = 1
        # select move
      # perform move from player 1
    # simulate enemy moves
    else:

    


def check_for_terminal():
  """
  """
  pass

def utility():
  """
  """
  pass





