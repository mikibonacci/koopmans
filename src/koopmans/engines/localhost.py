import os
import sys
from typing import List

from ase.calculators.calculator import CalculationFailed

from koopmans import utils
from koopmans.calculators import (Calc, PhCalculator, ProjwfcCalculator,
                                  ReturnsBandStructure)
from koopmans.step import Step

from koopmans.pseudopotentials import read_pseudo_file

from .engine import Engine


class LocalhostEngine(Engine):
    # Engine for running a workflow locally
    def _run_steps(self, steps: tuple[Step, ...]) -> None:
        for step in steps:
            self._step_running_message(step)

            try:
                step.run()
            except CalculationFailed:
                self._step_failed_message(step)
                raise

            self._step_completed_message(step)

            # If we reached here, all future steps should be performed from scratch
            self.from_scratch = True

        return

    def load_old_calculator(self, calc: Calc):
        return load_old_calculator(calc)
    
    def get_pseudo_data(self, workflow):
        pseudo_data = {}
        for symbol,filename in workflow.pseudopotentials.items():
            pseudo_data[symbol] = read_pseudo_file(workflow.parameters.pseudo_directory / filename)

        return pseudo_data
        
def load_old_calculator(calc):
    # This is a separate function so that it can be imported by other engines
    loaded_calc = calc.__class__.fromfile(calc.directory / calc.prefix)

    if loaded_calc.is_complete():
        # If it is complete, load the results
        calc.results = loaded_calc.results

        # Check the convergence of the calculation
        calc.check_convergence()

        # Load k-points if relevant
        if hasattr(loaded_calc, 'kpts'):
            calc.kpts = loaded_calc.kpts

        if isinstance(calc, ReturnsBandStructure):
            calc.generate_band_structure()

        if isinstance(calc, ProjwfcCalculator):
            calc.generate_dos()

        if isinstance(calc, PhCalculator):
            calc.read_dynG()

    return loaded_calc
