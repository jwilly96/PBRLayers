from krita import Krita
from .pbr_layers_extension import PBRLayersExtension

app = Krita.instance()
extension = PBRLayersExtension(parent=app)
app.addExtension(extension)
