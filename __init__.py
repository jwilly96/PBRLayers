from krita import *
from .pbr_layers_extension import PBRLayersExtension

# Register the extension
instance = Krita.instance()
dock_widget = instance.addExtension(PBRLayersExtension(instance))
