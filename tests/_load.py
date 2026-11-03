"""Load a module script from the trading skill folder."""

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, ".claude", "skills", "trading")
FIX = os.path.join(ROOT, "tests", "fixtures")


def load(module, name):
    path = os.path.join(SKILL, module, name + ".py")
    spec = importlib.util.spec_from_file_location("trading_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
