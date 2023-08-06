"""MIDAS scenario upgrade module.

This module adds a mosaikhdf database to the scenario.

"""
import os


def upgrade(scenario, params):
    """Add a mosaikhdf database to the scenario."""
    if scenario["with_db"]:
        _add_db(scenario, params)

    return scenario


def _add_db(scenario, params):
    """Create the database in the mosaik world."""

    # Check params
    db_params = params.setdefault("mosaikdb_params", dict())
    db_params.setdefault("sim_name", "MosaikDB")
    db_params.setdefault("cmd", "python")
    db_params.setdefault("import_str", "mosaik_hdf5:MosaikHdf5")
    db_params.setdefault("step_size", scenario["step_size"])
    db_params.setdefault("filename", "midasmv.hdf5")
    db_params["filename"] = os.path.join(
        scenario["output_path"], db_params["filename"]
    )
    world = scenario["world"]

    world.sim_config[db_params["sim_name"]] = {
        db_params["cmd"]: db_params["import_str"]
    }

    scenario["mosaikdb_sim"] = world.start(
        db_params["sim_name"],
        step_size=db_params["step_size"],
        duration=scenario["end"],
    )

    database = scenario["mosaikdb_sim"].Database(
        filename=db_params["filename"]
    )
    scenario["database"] = database
