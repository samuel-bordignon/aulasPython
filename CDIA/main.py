from dataclasses import dataclass
import pyxel
import math
import random

#CORES permitidas: 
#COLOR_BLACK
#COLOR_NAVY
#COLOR_PURPLE
#COLOR_GREEN
#COLOR_BROWN
#COLOR_DARK_BLUE
#COLOR_LIGHT_BLUE
#COLOR_WHITE
#COLOR_RED
#COLOR_ORANGE
#COLOR_YELLOW
#COLOR_LIME
#COLOR_CYAN
#COLOR_GRAY
#COLOR_PINK
#COLOR_PEACH

#Classe que define as mercadorias para pontuação
#Devem ser coletadas pelo jogador
@dataclass
class Merch:
    x:int
    y:int
    acceleration={'x':0.0,'y':0.0}
    velocity={'x':0.0,'y':0.0}
    gravity_force={'x':0.0,'y':0.0}
    points:int

    def get_color(self):
        match self.points:
            case 10:
                return pyxel.COLOR_CYAN
            case 20:
                return pyxel.COLOR_LIME
            case 40:
                return pyxel.COLOR_PINK
            case 80:
                return pyxel.COLOR_PEACH
            case -10:
                return pyxel.COLOR_DARK_BLUE
            case -30:
                return pyxel.COLOR_ORANGE
            case -50:
                return pyxel.COLOR_RED
            case _:
                return "Unknown Status"

# Classe para as informações das naves
@dataclass
class Ship:
    x:int
    y:int
    rotation: float = 0 #angulo de rotação (radianos)
    rotation_dir: int = 0 # -1=esquerda, 0=sem rotação, 1=direita
    exploded:bool = False
    points:int = 0
    lives:int = 3
    velocity= {'x': 0.0,'y': 0.0}
    acceleration= {'x': 0.0,'y': 0.0}
    gravity_force= {'x': 0.0,'y': 0.0}
    thrust_force= {'x': 0.0,'y': 0.0}
    total_force= {'x': 0.0,'y': 0.0}
    
##########################
### Definição de constantes para configuração
##########################
#Constantes para configuração do movimento das naves
SHIP_RADIUS = 10
ROTATION_SPEED = 0.03
TOP_SPEED = 5
DRAG = 0.5
MAX_ACCELERATION = 2
THRUST_DELTA = 0.04
SHIP_MASS = 4
#Constantes para definição da estrela
STAR_POSITION = { 'x': 150, 'y': 150 }
STAR_SCALE = 3
STAR_RADIUS = 8 * STAR_SCALE
STAR_COLOR = '#F5A927'
STAR_MASS = 100
#Constantes para as mercadorias
SCRAP_RADIUS = 2
SCRAP_MASS = 1
#Definições de pontuação para distribuição aleatória
POINTS = [10,20,-10,40,-30,80,-50]
WEIGHTS = [10,11,20,21,40,41,42]
WEIGHT_BUDGET = 1000

#Mercadorias que podem ser coletadas pelo jogador
MERCHS_IN_PLAY = []

GAVITY_CONSTANT = 4

STEERING = 0.12  # entre 0.05 e 0.25


collision_message_timer = 0

auditoria = { 'dv':{},'np':{} }

#################################
### Funções para o controle da movimentação das naves
#################################
def set_rotation(ship, direction) :
    if ship.rotation_dir == direction :
        return
    if ship.rotation_dir == -direction :
        ship.rotation_dir = 0
    else:
        ship.rotation_dir = direction

def unset_rotation(ship, direction) :
    if ship.rotation_dir == direction :
        ship.rotation_dir = 0
    elif ship.rotation_dir == -direction :
        return
    
def rotate_ship(ship):
    if ship.rotation_dir != 0:
        ship.rotation += ship.rotation_dir * ROTATION_SPEED

def move_ship(ship):
    ship.total_force['x'] = ship.thrust_force['x'] + ship.gravity_force['x']
    ship.total_force['y'] = ship.thrust_force['y'] + ship.gravity_force['y']

    ship.acceleration['x'] = ship.total_force['x'] / SHIP_MASS
    ship.acceleration['y'] = ship.total_force['y'] / SHIP_MASS

    ship.velocity['x'] += ship.acceleration['x']
    ship.velocity['y'] += ship.acceleration['y']

    # Faz a velocidade acompanhar parcialmente a direção da nave
    speed = math.sqrt(ship.velocity['x']**2 + ship.velocity['y']**2)

    desired_vx = speed * math.cos(ship.rotation)
    desired_vy = speed * math.sin(ship.rotation)

    ship.velocity['x'] += (desired_vx - ship.velocity['x']) * STEERING
    ship.velocity['y'] += (desired_vy - ship.velocity['y']) * STEERING

    # Limita velocidade máxima
    speed = math.sqrt(ship.velocity['x']**2 + ship.velocity['y']**2)

    if speed > TOP_SPEED:
        scale = TOP_SPEED / speed
        ship.velocity['x'] *= scale
        ship.velocity['y'] *= scale

    ship.x += ship.velocity['x']
    ship.y += ship.velocity['y']

def set_thrust_force(ship, magnitude):
    thrust_force = magnitude * THRUST_DELTA

    ship.thrust_force['x'] = thrust_force * math.cos(ship.rotation)
    ship.thrust_force['y'] = thrust_force * math.sin(ship.rotation)

def set_gravity_force(ship):
    ux, uy, distance = get_unity_ship(ship)
    gravity_force = GAVITY_CONSTANT * ((SHIP_MASS * STAR_MASS) / pow(distance, 2))
    ship.gravity_force['x'] = gravity_force * ux
    ship.gravity_force['y'] = gravity_force * uy

def get_unity_ship(ship):
    dx = STAR_POSITION['x'] - ship.x
    dy = STAR_POSITION['y'] - ship.y
    distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    ux = dx / distance
    uy = dy / distance

    return ux, uy, distance

def move_scrap(scrap):
    dx = STAR_POSITION['x'] - scrap.x
    dy = STAR_POSITION['y'] - scrap.y

    distance = math.sqrt(dx**2 + dy**2)

    ux = dx / distance
    uy = dy / distance

    gravity_force = GAVITY_CONSTANT * ((SCRAP_MASS * STAR_MASS) / distance**2)

    scrap.gravity_force['x'] = gravity_force * ux
    scrap.gravity_force['y'] = gravity_force * uy

    scrap.acceleration['x'] = scrap.gravity_force['x']
    scrap.acceleration['y'] = scrap.gravity_force['y']

    scrap.velocity['x'] += scrap.acceleration['x']
    scrap.velocity['y'] += scrap.acceleration['y']

    scrap.x += scrap.velocity['x']
    scrap.y += scrap.velocity['y']

#####################
#### Funções de inicialização das Mercadorias (pontos)
#####################
# Seleção aleatória com base em pesos

def select_points():
    total = 0
    for w in WEIGHTS:
        total += w
    # Número aleatório [1, total]
    rd = random.randint(1,total)
    cursor = 0
    for i in range(len(WEIGHTS)):
        cursor += WEIGHTS[i]
        if (cursor >= rd):
            return (POINTS[i],WEIGHTS[i])
    return -10
    
def spawn_scrap():
   budget = WEIGHT_BUDGET
   while budget > 0:
       p,w = select_points()
       # Cria a mercadoria em uma posição aleatória dentro do mapa (entre 0 e 300)
       #TO-DO: criar lógica para evitar que seja criada muito próxima da estrela
       #TO-DO: Criar lógica para espalhar melhor os pontos no mapa
       scrap = Merch(random.randint(0,300),random.randint(0,300),p)
       MERCHS_IN_PLAY.append(scrap)
       budget -= w

###########################
#### Funções para verificação de colisões
###########################

#Verifica colisões das mercadorias
def check_scrap_collision(ship):
    #TO-DO: Verifica se a nave encostou nas cargas
    #TO-DO: Verifica se as cargas encostaram na estrela
    #RETORNA: Lista de Merchs pegos pela nave, lista de Merchs engolidos pela estrela
    for scrap in MERCHS_IN_PLAY:
        dx = scrap.x - STAR_POSITION['x']
        dy = scrap.y - STAR_POSITION['y']
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
        if distance < SHIP_RADIUS + SCRAP_RADIUS:
            MERCHS_IN_PLAY.remove(scrap)
            ship.points += abs(scrap.points)
        if distance < SHIP_RADIUS + SCRAP_RADIUS:
            MERCHS_IN_PLAY.remove(scrap)
            
    
# Verifica colisões da nave
def check_collisions(ship):
    global collision_message_timer
    dx = ship.x - STAR_POSITION['x']
    dy = ship.y - STAR_POSITION['y']
    distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    if distance < SHIP_RADIUS + STAR_RADIUS or ship.x < 0 or ship.x > 300 or ship.y < 0 or ship.y > 300:
        ship.lives -= 1

        ship.x= 50
        ship.y= 50

        ship.velocity['x'] = 0
        ship.velocity['y'] = 0

        ship.acceleration['x'] = 0
        ship.acceleration['y'] = 0

        ship.total_force['x'] = 0
        ship.total_force['y'] = 0

        ship.thrust_force['x'] = 0
        ship.thrust_force['y'] = 0

        ship.gravity_force['x'] = 0
        ship.gravity_force['y'] = 0

        ship.rotation_dir = 0
        ship.rotation = 0

        collision_message_timer = 180
            

######################
### Classe principal da game engine
######################
class App:
    c_needle = Ship(50,50)
    c_wedge = Ship(250,250)

    def __init__(self):
        pyxel.init(300, 300)
        pyxel.load("my_resource.pyxres")
        self.x = 0
        spawn_scrap()
        pyxel.run(self.update, self.draw)
        
    # Processa a entrada de teclado do usuário
    def processa_teclado(self):
        if pyxel.btn(pyxel.KEY_W):
            set_thrust_force(self.c_needle, 1)
        elif pyxel.btn(pyxel.KEY_S):
            set_thrust_force(self.c_needle, -1)
            
        if pyxel.btn(pyxel.KEY_A):
            set_rotation(self.c_needle, -1)
        elif pyxel.btn(pyxel.KEY_D):
            set_rotation(self.c_needle, 1)

        if not pyxel.btn(pyxel.KEY_A):
            unset_rotation(self.c_needle, -1)
            
        if not pyxel.btn(pyxel.KEY_D):
            unset_rotation(self.c_needle, 1)

    #Atualiza as informações do jogo ANTES de desenhar cada frame
    # 1. Verifica se há alguma tecla pressionada
    # 2. Aplica rotação na Nave
    # 3. Aplica o movimento da nave
    def update(self):
        global collision_message_timer
        rotate_ship(self.c_needle)      # gira primeiro
        self.processa_teclado()          # empuxo já usa o ângulo atualizado
        set_gravity_force(self.c_needle)
        move_ship(self.c_needle)
        check_collisions(self.c_needle)
        check_scrap_collision(self.c_needle)

        for scrap in MERCHS_IN_PLAY:
            move_scrap(scrap)
        
        if collision_message_timer > 0:
            collision_message_timer -= 1
        # Mover as caixas

    #Faz o desenho da tela do jogo
    def draw(self):
        global collision_message_timer
        
        pyxel.cls(0)
        needle = self.c_needle
        wedge = self.c_wedge
        # Estrela no centro da tela
        pyxel.blt(STAR_POSITION['x'], STAR_POSITION['y'], 0, 24, 0, 16, 16, scale=STAR_SCALE)
        # Nave do Jogador 1 (Needle)
        pyxel.blt(needle.x, needle.y, 0, 8, 8, 16, 16, rotate=math.degrees(needle.rotation)+90, colkey=0)
        for scrap in MERCHS_IN_PLAY:
            pyxel.circ(scrap.x, scrap.y, SCRAP_RADIUS, col=scrap.get_color())
        #pyxel.text(48, 100, "Pyxel Code Maker", pyxel.rndi(1, 15))
        pyxel.text(10, 5, f"Vidas: {needle.lives}", pyxel.COLOR_WHITE)
        pyxel.text(10, 12, f"Pontos: {needle.points}", pyxel.COLOR_WHITE)
        
        if collision_message_timer > 0:
            pyxel.text(100, 200, "VOCE COLIDIU", pyxel.COLOR_RED)
            
        # Remover Texto Abaixo. Usado apenas para auxiliar no desenvolvimento
        pyxel.text(10, 25, f"DV: {auditoria['dv']}", pyxel.COLOR_WHITE)
        pyxel.text(10, 35, f"Need: x:{needle.x} y:{needle.y} r:{needle.rotation}", pyxel.COLOR_WHITE)
    
App()
