import re

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the function loadOrders() and replace the entire tbody.innerHTML assignment block.
def replace_func(match):
    return """tbody.innerHTML = data.orders.map(o => `
          <tr>
              <td>#${o.id}</td>
              <td>${o.created_at}</td>
              <td>${o.user}<br><small>${o.email}</small></td>
              <td>${o.items.map(i => `${i.quantity}kg ${i.product_name}`).join('<br>')}</td>
              <td>₹${o.total_amount.toFixed(2)}</td>
              <td><span style="padding:3px 8px; border-radius:12px; background:${(o.status||'Pending') === 'Pending' ? '#fef08a' : '#bbf7d0'}; color:#111; font-size:12px; font-weight:bold;">${o.status||'Pending'}</span></td>
              <td>
                  <div style="font-size:12px; margin-bottom: 5px; color:#666;">
                      ${o.delivery_address ? `<i class="fa-solid fa-location-dot"></i> ${o.delivery_address}` : 'No Address Provided'}
                  </div>
                  ${(o.status||'Pending') === 'Pending' ? 
                  `<button onclick="updateOrderStatus(${o.id}, 'Sent')" style="background:#166534; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer; font-weight:bold;"><i class="fa-solid fa-paper-plane"></i> Send</button>` : 
                  `<span style="color:#166534; font-weight:bold;"><i class="fa-solid fa-check-circle"></i> Dispatched</span>`
                  }
              </td>
          </tr>
      `).join('');"""

# Regex to match the assignment to tbody.innerHTML inside loadOrders
content = re.sub(r'tbody\.innerHTML = data\.orders\.map\(o => `.*?`\)\.join\(\'\'\);', replace_func, content, flags=re.DOTALL)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated admin.html successfully!")
