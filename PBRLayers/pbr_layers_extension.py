from krita import *
from . import pbr_layers_logic

class PBRLayersExtension(Extension):
    """Krita extension that adds a PBR Layers tool"""

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        """Set up the extension and register actions"""
        pass

    def createActions(self, window):
        """Create and register the PBR Layers action"""
        # Create the action
        action = window.createAction("pbr_layers", "PBR Layers", "tools/scripts")
        action.triggered.connect(self.process_pbr_layers)

    def process_pbr_layers(self):
        """Process PBR texture layers"""
        pbr_layers_logic.run_pbr_flatten()
