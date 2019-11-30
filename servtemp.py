from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from temp import Schelling


class HappyElement(TextElement): # Comenzamos con la parte visual del modelo

    def __init__(self):
        pass

    def render(self, model):
        return "felices: " + str(model.felices) # Debajo del grid observamos la cuenta total de agentes felices

def schelling_draw(agent): # En esta sección, establecemos cómo se representará a cada agente en el grid
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h":1, "Filled": "true", "Layer": 0}

#for i in agent.type:
#    portrayal["Color"] = color[i]
    
    if agent.type == 0:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal

happy_element = HappyElement()
canvas_element = CanvasGrid(schelling_draw, 50, 50, 500, 500)
happy_chart = ChartModule([{"Label": "felices", "Color": "Black"}])

model_params = {
    "height": 50,
    "width": 50,
    "density": UserSettableParameter("slider", "Densidad poblacional", 0.5, 0.1, 1.0, 0.1),
    "minority_pc": UserSettableParameter("slider", "Fracción minoritaria", 0.5, 0.00, 1.0, 0.1),
    "homophily": UserSettableParameter("slider", "Vecinos similares deseados", 4, 0, 8, 1),
}

server = ModularServer(Schelling,
                       [canvas_element, happy_element, happy_chart],
                       "Tarea 6", model_params)