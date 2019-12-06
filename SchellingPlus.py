"""
Tarea 6
Daniel Juárez Bautista
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent): # Comenzamos definiendo a cada agente
    def __init__(self, pos, model, agent_type):
        
# Comenzamos definiendo las características del agente y su movimiento en búsqueda de agentes similares. 
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        vecinos = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1 # El individuo observa cuántos agentes a su alrededor son de su mismo tipo
            if neighbor.type == self.type or neighbor.type!=self.type:
                vecinos += 1 # El individuo observa cuántos vecinos tiene
    
        # Modelamos el movimiento a una casa vacía condicionado a ser infeliz, es decir, no tener los vecinos similares deseados o no tener vecinos. 
        if similar < self.model.homophily or self.model.grid.neighbor_iter==0:
            self.model.grid.move_to_empty(self)
        else:
            self.model.felices += 1 # Si el agente es feliz, no se mueve y se contabiliza un agente feliz


class Schelling(Model):
    '''
    Modelo de Schelling con múltiples tipos de agentes.
    '''
    def __init__(self, height=50, width=50, density=0.8, num_agent_types=2, homophily=3):
        self.height = height
        self.width = width 
        self.density = density
        self.num_agent_types = num_agent_types
        self.homophily = homophily

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=False) # A diferencia del MultiGrid, el SingleGrid solo permite un agente en cada espacio

        self.felices = 0 
        self.datacollector = DataCollector(
            {"felices": "felices"},  # Conservamos la info de agentes felíces en cada tick para graficarlo. 
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

# En esta sección, etiquetamos a cada agente según su tipo 
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                agent_type = self.random.randint(1,num_agent_types)  # Asignamos aleatoriamente el tipo al individuo entre 1 y la cantidad definida por el usuario
                agent = SchellingAgent((x, y), self, agent_type) 
                self.grid.place_agent(agent, (x, y))
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