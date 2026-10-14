with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

# We need to replace the img assignment block
target = '''    if (itemType === 'seed') {
        img1 = "https://images.unsplash.com/photo-1593369165383-7c152a55097b?w=150&h=150&fit=crop";
        img2 = "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=150&h=150&fit=crop";
        img3 = "https://images.unsplash.com/photo-1592978340176-580a5611cd0e?w=150&h=150&fit=crop";
        desc = "High-yield seeds";
    } else {
        img1 = "https://images.unsplash.com/photo-1627916962295-d227dbb34ba1?w=150&h=150&fit=crop";
        img2 = "https://images.unsplash.com/photo-1585675100414-22d71f11e9df?w=150&h=150&fit=crop";
        img3 = "https://images.unsplash.com/photo-1592849008985-1d01990c7da7?w=150&h=150&fit=crop";
        desc = "Organic nutrients";
    }'''

replacement = '''    if (itemType === 'seed') {
        img1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Various_seeds.jpg/320px-Various_seeds.jpg";
        img2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sunflower_seeds.jpg/320px-Sunflower_seeds.jpg";
        img3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Pumpkin_seeds_in_a_bowl.jpg/320px-Pumpkin_seeds_in_a_bowl.jpg";
        desc = "High-yield seeds";
    } else {
        img1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Fertilizer.jpg/320px-Fertilizer.jpg";
        img2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Mineral_Fertilizer.JPG/320px-Mineral_Fertilizer.JPG";
        img3 = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Compost_01.jpg/320px-Compost_01.jpg";
        desc = "Organic nutrients";
    }'''

js = js.replace(target, replacement)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated common.js with reliable images")
