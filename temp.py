from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent): # Comenzamos definiendo a cada agente
    def __init__(self, pos, model, agent_type):
        
 # En este caso, hay dos tipos (0,1) que son mayoría y minoría
 
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # Modelamos el movimiento a una casa vacía condicionado a ser infeliz (no tener vecinos o tener pocos vecinos similares)
        if similar < self.model.homophily or self.model.grid.neighbor_iter==0:
            self.model.grid.move_to_empty(self)
        else:
            self.model.felices += 1 # Si el agente es feliz, no se mueve y se contabiliza un agente feliz


class Schelling(Model):
    '''
    Modelo de Schelling con diferentes tipos de agentes.
    '''

    def __init__(self, height=50, width=50, density=0.8, minority_pc=0.2, homophily=3): # Aquí establecemos el tamaño máximo del Grid, aunque en server.py definimos dentro de qué área se desarrolla el modelo
        self.height = height
        self.width = width 
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False) # A diferencia del MultiGrid, el SingleGrid solo permite un agente en cada espacio

        self.felices = 0
        self.datacollector = DataCollector(
            {"felices": "felices"},  # Agentes felices
 
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

# En esta sección, etiquetamos a cada agente según su tipo 
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self): # Este step permite que el modelo siga corriendo hasta que todos los agentes sean felices 
        self.felices = 0
        self.schedule.step()
        # Por fines gráficos, recolectamos la información sobre la cantidad de agentes felices
        self.datacollector.collect(self)

        if self.felices == self.schedule.get_agent_count():
            self.running = False