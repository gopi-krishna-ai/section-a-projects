import re

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_dropdown = """<select onchange="updateOrderStatus(${o.id}, this.value)" style="padding:4px; border-radius:4px;">
                    <option value="" disabled selected>Update</option>
                    <option value="Pending">Pending</option>
                    <option value="Shipped">Shipped</option>
                    <option value="Delivered">Delivered</option>
                </select>"""

new_dropdown = """<div style="font-size:12px; margin-bottom: 5px; color:#666;">
                    ${o.delivery_address ? `<i class="fa-solid fa-location-dot"></i> ${o.delivery_address}` : 'No Address Provided'}
                </div>
                <select onchange="updateOrderStatus(${o.id}, this.value)" style="padding:4px; border-radius:4px;">
                    <option value="" disabled selected>Update</option>
                    <option value="Pending Approval">Pending Approval</option>
                    <option value="Approved - Awaiting Location">Approved - Awaiting Location</option>
                    <option value="Location Provided">Location Provided</option>
                    <option value="Delivered">Delivered</option>
                </select>"""

content = content.replace(old_dropdown, new_dropdown)

# also update the status badge colors in admin.html
old_badge = """<span style="padding:3px 8px; border-radius:12px; background:${o.status==='Pending'?'#fef08a':(o.status==='Shipped'?'#bae6fd':'#bbf7d0')}; color:#111; font-size:12px;">${o.status}</span>"""

new_badge = """<span style="padding:3px 8px; border-radius:12px; background:${o.status.includes('Pending')?'#fef08a':(o.status.includes('Awaiting')?'#bae6fd':(o.status.includes('Location')?'#e9d5ff':'#bbf7d0'))}; color:#111; font-size:12px; font-weight:bold;">${o.status}</span>"""

content = content.replace(old_badge, new_badge)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated admin.html dropdown and badges")
