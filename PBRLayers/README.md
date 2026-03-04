# PBR Layers Plugin for Krita

This plugin automatically detects and processes PBR (Physically-Based Rendering) texture layers in Krita.

## Features

- Automatically detects PBR texture layers by name (albedo, normal, roughness, height, AO, etc.)
- Splits normal maps into Red and Green channels
- Sets appropriate blending modes and opacity for each texture type
- Organizes all processed layers into a PBR_Layers group

## Installation

### On Windows:

1. Copy the entire `PBRFlatten` folder to:
```
%APPDATA%\krita\pykrita\
```

Usually this expands to:
```
C:\Users\[YourUsername]\AppData\Roaming\krita\pykrita\
```

2. Restart Krita

3. Ensure both of these are present directly inside `pykrita`:
   - `PBRLayers.desktop`
   - `PBRLayers/` (folder with `__init__.py`)

4. The plugin action appears under **Tools > Scripts > PBR Layers**. You can also search for "PBR Layers" in the action menu.

### On macOS:

Copy `PBRLayers.desktop` and the `PBRLayers/` folder to:
```
~/Library/Application Support/krita/pykrita/
```

### On Linux:

Copy `PBRLayers.desktop` and the `PBRLayers/` folder to:
```
~/.local/share/krita/pykrita/
```

## Usage

1. Open an image with PBR texture layers
2. Name your layers to include PBR keywords (Most texture sites, including Textures.com, will already be properly named:
   - `albedo` or `basecolor` for diffuse/color maps
   - `normal` for normal maps
   - `roughness` for roughness maps
   - `metallic` for metallic maps
   - `height` for height maps
   - `ao` for ambient occlusion maps

3. Go to **Tools > Scripts > PBR Layers** (or search for "PBR Layers" in the action search)

4. The plugin will create a `PBR_Layers` group with all processed textures properly organized and configured

## Notes

- Original layers are hidden after processing
- Normal maps are split into Red and Green channels automatically
- Each texture type gets the appropriate blending mode (Normal, Multiply, Overlay)
- All processed layers are set to full opacity (256)
