with open('templates/recommendation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix for crop
target_crop = '''html += `<button onclick="window.location.href='/soil'" style="width:100%; padding:10px; background:#166534; color:white; border:none; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">Next: Soil Analysis <i class="fa-solid fa-arrow-right"></i></button>`;'''

replace_crop = '''
                          let basePrice = 200 + (d.crop.length * 10) + (Math.random() * 50);
                          let dp = Math.round(Math.round(basePrice) * 0.85);
                          html += `
                          <div style="margin-top: 15px; background: white; padding: 10px; border-radius: 8px; border: 1px solid #22c55e;">
                              <h5 style="margin-top:0; color:#166534; font-size:14px;"><i class="fa-solid fa-store"></i> Premium ${d.crop} Seeds</h5>
                              <div style="display:flex; gap:10px;">
                                  <img src="https://images.unsplash.com/photo-1593369165383-7c152a55097b?w=100&h=100&fit=crop" style="width:70px; height:70px; border-radius:6px; object-fit:cover;">
                                  <div>
                                      <div style="font-size:12px; color:#4b5563; margin-bottom:5px;">High-yield seeds tailored for this area.</div>
                                      <div style="font-size:14px; font-weight:bold; color:#15803d;"><span style="text-decoration:line-through; color:#ef4444; font-size:11px;">₹${Math.round(basePrice)}</span> ₹${dp}</div>
                                      <button onclick="showToast('Added to cart!', 'success')" style="margin-top:5px; background:#166534; color:white; border:none; border-radius:4px; padding:4px 8px; font-size:11px; cursor:pointer;">Purchase (Save 15%)</button>
                                  </div>
                              </div>
                          </div>`;
                          
                          html += `<button onclick="window.location.href='/soil'" style="width:100%; padding:10px; background:#166534; color:white; border:none; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">Next: Soil Analysis <i class="fa-solid fa-arrow-right"></i></button>`;
'''

if target_crop in html:
    html = html.replace(target_crop, replace_crop)

# Fix for fertilizer
target_fert = '''html += `<button onclick="window.location.href='/dashboard'" style="width:100%; padding:10px; background:#166534; color:white; border:none; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">Finish <i class="fa-solid fa-check"></i></button>`;'''

replace_fert = '''
                          let fertName = d.fertilizer;
                          let basePrice = 300 + (fertName.length * 15) + (Math.random() * 50);
                          let dp = Math.round(Math.round(basePrice) * 0.85);
                          html += `
                          <div style="margin-top: 15px; background: white; padding: 10px; border-radius: 8px; border: 1px solid #22c55e;">
                              <h5 style="margin-top:0; color:#166534; font-size:14px;"><i class="fa-solid fa-store"></i> Organic ${fertName}</h5>
                              <div style="display:flex; gap:10px;">
                                  <img src="https://images.unsplash.com/photo-1627916962295-d227dbb34ba1?w=100&h=100&fit=crop" style="width:70px; height:70px; border-radius:6px; object-fit:cover;">
                                  <div>
                                      <div style="font-size:12px; color:#4b5563; margin-bottom:5px;">High-grade nutrients for max yield.</div>
                                      <div style="font-size:14px; font-weight:bold; color:#15803d;"><span style="text-decoration:line-through; color:#ef4444; font-size:11px;">₹${Math.round(basePrice)}</span> ₹${dp}</div>
                                      <button onclick="showToast('Added to cart!', 'success')" style="margin-top:5px; background:#166534; color:white; border:none; border-radius:4px; padding:4px 8px; font-size:11px; cursor:pointer;">Purchase (Save 15%)</button>
                                  </div>
                              </div>
                          </div>`;
                          
                          html += `<button onclick="window.location.href='/dashboard'" style="width:100%; padding:10px; background:#166534; color:white; border:none; border-radius:8px; margin-top:10px; cursor:pointer; font-weight:bold;">Finish <i class="fa-solid fa-check"></i></button>`;
'''

if target_fert in html:
    html = html.replace(target_fert, replace_fert)

with open('templates/recommendation.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated recommendation.html")
