# PBR Layers Plugin for Krita

This plugin automatically detects and processes PBR (Physically-Based Rendering) texture layers in Krita.

If you've ever used a site like textures.com to find textures for a game/application that doesn't use PBR materials, you've probably found that your selection is severely limited. You may have attempted to use only the albedo texture in your game, only to find that it looks incredibly flat compared to the rendered screenshots showcasing that material. The purpose of this plugin is to open up the opportunity for use of PBR materials in these instances. 


## Features

- Automatically detects PBR texture layers by name (albedo, normal, roughness, height, AO, etc.)
- Splits normal maps into Red and Green channels
- Sets appropriate blending modes and opacity for each texture type
- Organizes all processed layers into a PBR_Layers group

### Albedo Texture Before Using Plugin

<img width="257" height="256" alt="image" src="https://github.com/user-attachments/assets/3629430b-644b-4c5f-8da6-6cabbd33cc11" />

### Layers Before Using Plugin

<img width="251" height="215" alt="image" src="https://github.com/user-attachments/assets/e8710848-a024-4b97-aade-205faeb64382" />

### Final Texture After Using Plugin

<img width="254" height="254" alt="image" src="https://github.com/user-attachments/assets/e103423f-4bcd-4116-9484-bfa336bcc957" />

### Layers After Using Plugin

<img width="185" height="298" alt="image" src="https://github.com/user-attachments/assets/dd90373d-430a-477c-bb19-c4093d7723a9" />



## Installation

### Any Platform (Web Install Through Krita) (Recommended)
1. Go to Tools > Scripts > Install From Web
2. Enter the URL for this git repo

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
