import mesa
import json
import sys
from aml_simulator.mesa.sim_properties import SimProperties 
from aml_simulator.mesa.model_parameters import ModelParameters
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AMLSimModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, property_file : str):
        super().__init__()
        self.property_file = property_file
        self.load_properties()
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)

    def step(self):
        """Advance the model by one step."""

        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
        self.schedule.step()

    def load_properties(self): 
        if self.property_file is None:
            raise ValueError("Property file must be provided")
        
        self.properties = SimProperties(self.property_file)
        logging.info("Properties are loaded successfully")

        self.reset_randomizer(self.properties.seed)
        logging.info("Randomizer set to seed {}".format(self.properties.seed))
        

        

if __name__ == "__main__":
    argv = sys.argv
    conf_file = argv[1]
    print(conf_file)

    if len(argv) > 2 : 
        model_parameter_file = argv[2]
        logging.info(f"Model parameter file: {model_parameter_file}")
        ModelParameters.load_properties(model_parameter_file)
        logging.info("Model parameters are loaded successfully")

    model = AMLSimModel(conf_file)
