import json
import os

# List of files to process
files_to_process = [
    "templates/product.variant-image-square.json",
    "templates/product.list-stacked.json",
    "templates/product.gift.json",
    "templates/product.variant-dropdown.json",
    "templates/product.thumb-left.json",
    "templates/product.thumb-right.json",
    "templates/product.collage-s1.json",
    "templates/product.des-tabcenter.json",
    "templates/product.without-thumb.json",
    "templates/product.product-bundle.json",
    "templates/product.collage-s2.json",
    "templates/product.tab-accordion.json",
    "templates/product.list-grid.json",
    "templates/product.variant-image.json"
]

def remove_background_video(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        sections = data.get('sections', {})
        order = data.get('order', [])
        
        sections_to_remove = []
        
        # Find sections with type "backgroundvideo"
        for section_id, section_data in sections.items():
            if section_data.get('type') == 'backgroundvideo':
                sections_to_remove.append(section_id)
        
        if not sections_to_remove:
            print(f"No backgroundvideo section found in {file_path}")
            return

        # Remove sections and update order
        for section_id in sections_to_remove:
            del sections[section_id]
            if section_id in order:
                order.remove(section_id)
            print(f"Removed section {section_id} from {file_path}")
            
        # Save changes
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all files
for file_path in files_to_process:
    if os.path.exists(file_path):
        remove_background_video(file_path)
    else:
        print(f"File not found: {file_path}")
