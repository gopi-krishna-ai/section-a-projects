import re

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_content = f.read()

# I need to replace the status badge and the select dropdown.
old_table_logic = """<td><span style="padding:3px 8px; border-radius:12px; background:${(o.status||'Pending').includes('Pending')?'#fef08a':((o.status||'Awaiting').includes('Awaiting')?'#bae6fd':((o.status||'Location').includes('Location')?'#e9d5ff':'#bbf7d0'))}; color:#111; font-size:12px; font-weight:bold;">${o.status||'Pending Approval'}</span></td>
            <td>
                <div style="font-size:12px; margin-bottom: 5px; color:#666;">
                    ${o.delivery_address ? `<i class="fa-solid fa-location-dot"></i> ${o.delivery_address}` : 'No Address Provided'}
                </div>
                <select onchange="updateOrderStatus(${o.id}, this.value)" style="padding:4px; border-radius:4px;">
                    <option value="" disabled selected>Update</option>
                    <option value="Pending Approval">Pending Approval</option>
                    <option value="Approved - Awaiting Location">Approved - Awaiting Location</option>
                    <option value="Location Provided">Location Provided</option>
                    <option value="Delivered">Delivered</option>
                </select>
            </td>"""

new_table_logic = """<td><span style="padding:3px 8px; border-radius:12px; background:${(o.status||'Pending') === 'Pending' ? '#fef08a' : '#bbf7d0'}; color:#111; font-size:12px; font-weight:bold;">${o.status||'Pending'}</span></td>
            <td>
                <div style="font-size:12px; margin-bottom: 5px; color:#666;">
                    ${o.delivery_address ? `<i class="fa-solid fa-location-dot"></i> ${o.delivery_address}` : 'No Address Provided'}
                </div>
                ${(o.status||'Pending') === 'Pending' ? 
                `<button onclick="updateOrderStatus(${o.id}, 'Sent')" style="background:#166534; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer; font-weight:bold;"><i class="fa-solid fa-paper-plane"></i> Send</button>` : 
                `<span style="color:#166534; font-weight:bold;"><i class="fa-solid fa-check-circle"></i> Dispatched</span>`
                }
            </td>"""

# wait, in my previous fix I used: 
# (o.status||'Pending').includes('Pending')
# Let's just regex replace the exact block if possible, or build a more flexible replacement.
admin_content = re.sub(r'<td><span style="padding:3px 8px; border-radius:12px; background:\$\{\(o\.status\|\|[^<]+</td>\s*<td>\s*<div style="font-size:12px; margin-bottom: 5px; color:#666;">\s*\$\{o\.delivery_address \? `<i class="fa-solid fa-location-dot"></i> \$\{o\.delivery_address\}` : \'No Address Provided\'\}\s*</div>\s*<select onchange="updateOrderStatus\(\$\{o\.id\}, this\.value\)" style="padding:4px; border-radius:4px;">\s*<option value="" disabled selected>Update</option>\s*<option value="Pending Approval">Pending Approval</option>\s*<option value="Approved - Awaiting Location">Approved - Awaiting Location</option>\s*<option value="Location Provided">Location Provided</option>\s*<option value="Delivered">Delivered</option>\s*</select>\s*</td>', new_table_logic, admin_content, flags=re.DOTALL)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_content)
print("Updated admin.html UI")
