import re

with open('templates/orders.html', 'r', encoding='utf-8') as f:
    orders_content = f.read()

old_js = """            let actionHTML = '';
            if (o.status === 'Approved - Awaiting Location') {
                actionHTML = `
                    <div style="margin-top: 15px; padding: 15px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;">
                        <p style="font-weight: bold; margin-bottom: 10px; color: #166534;">Admin Approved! Please provide delivery location:</p>
                        <input type="text" id="loc_${o.id}" placeholder="Enter your full address" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 10px;">
                        <button onclick="submitLocation(${o.id})" style="background: #166534; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; cursor: pointer;">Submit Location</button>
                    </div>
                `;
            } else if (o.delivery_address) {
                actionHTML = `
                    <div style="margin-top: 10px; padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 13px;">
                        <strong>Delivery Address:</strong> ${o.delivery_address}
                    </div>
                `;
            }"""

new_js = """            let actionHTML = `
                <div style="margin-top: 10px; padding: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 13px; color: #333;">
                    <strong>Delivery Address:</strong> ${o.delivery_address || 'Not Provided'}<br>
                    <strong>Payment Method:</strong> Cash on Delivery
                </div>
            `;
            if (o.status === 'Sent') {
                actionHTML += `
                    <div style="margin-top: 10px; padding: 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; font-size: 14px; color: #166534; font-weight: bold;">
                        <i class="fa-solid fa-truck-fast"></i> It will reach you in 1 week to your location.
                    </div>
                `;
            }"""

orders_content = orders_content.replace(old_js, new_js)

# Also update status colors
color_logic_old = """            let statusColor = '#fef08a'; // yellow
            if (o.status === 'Approved - Awaiting Location') statusColor = '#bfdbfe'; // blue
            if (o.status === 'Location Provided') statusColor = '#e9d5ff'; // purple
            if (o.status === 'Shipped') statusColor = '#fed7aa'; // orange
            if (o.status === 'Delivered') statusColor = '#bbf7d0'; // green"""

color_logic_new = """            let statusColor = '#fef08a'; // yellow
            if (o.status === 'Sent') statusColor = '#bbf7d0'; // green"""

orders_content = orders_content.replace(color_logic_old, color_logic_new)

with open('templates/orders.html', 'w', encoding='utf-8') as f:
    f.write(orders_content)
print("Updated orders.html logic")
