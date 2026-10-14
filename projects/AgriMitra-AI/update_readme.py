import re

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Farmer Features
old_farmer_features = """*   **Dynamic E-Cart & Marketplace:** Whenever a crop or fertilizer is recommended, users are presented with a seamless, Amazon-style cart to purchase the exact seeds/fertilizers directly from the platform."""
new_farmer_features = """*   **Dynamic E-Cart & Marketplace:** Whenever a crop or fertilizer is recommended, users are presented with a seamless, Amazon-style cart to purchase the exact seeds/fertilizers directly from the platform.
*   **Geo-Spatial 1-Click Checkout:** When a farmer clicks their farm on the prediction map, the system caches their precise geographical coordinates and village name. During cart checkout, this location is automatically bound to the order for 1-click dispatch, eliminating manual address typing.
*   **Session-Isolated Cart:** Highly secure `localStorage` engineering ensures carts are isolated by user IDs, preventing data leakage across shared computers.
*   **Live Order Tracking:** Users have a dedicated `My Orders` page displaying 'Cash on Delivery' invoices and automated ETA notifications (e.g., *'It will reach you in 1 week'*)."""

content = content.replace(old_farmer_features, new_farmer_features)

# Update Admin Features
old_admin_features = """*   **Order & Stock Management:** Tracks live inventory. If stock hits `0`, the E-Cart automatically blocks purchases with an "Out of Stock" badge. Admins can update order statuses (Pending -> Shipped -> Delivered)."""
new_admin_features = """*   **Order & Stock Management:** Tracks live inventory. If stock hits `0`, the E-Cart automatically blocks purchases with an "Out of Stock" badge.
*   **1-Click Logistics Dispatch:** Admins receive user orders with pre-filled geolocation data pulled straight from the crop map. A single "Send" button instantly dispatches the item, updating the user's dashboard with a delivery ETA."""

content = content.replace(old_admin_features, new_admin_features)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated README.md")
