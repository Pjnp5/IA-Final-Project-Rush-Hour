from copy import deepcopy
import common

def check_orientation(car_coords):
    if car_coords[0].y == car_coords[-1].y:
        return 'H'
    else:
        return 'V'

def make_board(Map, N):
      new_grid = (str)(Map).split(' ')[1]
      board = [new_grid[idx:idx + N] for idx in range(0, len(new_grid),N)]
      new_grid2 = []
      for line in board:
        linha=[]
        for letter in line:
          if letter != 'o' and letter != 'x':
            if check_orientation(Map.piece_coordinates(letter)) == 'V':
              if letter == 'O':
                letter = 'z'
              else:
                letter = letter.lower()
          linha.append(letter)
        new_grid2.append(linha)
      return new_grid2

def make_str_board(board):
  return '\n'.join(''.join(a) for a in board)


def copy_board(board):
  return [a[:] for a in board]

def is_solved(board, gridsize, start_row):
  if board[start_row][gridsize -1] == 'A':
    return True
  return False

def get_next_states(board, gridsize):
  processed_chars_set = set(['o'])
  next_states = []
  for row in range(gridsize):
    for column in range(gridsize):
      char = board[row][column]
      # Ver se esta char já foi tratada e se não é nem espaço nem impedimento
      if char not in processed_chars_set and char != 'x' and char != 'o':
        # adicionar a letra do carro aos carros processados
        processed_chars_set.add(char)
        # criar as varáveis responsáveis por ver os movimentos possiveis dos carros e as posições destes
        vertical_checker = 0
        horizontal_checker = 0
        # se a letra não for capital então o carro é vertical
        is_vertical = not char.isupper()
        if is_vertical:
          #se for vertical então vamos dizer que a sua variavél vertical é igual a 1, vai servir para ver espaços por cima e por baixo da peça (por exemplo)
          vertical_checker = 1
        else:
          #se for horizontal então vamos dizer que a sua variavél horizontal é igual a 1
          horizontal_checker = 1
        # os valores máximos e minimos são inicializádos com os valores da row e da coluna da peça
        piece_min_row, piece_max_row = row, row
        piece_min_col, piece_max_col = column, column
        # este while tem como objetivo saber onde começa a peça que estamos a usar, sendo assim vai retirar ao valor minimo atual o valor da variavel antes criada
        # se for um carro horizontal vai diminuir 1 ao valor minimo da coluna
        # se for um carro vertical vai diminuir 1 ao valor minimo da row
        while piece_min_row - vertical_checker >= 0 and piece_min_col - horizontal_checker >= 0 and board[piece_min_row - vertical_checker][piece_min_col - horizontal_checker] == char:
          # se for vertical vertical_checker = 1 e horizontal_checker = 0, logo vai andando 1 para cima até deixar de ser a mesma peça ou acabar o tabuleiro
          piece_min_row -= vertical_checker
          # se for horizontal vertical_checker = 0 e horizontal_checker = 1, logo vai andando 1 para trás até deixar de ser a mesma peça ou acabar o tabuleiro
          piece_min_col -= horizontal_checker

        # este while tem como objetico saber onde acaba a peça que estamos a usar, sendo assim vai somar ao valor máximo atual o valor da variavel antes criada
        # se for um carro horizontal vai somar 1 ao valor máximo da coluna
        # se for um carro vertical vai somar 1 ao valor máximo da row
        while piece_max_row + vertical_checker < gridsize and piece_max_col + horizontal_checker < gridsize and board[piece_max_row + vertical_checker][piece_max_col + horizontal_checker] == char:
          # se for vertical vertical_checker = 1 e horizontal_checker = 0, logo vai andando 1 para baixo até deixar de ser a mesma peça ou acabar o tabuleiro
          piece_max_row += vertical_checker
          # se for horizontal vertical_checker = 0 e horizontal_checker = 1, logo vai andando 1 para a frente até deixar de ser a mesma peça ou acabar o tabuleiro
          piece_max_col += horizontal_checker

        # Aqui vemos se a peça está encostada ao lado esquerdo ou ao topo do tabuleiro, e se a peça pode mexer-se para cima ou para a esquerda
        # A 3ª condição só verificada se as anteriores forem verdade
        # Se o carro for vertical:
        # O vertical_checker é 1 logo piece_min_row - vertical_checker = piece_min_row - 1
        # O horizontal_checker é 0 logo piece_min_col - horizontal_checker = piece_min_col
        # Em resumo checa se o espaço em cima da peça está vazio
        # Se o carro for horizontal:
        # O vertical_checker é 0 logo piece_min_row - vertical_checker = piece_min_row
        # O horizontal_checker é 1 logo piece_min_col - horizontal_checker = piece_min_col - 1
        # Em resumo checa se o espaço à esquerda da peça está vazio
        if piece_min_row - vertical_checker >= 0 and piece_min_col - horizontal_checker >= 0 and board[piece_min_row - vertical_checker][piece_min_col - horizontal_checker] == 'o':
          # o espaço em cima ou à esquerda da peça está vazio, copiamos o board atual e na copia fazemos as alterações como se movessemos a peça nessa direção
          # copiar o tabuleiro
          next_state = copy_board(board)
          # mexer a peça para o lugar vazio
          next_state[piece_min_row - vertical_checker][piece_min_col - horizontal_checker] = char
          # o ultimo espaço do lado contário que a peça ocupava fica vazio
          next_state[piece_max_row][piece_max_col] = 'o'
          # se for letra minuscula é carro vertical então vai mexer-se para cima, se for maiuscula move para baixo
          if char.islower():
            # mover a peça (transformar em capital por o jogo pede assim) para cima
            move = (char.upper(), "w")
          else:
            #mover a peça para a esquerda
            move = (char, "a")
          # dar apende no array de moves com os novos estados possiveis
          next_states.append((next_state, move))

        # Aqui vemos se a peça está encostada ao lado direito ou ao fundo do tabuleiro, e se a peça pode mexer-se para baixo ou para a direita
        # A 3ª condição só verificada se as anteriores forem verdade
        # Se o carro for vertical:
        # O vertical_checker é 1 logo piece_min_row + vertical_checker = piece_min_row + + 1
        # O horizontal_checker é 0 logo piece_min_col + horizontal_checker = piece_min_col 
        # Em resumo checa se o espaço em baixo da peça está vazio
        # Se o carro for horizontal:
        # O vertical_checker é 0 logo piece_min_row + vertical_checker = piece_min_row
        # O horizontal_checker é 1 logo piece_min_col + horizontal_checker = piece_min_col + 1
        # Em resumo checa se o espaço à direita da peça está vazio
        if piece_max_row + vertical_checker < gridsize and piece_max_col + horizontal_checker < gridsize and board[piece_max_row + vertical_checker][piece_max_col + horizontal_checker] == 'o':
          # o espaço em baixo ou à direita da peça está vazio, copiamos o board atual e na copia fazemos as alterações como se movessemos a peça nessa direção
          # copiar o tabuleiro
          next_state = copy_board(board)
          # mexer a peça para o lugar vazio
          next_state[piece_min_row][piece_min_col] = 'o'
          # o ultimo espaço do lado contário que a peça ocupava fica vazio
          next_state[piece_max_row + vertical_checker][piece_max_col + horizontal_checker] = char
          # mover a peça (transformar em capital por o jogo pede assim) para baixo
          if char.islower():
            move = (char.upper(), "s")
          # mover a peça para a direita
          else:
            move = (char, "d")
          # dar apende no array de moves com os novos estados possiveis
          next_states.append((next_state, move))
  # retornar à funçao search todos os novos estados possiveis
  return next_states

def search(board, gridsize, start_row):
  # criar uma queue que vai funcionar como os nodes
  queue = [(0, [board], [])]
  # todos os tabuleiros que já tivemos, em branco no inicio porque ainda nã houve nenhum
  board_set = set()
  # enquanto houver queue e não for encontrada uma jogada vencedora isto corre
  while queue:
    # vamos usar o primeiro elemento da queue
    path = queue.pop(0)
    # ver se este elemento já é a solução (carro vermelho no fim da sua linha)
    if is_solved(path[1][-1], gridsize, start_row):
      return path[1], path[2]

    # obter os estados possiveis tendo em conta o ultimo tabuleiro do path
    for next_state in get_next_states(path[1][-1], gridsize):
      # por cada novo estado, vamos ver se este já foi visitado (se tinha um tabuleiro igual)
      # se já visitámos o tabuleiro simpleste damos discard dele
      if make_str_board(next_state[0]) not in board_set:
        # se ainda não tinhamos visitado este tabuleiro das append ao conjunto de tabuleiros visitados
        board_set.add(make_str_board(next_state[0]))
        # e damos também append deste novo estado à queue para mais tarde poder visitá-lo e obter os estados que vêm a partir dele
        queue.append((path[0] + 1, path[1] + [next_state[0]], path[2] + [next_state[1]]))
      

  return []

class Bot:
  def __init__(self, grid, cursor):
    self.cursor = cursor
    self.final_moves = None
    self.Map = common.Map(grid)
    self.final_grids = None

  def run(self, new_grid, cursor, selected):
    self.cursor = cursor
    self.Map = common.Map(new_grid)

    if self.final_moves == [] or self.final_moves == None:
        board = make_board(common.Map(new_grid), self.Map.grid_size)
        self.final_grids ,self.final_moves = search(board, self.Map.grid_size, self.Map.piece_coordinates(self.Map.player_car)[0].y)
    else:
      coisa = [True if "O" in row else False for row in self.Map.grid]
      if True in coisa:
        grid = [[letter.lower() if letter != 'O' else letter for letter in row ] for row in deepcopy(self.Map.grid)]
        grid2 = [[letter.lower() if letter != 'O' else letter for letter in row ] for row in deepcopy(self.final_grids[0])]
        for row in range(len(grid2)):
          for col in range(len(grid2)):
            if grid2[row][col] == 'z':
              grid2[row][col] = 'O'
      else:
        grid = [[letter.lower() for letter in row ] for row in deepcopy(self.Map.grid)]
        grid2 = [[letter.lower() for letter in row ] for row in deepcopy(self.final_grids[0])]

      if grid != grid2 and self.Map.grid_size < 8:
        board = make_board(common.Map(new_grid), self.Map.grid_size)
        self.final_grids ,self.final_moves = search(board, self.Map.grid_size, self.Map.piece_coordinates(self.Map.player_car)[0].y)
      movimento = self.final_moves[0]

      if True in coisa:
        for row in range(len(movimento[0])):
          for col in range(len(movimento[0])):
            if movimento[0][row][col] == 'z':
              movimento[0][row][col] = 'O'

        if movimento[0] == 'Z':
          movimento = ('O', movimento[1])

      return Bot.move_cursor(self, movimento[0], selected, movimento[1])

  def check_orientation(self, car_coords):
    if car_coords[0].y == car_coords[-1].y:
        return 'H'
    else:
        return 'V'

  def move_cursor(self, letter, selected, key_direction):
    letter_coords = self.Map.piece_coordinates(letter)
    if self.Map.get(common.Coordinates(self.cursor[0], self.cursor[1])) != letter:
      if selected == "":
          if self.cursor[1] > letter_coords[0].y:
              return "w"
          elif self.cursor[1] < letter_coords[0].y:
              return "s"
          elif self.cursor[0] > letter_coords[0].x:
              return "a"
          elif self.cursor[0] < letter_coords[0].x:
              return "d"
      else:
            return " "
    else:
      if selected == "":
        return " "
      else:
        self.final_moves.pop(0)
        self.final_grids.pop(0)
        return key_direction