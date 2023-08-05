from abc import ABC, abstractmethod
from blip_flowanalysis.core import Flow


class Analyser(ABC):
    """Implements different structural analysis on chatbot flow data.
    
    This abstract base class defines that any subclass must implement its own `analyse` method.
    Additional methods can also be implemented, but the core operations of the analysis are to be
    performed by this method.
    
    """
    
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def analyse(self, flow: Flow):
        raise NotImplementedError()
