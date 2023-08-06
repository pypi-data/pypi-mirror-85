"""This module contains the MIDAS powergrid upgrade."""
import logging

from mosaik.util import connect_many_to_one
from midas.scenario.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class PowergridModule(UpgradeModule):
    """The MIDAS powergrid update module."""

    def __init__(self):
        super().__init__("powergrid", LOG)
        self.default_name = "midasmv"
        self.default_sim_name = "Powergrid"
        self.default_import_str = "midas.core:PandapowerSimulator"

        self.models = {
            "Line": ["loading_percent"],
            "Trafo": ["loading_percent"],
            "Bus": ["vm_pu", "va_degree"],
            "Load": ["p_mw", "q_mvar"],
            "Sgen": ["p_mw", "q_mvar"],
        }

    def check_module_params(self):
        """Check the module params for this upgrade."""

        module_params = self.params.setdefault(f"{self.name}_params", dict())

        if not module_params:
            module_params[self.default_name] = dict()

        module_params.setdefault("sim_name", self.default_sim_name)
        module_params.setdefault("cmd", "python")
        module_params.setdefault("import_str", self.default_import_str)
        module_params.setdefault("step_size", self.scenario["step_size"])

        return module_params

    def check_sim_params(self, module_params, **kwargs):
        """Check simulator params for a certain simulator."""

        self.sim_params.setdefault("sim_name", module_params["sim_name"])
        self.sim_params.setdefault("cmd", module_params["cmd"])
        self.sim_params.setdefault("import_str", module_params["import_str"])
        self.sim_params.setdefault("step_size", module_params["step_size"])
        self.sim_params.setdefault("gridfile", self.sim_name)
        self.sim_params.setdefault("with_ts", False)

    def start_models(self):
        """Start all models for this simulator.

        Since we want the grids to be able to be interconnected with
        each other, each grid model should have its own simulator.

        Parameters
        ----------
        sim_name : str
            The sim name, not to be confused with *sim_name* for
            mosaik's *sim_config*. **This** sim_name is the simulator
            key in the configuration yaml file.

        """
        mod_key = f"{self.name}_{self.sim_name}"

        mod_name = "Grid"
        if self.sim_params["with_ts"]:
            mod_name += "TS"
        params = {"gridfile": self.sim_params["gridfile"]}

        self.start_model(mod_key, mod_name, params)

    def connect(self, *args):
        # Nothing to do so far
        # Maybe to other grids in the future?
        pass

    def connect_to_db(self):
        """Add connections to the database."""

        mdb = self.scenario["database"]
        grid = self.scenario[f"{self.name}_{self.sim_name}"]

        for entity in grid.children:
            if entity.type in self.models:
                self.connect_entities(entity, mdb, self.models[entity.type])

        self.connect_entities(grid, mdb, ["health"])
