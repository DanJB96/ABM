"""
Tarea 6
Daniel Juárez Bautista
"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from SchellingPlus import Schelling


class HappyElement(TextElement): # Comenzamos con la parte visual del modelo

    def __init__(self):
        pass

    def render(self, model):
        return "felices: " + str(model.felices) # Debajo del grid observamos la cuenta total de agentes felices

def schelling_draw(agent): # En esta sección, establecemos cómo se representará a cada agente en el grid
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 0.75, "h":0.75, "Filled": "true", "Layer": 0}
    if agent.type == 1:
        portrayal["Color"] = ["red"]
    if agent.type == 2:
        portrayal["Color"] = ["blue"]
    if agent.type == 3:
        portrayal["Color"] = ["cyan"]
    if agent.type == 4:
        portrayal["Color"] = ["yellow"]
    if agent.type == 5:
        portrayal["Color"] = ["black"]
    return portrayal


happy_element = HappyElement() 
canvas_element = CanvasGrid(schelling_draw, 50, 50, 500, 500)
happy_chart = ChartModule([{"Label": "felices", "Color": "Black"}])

model_params = {
    "height": 50,
    "width": 50,
    "density": UserSettableParameter("slider", "Densidad poblacional", 0.8, 0.1, 1.0, 0.1),
    "homophily": UserSettableParameter("slider", "Vecinos similares deseados", 4, 0, 8, 1),
    "num_agent_types": UserSettableParameter("slider", "Cantidad de tipos de agentes", 2, 1, 5, 1),
}

server = ModularServer(Schelling,
                       [canvas_element, happy_element, happy_chart],
                       "Tarea 6", model_params)