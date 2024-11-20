import plistlib
from PIL import Image
import os
import sys
from consolemenu import *
from consolemenu.items import *



def main():
   menu()


def menu():
    # Create the main menu
    main_menu = ConsoleMenu("MMC Texture Toolbox by Blob", "Choose an option")

    # Create a submenu
    ExportTexture = ConsoleMenu("Export Texture", "Export the Texture to a MMC compatible Spritesheet\nSelect a type of Spritesheet")

    menuTexutreQuality = ConsoleMenu("Texture Quality", "Select a menuTexture quality")

    partsTexutreQuality = ConsoleMenu("Texture Quality", "Select a partsTexture quality")

    # Add a function item to the submenu

    menuTextureExportHigh = FunctionItem("HDR (High)", ToSpritesheet, args=["menuTextureHDR"])
    menuTextureExportMed = FunctionItem("HD (Medium)", ToSpritesheet, args=["menuTextureHD"])
    menuTextureExportLow = FunctionItem("SD (LOW)", ToSpritesheet, args=["menuTextureSD"])
    menuTexutreQualityOption = SubmenuItem("menuTexture", menuTexutreQuality, ExportTexture)

    partsTextureExportHigh = FunctionItem("HDR (High)", ToSpritesheet, args=["partsTextureHDR"])
    partsTextureExportMed = FunctionItem("HD (Medium)", ToSpritesheet, args=["partsTextureHD"])
    partsTextureExportLow = FunctionItem("SD (LOW)", ToSpritesheet, args=["partsTextureSD"])
    partsTexutreQualityOption = SubmenuItem("partsTexture", partsTexutreQuality, ExportTexture)
    
    ExportTexture.append_item(menuTexutreQualityOption)
    ExportTexture.append_item(partsTexutreQualityOption)
    menuTexutreQuality.append_item(menuTextureExportLow)
    menuTexutreQuality.append_item(menuTextureExportMed)
    menuTexutreQuality.append_item(menuTextureExportHigh)
    partsTexutreQuality.append_item(partsTextureExportLow)
    partsTexutreQuality.append_item(partsTextureExportMed)
    partsTexutreQuality.append_item(partsTextureExportHigh)

    # Add a SubmenuItem to the main menu
    ExportTextureOption = SubmenuItem("Export Textures", ExportTexture, main_menu)
    ImportTextureOption = FunctionItem("Import Textures [NOT READY!]", print, [""])
    main_menu.append_item(ExportTextureOption)
    main_menu.append_item(ImportTextureOption)

    # Show the main menu
    main_menu.show()


def ToSpritesheet(Texturefile):
    # menuTexture
    if Texturefile == "menuTextureSD":
        plist_path = "plists/SD/menuTexture.plist"
        input_dir = "Textures/menuTexture"
        atlas_output_path = "Exported/SD/menuTexture.png"
    elif Texturefile == "menuTextureHD":
        plist_path = "plists/HD/menuTexture.plist"
        input_dir = "Textures/menuTexture"
        atlas_output_path = "Exported/HD/menuTexture.png"
    elif Texturefile == "menuTextureHDR":
        plist_path = "plists/HDR/menuTexture.plist"
        input_dir = "Textures/menuTexture"
        atlas_output_path = "Exported/HDR/menuTexture.png"

    # partsTexture
    elif Texturefile == "partsTextureSD":
        plist_path = "plists/SD/partsTexture.plist"
        input_dir = "Textures/partsTexture"
        atlas_output_path = "Exported/SD/partsTexture.png"
    elif Texturefile == "partsTextureHD":
        plist_path = "plists/HD/partsTexture.plist"
        input_dir = "Textures/partsTexture"
        atlas_output_path = "Exported/HD/partsTexture.png"
    elif Texturefile == "partsTextureHDR":
        plist_path = "plists/HDR/partsTexture.plist"
        input_dir = "Textures/partsTexture"
        atlas_output_path = "Exported/HDR/partsTexture.png"


    # Load the plist file
    with open(plist_path, "rb") as file:
        plist_data = plistlib.load(file)

    # Get the metadata for the texture atlas
    metadata = plist_data['metadata']
    texture_size = metadata['size']
    atlas_width, atlas_height = map(int, texture_size.strip("{}").split(","))

    # Create a blank canvas for the texture atlas
    # Since the pixel format is RGBA8888, we create a canvas with RGBA mode
    atlas_image = Image.new("RGBA", (atlas_width, atlas_height))

    # Place each sprite into the atlas
    for frame_name, frame_data in plist_data["frames"].items():
        sprite_path = os.path.join(input_dir, frame_name)
        if not os.path.exists(sprite_path):
            print(f"Sprite not found: {sprite_path}")
            continue

        # Open the sprite image
        sprite_image = Image.open(sprite_path)

        # Parse textureRect
        rect = frame_data["textureRect"]
        rect = rect.strip("{}").split("},{")
        xy = tuple(map(int, rect[0].strip("{}").split(",")))
        wh = tuple(map(int, rect[1].strip("{}").split(",")))

        # Check for size mismatch and resize if needed
        if sprite_image.size != wh:
            sprite_image = sprite_image.resize(wh, Image.Resampling.LANCZOS)

        # Paste the sprite into the atlas at the specified position
        atlas_image.paste(sprite_image, xy)

    # Save the resulting texture atlas
    atlas_image.save(atlas_output_path)

    print(f"Texture atlas saved at {atlas_output_path}.")

main()