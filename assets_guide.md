# 🎨 Asset Integration Guide

## 📁 Folder Structure
```
assets/
├── sprites/
│   ├── player/
│   │   ├── player_down_0.png
│   │   ├── player_down_1.png
│   │   ├── player_up_0.png
│   │   ├── player_left_0.png
│   │   └── player_right_0.png
│   ├── npcs/
│   │   ├── elder.png
│   │   ├── blacksmith.png
│   │   ├── merchant.png
│   │   └── villager.png
│   ├── items/
│   │   ├── herb.png
│   │   ├── coin.png
│   │   ├── potion.png
│   │   └── chest.png
│   └── environment/
│       ├── house_1.png
│       ├── tree_oak.png
│       ├── tree_pine.png
│       └── tileset_grass.png
├── sounds/
│   ├── pickup.wav
│   ├── talk.wav
│   └── menu_select.wav
└── music/
    └── background.ogg
```

## 🎯 Recommended Asset Specifications

### **Player Sprites**
- **Size**: 32x48 pixels
- **Format**: PNG with transparency
- **Animation**: 4 frames per direction (down, up, left, right)

### **NPC Sprites**
- **Size**: 32x48 pixels
- **Format**: PNG with transparency
- **Style**: Consistent with player

### **Item Sprites**
- **Size**: 16x16 pixels
- **Format**: PNG with transparency
- **Style**: Clear and recognizable

### **Environment Sprites**
- **Houses**: 80x100 pixels
- **Trees**: 48x64 pixels
- **Tilesets**: 32x32 per tile

## 🔗 Free Asset Sources

### **1. OpenGameArt.org**
- Search: "pixel art rpg"
- License: CC0 or CC-BY
- Good for: Complete character sets

### **2. Kenney.nl**
- All assets CC0
- Consistent art style
- Good for: UI and environment

### **3. Itch.io Free Assets**
- Search: "pixel art" + "free"
- Various licenses
- Good for: Themed asset packs

## 🛠️ How to Use

1. **Download assets** from recommended sources
2. **Place files** in correct folders following the structure above
3. **Run the game** - it will automatically use external assets if found
4. **Fallback system** - if assets not found, uses generated pixel art

## 📝 Asset Naming Convention

- **Player**: `player_{direction}_{frame}.png`
- **NPCs**: `{npc_name}.png` (lowercase)
- **Items**: `{item_name}.png`
- **Environment**: `{object_type}_{variant}.png`

The game will automatically detect and use your assets!