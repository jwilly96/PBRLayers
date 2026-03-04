from krita import *

pbr_layers = {}
old_layers = []

class PBRLayer:
    """Class to represent a PBR layer and its properties"""
    def __init__(self, layer, name=None, pbr_type=None, blending_mode=None, blending_opacity=256, index=0):
        self.layer = layer
        if name:
            self.name = name
        else:
            self.name = layer.name()
        self.type = layer.type()
        self.blending_mode = blending_mode
        self.blending_opacity = blending_opacity
        self.pbr_type = pbr_type
        self.index = index

    def check_if_pbr_layer(self):
        """Check if the layer name indicates a PBR texture"""
        name_lower = self.name.lower()
        pbr_keywords = ["albedo", "basecolor", "normal", "roughness", "metallic", "height", "ao"]
        return any(keyword in name_lower for keyword in pbr_keywords)


def run_pbr_flatten():
    """Main function to execute the PBR layer processing"""
    global pbr_layers, old_layers
    pbr_layers = {}
    old_layers = []
    
    doc = Krita.instance().activeDocument()
    
    if doc:
        print("Iterating through all layers in:", doc.name())
        # Get all top-level nodes and iterate through them
        for node in doc.topLevelNodes():
            iterate_layers(node)
        add_pbr_layers_to_document(doc)
    else:
        print("No active document found")


def iterate_layers(node, depth=0):
    """Recursively iterate through all layers in the node tree"""
    indent = "  " * depth
    print(f"{indent}Layer: {node.name()} - Type: {node.type()}")
    if node.type() == "paintlayer":
        check_layer_name_for_pbr_keyword(node)
    # Recursively iterate through child nodes
    for child in node.childNodes():
        iterate_layers(child, depth + 1)


def check_layer_name_for_pbr_keyword(layer):
    """Check if the layer name indicates a PBR texture"""
    layer_name = layer.name().lower()
    
    # Skip already split layers
    if layer_name.endswith("_red") or layer_name.endswith("_green"):
        return False
    
    pbr_keywords = ["albedo", "basecolor", "normal", "roughness", "metallic", "height", "ao", "translucency", "alpha"]
    for keyword in pbr_keywords:
        if keyword in layer_name:
            old_layers.append(layer)  # Keep track of original layers for potential cleanup
            print(f"Layer '{layer.name()}' is likely a PBR texture (contains '{keyword}')")
            match keyword:
                case "normal":
                    process_normal_map(layer)
                case "ao":
                    process_ao_map(layer)
                case "roughness":
                    process_roughness_map(layer)
                case "height":
                    process_height_map(layer)
                case "albedo" | "basecolor":
                    process_albedo_map(layer)
            return True


def process_normal_map(layer):
    """Process a normal map layer by splitting it into its RGB channels"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    print(f"Processing normal map layer: {layer.name()}")
    split_normal_map(layer)


def process_ao_map(layer):
    """Process an AO map layer by setting it to multiply blending mode"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    print(f"Processing AO map layer: {layer.name()}")
    layer_copy = layer.duplicate()
    pbr_layers[1] = PBRLayer(layer_copy, "PBR_AO", pbr_type="ao", blending_mode="multiply", blending_opacity=256, index=1)


def process_roughness_map(layer):
    """Process a roughness map layer by setting it to multiply blending mode"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    print(f"Processing roughness map layer: {layer.name()}")
    layer_copy = layer.duplicate()
    pbr_layers[4] = PBRLayer(layer_copy, "PBR_Roughness", pbr_type="roughness", blending_mode="multiply", blending_opacity=256, index=4)


def process_height_map(layer):
    """Process a height map layer by setting it to overlay blending mode"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    print(f"Processing height map layer: {layer.name()}")
    layer_copy = layer.duplicate()
    pbr_layers[5] = PBRLayer(layer_copy, "PBR_Height", pbr_type="height", blending_mode="overlay", blending_opacity=256, index=5)


def process_albedo_map(layer):
    """Process an albedo/base color map layer by setting it to normal blending mode"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    print(f"Processing albedo/base color map layer: {layer.name()}")
    layer_copy = layer.duplicate()
    pbr_layers[0] = PBRLayer(layer_copy, "PBR_Albedo", pbr_type="albedo", blending_mode="normal", blending_opacity=256, index=0)


def split_normal_map(layer):
    """Split a normal map into Red and Green channels"""
    if layer.type() != "paintlayer":
        print(f"Layer '{layer.name()}' is not a paint layer, skipping.")
        return
    
    doc = Krita.instance().activeDocument()
    
    # Get layer bounds
    bounds = layer.bounds()
    x, y, w, h = bounds.x(), bounds.y(), bounds.width(), bounds.height()
    
    # Get pixel data from the original layer
    pixel_data = layer.pixelData(x, y, w, h)
    
    # Create new layers for Red and Green channels
    red_layer = doc.createNode(f"{layer.name()}_Red", "paintlayer")
    green_layer = doc.createNode(f"{layer.name()}_Green", "paintlayer")
    
    # Process pixel data (BGRA format, 4 bytes per pixel)
    pixels = bytearray(pixel_data)
    
    red_pixels = bytearray(len(pixels))
    green_pixels = bytearray(len(pixels))
    
    for i in range(0, len(pixels), 4):
        # In BGRA format: [i]=Blue, [i+1]=Green, [i+2]=Red, [i+3]=Alpha
        
        # Red channel - show red component as grayscale
        red_pixels[i] = pixels[i+2]      # Blue = Red value
        red_pixels[i+1] = pixels[i+2]    # Green = Red value
        red_pixels[i+2] = pixels[i+2]    # Red = Red value
        red_pixels[i+3] = 255            # Full opacity
        
        # Green channel - show green component as grayscale
        green_pixels[i] = pixels[i+1]    # Blue = Green value
        green_pixels[i+1] = pixels[i+1]  # Green = Green value
        green_pixels[i+2] = pixels[i+1]  # Red = Green value
        green_pixels[i+3] = 255          # Full opacity
    
    # Set pixel data on new layers
    red_layer.setPixelData(bytes(red_pixels), x, y, w, h)
    green_layer.setPixelData(bytes(green_pixels), x, y, w, h)
    
    pbr_layers[2] = PBRLayer(red_layer, "PBR_Normal_R", pbr_type="normal_red", blending_mode="overlay", blending_opacity=256, index=2)
    pbr_layers[3] = PBRLayer(green_layer, "PBR_Normal_G", pbr_type="normal_green", blending_mode="overlay", blending_opacity=256, index=3)

    doc.refreshProjection()
    print(f"Split normal map into: {red_layer.name()}, {green_layer.name()}")


def add_pbr_layers_to_document(doc):
    """Add the processed PBR layers to the document and set their properties"""
    # Hide original layers after processing
    for layer in old_layers:
        layer.setVisible(False)
    
    # Create a group layer for all PBR layers
    group_layer = doc.createNode("PBR_Layers", "grouplayer")
    doc.rootNode().addChildNode(group_layer, None)
    
    # Add layers in reverse order (highest index first) so they stack correctly
    for index in sorted(pbr_layers.keys(), reverse=True):
        pbr_layer = pbr_layers[index]
        layer = pbr_layer.layer
        group_layer.addChildNode(layer, None)
        layer.setBlendingMode(pbr_layer.blending_mode)
        layer.setOpacity(pbr_layer.blending_opacity)
        layer.setName(pbr_layer.name)
        print(f"Added layer '{pbr_layer.name}' to document with blending mode '{pbr_layer.blending_mode}' and opacity {pbr_layer.blending_opacity}%")
    
    doc.refreshProjection()
