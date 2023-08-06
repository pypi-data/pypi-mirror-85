from abc import ABC, abstractmethod

class ControllerBase(ABC):

    @abstractmethod
    def step(self, currentState, referenceStates=None, referenceControls=None):
        """step Performs a control step taking the current state and a reference trajectory
        and returns the controls for the current time step.

        :param currentState: Current state (estimate)
        :param referenceStates: Matrix where colums are reference states
        :param referenceControls: Matrix where colums are reference controls
        :returns A 2-tuple (u, dict), where u are the resulting controls and dict a dictionary
        with metadata
        """
        pass
