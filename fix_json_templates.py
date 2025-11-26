import os
import json

# List of files containing the invalid block
files_to_fix = [
    "templates/product.collage-s1.json",
    "templates/product.collage-s2.json",
    "templates/product.des-tabcenter.json",
    "templates/product.gift.json",
    "templates/product.list-grid.json",
    "templates/product.list-stacked.json",
    "templates/product.product-bundle.json",
    "templates/product.tab-accordion.json",
    "templates/product.thumb-left.json",
    "templates/product.thumb-right.json",
    "templates/product.variant-dropdown.json",
    "templates/product.variant-image.json",
    "templates/product.variant-image-square.json",
    "templates/product.without-thumb.json"
]

for file_path in files_to_fix:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (not found)")
        continue

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        modified = False
        
        # Check if product-content section exists
        if "sections" in data and "product-content" in data["sections"]:
            section = data["sections"]["product-content"]
            
            # Find blocks to remove
            blocks_to_remove = []
            if "blocks" in section:
                for block_id, block_data in section["blocks"].items():
                    if block_data.get("type") == "review":
                        blocks_to_remove.append(block_id)
            
            # Remove blocks
            for block_id in blocks_to_remove:
                del section["blocks"][block_id]
                modified = True
                print(f"Removed block {block_id} from {file_path}")
                
                # Remove from block_order
                if "block_order" in section and block_id in section["block_order"]:
                    section["block_order"].remove(block_id)
                    print(f"Removed {block_id} from block_order in {file_path}")

        if modified:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {file_path}")
        else:
            print(f"No changes needed for {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
