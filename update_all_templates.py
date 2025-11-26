import os
import json
import re

# Update Liquid Files
liquid_files = [f"sections/product-template-{i}.liquid" for i in range(2, 9)]

for file_path in liquid_files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} (not found)")
        continue

    with open(file_path, 'r') as f:
        content = f.read()

    # Regex to find the review div
    # <div class="review">\s*<span class="shopify-product-reviews-badge" data-id="{{ product.id }}"></span>\s*</div>
    
    pattern = r'(<div class="review">\s*<span class="shopify-product-reviews-badge" data-id="{{ product.id }}"></span>\s*</div>)'
    replacement = r'<div class="review">\n            {% render \'custom-rating-badge\', product: product %}\n            <span class="shopify-product-reviews-badge" data-id="{{ product.id }}" style="display: none !important;"></span>\n          </div>'
    
    if "custom-rating-badge" not in content:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Pattern not found in {file_path}")
    else:
        print(f"Already updated {file_path}")

# Update JSON Files
json_dir = "templates"
json_files = [f for f in os.listdir(json_dir) if f.startswith("product.") and f.endswith(".json")]

for file_name in json_files:
    file_path = os.path.join(json_dir, file_name)
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding {file_path}")
        continue

    updated = False
    
    # Add section to sections
    if "sections" in data and "custom-reviews-section" not in data["sections"]:
        data["sections"]["custom-reviews-section"] = {
            "type": "custom-reviews-section",
            "settings": {}
        }
        updated = True
        print(f"Added section to {file_name}")

    # Add section to order
    if "order" in data and "custom-reviews-section" not in data["order"]:
        order = data["order"]
        if "product-content" in order:
            idx = order.index("product-content")
            order.insert(idx + 1, "custom-reviews-section")
        elif "main" in order:
            idx = order.index("main")
            order.insert(idx + 1, "custom-reviews-section")
        else:
            order.append("custom-reviews-section")
        updated = True
        print(f"Added to order in {file_name}")

    if updated:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
