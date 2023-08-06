"""This module contains the *mosaik_api* meta definition for pysimmods
models.
"""
from pysimmods.generator.pvsystemsim import PVPlantSystem
from pysimmods.consumer.hvacsim import HVAC

META = {
    "models": {
        "Battery": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "soc_percent",
            ],
        },
        "Photovoltaic": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "t_air_deg_celsius",
                "t_module_deg_celsius",
                "bh_w_per_m2",
                "dh_w_per_m2",
                "s_module_w_per_m2",
            ],
        },
        "CHP": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "day_avg_t_air_deg_celsius",
                "p_th_mw",
            ],
        },
        "HVAC": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": [
                "set_percent",
                "p_mw",
                "q_mvar",
                "t_air_deg_celsius",
            ],
        },
        "Biogas": {
            "public": True,
            "params": ["params", "inits"],
            "attrs": ["set_percent", "p_mw", "q_mvar", "p_th_mw"],
        },
    }
}

MODELS = {"Photovoltaic": PVPlantSystem, "HVAC": HVAC}
