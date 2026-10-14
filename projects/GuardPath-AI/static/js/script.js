/* GuardPath interactive map
 * - Leaflet + OpenStreetMap gives a real street-map appearance.
 * - OSRM supplies real road geometry for the prototype route.
 * - Traffic is visualized from GuardPath's traffic_level feature (not live traffic).
 * - The trip marker moves proportionally along the road geometry.
 */

const OSRM_URL = "https://router.project-osrm.org/route/v1/driving/";
const MODE_SPEEDS = {
    walking: 5,
    bicycle: 15,
    public_transport: 25,
    car: 35,
};

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function formatMode(mode) {
    return mode.replace("_", " ").replace(/\b\w/g, c => c.toUpperCase());
}

function trafficClass(level) {
    if (level >= 7) return "high";
    if (level >= 4) return "medium";
    return "low";
}

function trafficLabel(level) {
    if (level >= 7) return "Heavy";
    if (level >= 4) return "Moderate";
    return "Low";
}

function createMap(areaCoords, areaInfo) {
    const map = L.map("route-map", { zoomControl: true }).setView([12.975, 77.69], 12.5);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    const markers = {};
    const trafficZones = {};
    const bounds = [];

    Object.entries(areaCoords).forEach(([name, [lat, lon]]) => {
        const info = areaInfo[name] || {};
        const level = Number(info.traffic_level || 0);
        const marker = L.circleMarker([lat, lon], {
            radius: 6,
            weight: 2,
            color: "#ffffff",
            fillColor: "#4f6f99",
            fillOpacity: 1,
        }).addTo(map);

        marker.bindTooltip(`<b>${escapeHtml(name)}</b><br>Traffic: ${trafficLabel(level)} (${level}/10)`, {
            direction: "top",
            opacity: 0.95,
        });

        marker.on("click", () => window.guardPathSelectNode(name));
        markers[name] = marker;
        bounds.push([lat, lon]);

        // Soft traffic/danger region around the ward. The radius is deliberately broad
        // enough to make the prototype resemble a traffic overlay rather than a point map.
        const zone = L.circle([lat, lon], {
            radius: 280 + level * 55,
            stroke: false,
            fillColor: level >= 7 ? "#e03131" : level >= 4 ? "#f08c00" : "#37b24d",
            fillOpacity: level >= 7 ? 0.16 : level >= 4 ? 0.11 : 0.06,
            interactive: false,
        }).addTo(map);
        trafficZones[name] = zone;
    });

    if (bounds.length) map.fitBounds(bounds, { padding: [20, 20] });

    return {
        map,
        markers,
        trafficZones,
        routeLayers: [],
        selectedRoute: null,
        routeLatLngs: [],
        tripMarker: null,
        animationFrame: null,
        animationStart: null,
        animationDuration: 0,
        progressDistances: [],
    };
}

function clearRouteLayers(state) {
    state.routeLayers.forEach(layer => state.map.removeLayer(layer));
    state.routeLayers = [];
    if (state.tripMarker) {
        state.map.removeLayer(state.tripMarker);
        state.tripMarker = null;
    }
    if (state.animationFrame) cancelAnimationFrame(state.animationFrame);
    state.animationFrame = null;
}

function setMarkerStyle(marker, kind) {
    if (kind === "source") {
        marker.setStyle({ radius: 9, fillColor: "#1971c2", color: "#fff", weight: 3 });
    } else if (kind === "destination") {
        marker.setStyle({ radius: 9, fillColor: "#c2255c", color: "#fff", weight: 3 });
    } else {
        marker.setStyle({ radius: 6, fillColor: "#4f6f99", color: "#fff", weight: 2 });
    }
}

function haversineKm(a, b) {
    const R = 6371;
    const lat1 = a[0] * Math.PI / 180;
    const lat2 = b[0] * Math.PI / 180;
    const dLat = (b[0] - a[0]) * Math.PI / 180;
    const dLon = (b[1] - a[1]) * Math.PI / 180;
    const x = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x));
}

function cumulativeDistances(latlngs) {
    const values = [0];
    for (let i = 1; i < latlngs.length; i++) {
        values.push(values[i - 1] + haversineKm(latlngs[i - 1], latlngs[i]));
    }
    return values;
}

function interpolateLatLng(latlngs, distances, targetKm) {
    if (!latlngs.length) return null;
    if (targetKm <= 0) return latlngs[0];
    const total = distances[distances.length - 1];
    if (targetKm >= total) return latlngs[latlngs.length - 1];

    let lo = 0, hi = distances.length - 1;
    while (lo < hi) {
        const mid = Math.floor((lo + hi) / 2);
        if (distances[mid] < targetKm) lo = mid + 1;
        else hi = mid;
    }
    const i = Math.max(1, lo);
    const d1 = distances[i - 1], d2 = distances[i];
    const t = (targetKm - d1) / Math.max(d2 - d1, 0.000001);
    return [
        latlngs[i - 1][0] + (latlngs[i][0] - latlngs[i - 1][0]) * t,
        latlngs[i - 1][1] + (latlngs[i][1] - latlngs[i - 1][1]) * t,
    ];
}

async function fetchRoadGeometry(path, areaCoords) {
    const coordinates = path.map(name => {
        const [lat, lon] = areaCoords[name];
        return `${lon},${lat}`;
    }).join(";");

    const response = await fetch(`${OSRM_URL}${coordinates}?overview=full&geometries=geojson&steps=false`);
    if (!response.ok) throw new Error("Routing service unavailable");
    const data = await response.json();
    if (!data.routes || !data.routes.length) throw new Error("No road geometry found");

    const route = data.routes[0];
    return {
        latlngs: route.geometry.coordinates.map(([lon, lat]) => [lat, lon]),
        distanceKm: route.distance / 1000,
        durationSeconds: route.duration,
    };
}

function drawTrafficSegment(state, latlngs, route, areaInfo) {
    // Draw a traffic-colored underlay for the recommended route.
    // The level is estimated from the nearest route-area in the GuardPath dataset.
    const levels = route.path.map(area => Number(areaInfo[area]?.traffic_level || 0));
    const avg = levels.reduce((a, b) => a + b, 0) / Math.max(levels.length, 1);
    const color = avg >= 7 ? "#e03131" : avg >= 4 ? "#f08c00" : "#37b24d";
    const layer = L.polyline(latlngs, { color, weight: 12, opacity: 0.28, lineCap: "round" }).addTo(state.map);
    state.routeLayers.push(layer);
}

function routeColor(route) {
    if (route.recommended) return "#1971c2";
    if (route.status === "Unsafe") return "#e03131";
    if (route.status === "Moderate") return "#f08c00";
    return "#868e96";
}

async function drawRoutes(state, routes, areaCoords, areaInfo, source, destination) {
    clearRouteLayers(state);
    Object.entries(state.markers).forEach(([name, marker]) => setMarkerStyle(marker, name === source ? "source" : name === destination ? "destination" : "normal"));

    const routeGeometries = [];
    for (const route of routes) {
        try {
            const geometry = await fetchRoadGeometry(route.path, areaCoords);
            routeGeometries.push({ route, geometry });
        } catch (e) {
            // Fall back to straight ward-to-ward lines if OSRM is unavailable.
            const latlngs = route.path.map(name => {
                const [lat, lon] = areaCoords[name];
                return [lat, lon];
            });
            routeGeometries.push({ route, geometry: { latlngs, distanceKm: route.distance_km, durationSeconds: 0 } });
        }
    }

    // Draw alternates first so the recommended route remains visible on top.
    routeGeometries.filter(x => !x.route.recommended).forEach(({ route, geometry }) => {
        const line = L.polyline(geometry.latlngs, {
            color: routeColor(route), weight: 5, opacity: 0.65, dashArray: "8 8",
        }).addTo(state.map);
        line.bindTooltip(`Route ${route.route_id}: ${route.status} · ${route.safety_score}/100`, { sticky: true });
        state.routeLayers.push(line);
    });

    const recommended = routeGeometries.find(x => x.route.recommended) || routeGeometries[0];
    if (!recommended) return;

    drawTrafficSegment(state, recommended.geometry.latlngs, recommended.route, areaInfo);

    const mainLine = L.polyline(recommended.geometry.latlngs, {
        color: routeColor(recommended.route), weight: 7, opacity: 0.96,
    }).addTo(state.map);
    mainLine.bindTooltip(`Recommended · ${recommended.route.safety_score}/100`, { sticky: true });
    state.routeLayers.push(mainLine);

    const sourceLatLng = recommended.geometry.latlngs[0];
    const destLatLng = recommended.geometry.latlngs[recommended.geometry.latlngs.length - 1];
    const sourcePin = L.marker(sourceLatLng, { title: `Start: ${source}` }).addTo(state.map);
    const destinationPin = L.marker(destLatLng, { title: `Destination: ${destination}` }).addTo(state.map);
    sourcePin.bindTooltip(`<b>START</b><br>${escapeHtml(source)}`);
    destinationPin.bindTooltip(`<b>DESTINATION</b><br>${escapeHtml(destination)}`);
    state.routeLayers.push(sourcePin, destinationPin);

    state.selectedRoute = recommended.route;
    state.routeLatLngs = recommended.geometry.latlngs;
    state.progressDistances = cumulativeDistances(state.routeLatLngs);
    state.animationDuration = Math.max(5000, getAnimationDuration(recommended.route, recommended.geometry));

    const tripProgress = document.getElementById("trip-progress");
    tripProgress.textContent = `Ready · ${recommended.route.distance_km} km · ${recommended.route.eta_text}`;
    document.getElementById("start-simulation").disabled = false;
    document.getElementById("stop-simulation").disabled = false;

    state.map.fitBounds(mainLine.getBounds(), { padding: [45, 45] });
}

function getAnimationDuration(route, geometry) {
    // The displayed ETA is realistic for the chosen mode; animation is compressed to seconds.
    const etaMinutes = Number(route.eta_minutes || 1);
    return Math.min(30000, Math.max(9000, etaMinutes * 1200));
}

// --- COMPREHENSIVE SAFE HAVEN POIS (POLICE, HOSPITAL, BUS STAND) ---
const SAFETY_POIS = [
    // Police Stations (High Security, 24/7 Rapid Response, 1.2km Safe Zone)
    { id: "pol-1", name: "Indiranagar Police Station", shortName: "Indiranagar PS", type: "police", lat: 12.9785, lng: 77.6390, desc: "24/7 Police Patrol & Rapid Response" },
    { id: "pol-2", name: "HAL Police Station", shortName: "HAL PS", type: "police", lat: 12.9575, lng: 77.6740, desc: "24/7 Highway & Traffic Police Division" },
    { id: "pol-3", name: "Marathahalli Police Station", shortName: "Marathahalli PS", type: "police", lat: 12.9550, lng: 77.6980, desc: "Outer Ring Road Safety Patrol Unit" },
    { id: "pol-4", name: "KR Puram Police Station", shortName: "KR Puram PS", type: "police", lat: 13.0030, lng: 77.6960, desc: "East Division Law & Order Hub" },
    { id: "pol-5", name: "Whitefield Police Station", shortName: "Whitefield PS", type: "police", lat: 12.9698, lng: 77.7499, desc: "Tech Corridor 24/7 Patrol Station" },
    { id: "pol-6", name: "Bellandur Police Station", shortName: "Bellandur PS", type: "police", lat: 12.9320, lng: 77.6850, desc: "Bellandur Junction Emergency Police Beat" },
    { id: "pol-7", name: "Baiyappanahalli Police Station", shortName: "Metro PS", type: "police", lat: 12.9910, lng: 77.6530, desc: "Metro & Railway Police Precinct" },
    { id: "pol-8", name: "Kadugodi Police Station", shortName: "Kadugodi PS", type: "police", lat: 12.9855, lng: 77.7470, desc: "Kadugodi Safety & Assistance Booth" },

    // Hospitals (Emergency Trauma & Critical Care, 1.0km Safe Zone)
    { id: "hosp-1", name: "Manipal Hospital (HAL Rd)", shortName: "Manipal Hosp", type: "hospital", lat: 12.9591, lng: 77.6492, desc: "24/7 Emergency Trauma & Ambulance Center" },
    { id: "hosp-2", name: "Chinmaya Hospital (CMH)", shortName: "CMH Hosp", type: "hospital", lat: 12.9780, lng: 77.6440, desc: "Multi-Speciality Emergency Hospital" },
    { id: "hosp-3", name: "Sakra World Hospital", shortName: "Sakra Hosp", type: "hospital", lat: 12.9265, lng: 77.6830, desc: "Advanced Trauma & Critical Care Unit" },
    { id: "hosp-4", name: "Manipal Hospital Whitefield", shortName: "Manipal WFD", type: "hospital", lat: 12.9860, lng: 77.7350, desc: "24/7 Emergency Response & Casualty" },
    { id: "hosp-5", name: "Brookefield Hospital", shortName: "Brookefield", type: "hospital", lat: 12.9650, lng: 77.7180, desc: "24-Hour Emergency & Critical Care" },
    { id: "hosp-6", name: "KR Puram General Hospital", shortName: "KRP Gen Hosp", type: "hospital", lat: 13.0050, lng: 77.6940, desc: "Government General & Emergency Hospital" },

    // Bus Stands / TTMC Hubs (High Footfall, Well-Lit BMTC Terminals, 750m Safe Zone)
    { id: "bus-1", name: "Domlur Bus Stand & TTMC", shortName: "Domlur TTMC", type: "bus", lat: 12.9610, lng: 77.6385, desc: "Major BMTC Hub with 24/7 Security & CCTV" },
    { id: "bus-2", name: "Marathahalli Bus Bridge", shortName: "Marathahalli Bus", type: "bus", lat: 12.9560, lng: 77.7010, desc: "High-Footfall 24/7 Transit Interchange" },
    { id: "bus-3", name: "KR Puram Railway & Bus Station", shortName: "KR Puram Bus/Stn", type: "bus", lat: 13.0005, lng: 77.6950, desc: "Intercity Transit Hub & BMTC Terminal" },
    { id: "bus-4", name: "Kadugodi Bus & Metro", shortName: "Kadugodi Bus", type: "bus", lat: 12.9870, lng: 77.7510, desc: "Whitefield Metro & Major BMTC Terminal" },
    { id: "bus-5", name: "HAL Main Bus Stop", shortName: "HAL Bus Stop", type: "bus", lat: 12.9580, lng: 77.6690, desc: "Well-Lit Transit Shelter with Constant Footfall" },
    { id: "bus-6", name: "Bellandur Central Bus Stop", shortName: "Bellandur Bus", type: "bus", lat: 12.9340, lng: 77.6870, desc: "Outer Ring Road Transit Shelter" }
];

let poiLayers = [];

function renderAllSafetyPois(state) {
    if (poiLayers.length > 0) return;
    
    SAFETY_POIS.forEach(poi => {
        let poiConfig = {
            police: { icon: "🚓", label: "Police Station" },
            hospital: { icon: "🏥", label: "Hospital" },
            bus: { icon: "🚌", label: "Bus Stand / TTMC" }
        }[poi.type];

        // High-Visibility Big Bubble Marker with Pulsing Ring & Label
        const bubbleIcon = L.divIcon({
            className: "safe-poi-bubble",
            html: `
                <div class="poi-bubble-container" title="${escapeHtml(poi.name)}">
                    <div class="poi-pulse-ring"></div>
                    <div class="poi-bubble-inner poi-bubble-${poi.type}">
                        ${poiConfig.icon}
                    </div>
                    <div class="poi-label-badge">${escapeHtml(poi.shortName || poi.name)}</div>
                </div>
            `,
            iconSize: [44, 44],
            iconAnchor: [22, 22],
            popupAnchor: [0, -24]
        });

        const bubbleMarker = L.marker([poi.lat, poi.lng], {
            icon: bubbleIcon,
            zIndexOffset: 850,
            title: poi.name
        }).addTo(state.map);

        bubbleMarker.bindTooltip(`
            <div style="font-family:Inter,sans-serif; text-align:center; padding:3px;">
                <strong style="color:var(--primary); font-size:13px;">${poiConfig.icon} ${escapeHtml(poi.name)}</strong><br>
                <span style="font-size:11px; color:#64748b;">${escapeHtml(poi.desc)}</span><br>
                <div style="margin-top:5px; color:#10b981; font-weight:700; font-size:11px;">⚡ Click to Change Destination Here</div>
            </div>
        `, { direction: "top", opacity: 0.95 });

        bubbleMarker.on("click", (e) => {
            if (e && e.originalEvent) e.originalEvent.stopPropagation();
            promptRerouteToPoi(poi);
        });

        poiLayers.push(bubbleMarker);
    });
}

function promptRerouteToPoi(poi) {
    window._pendingPoiReroute = poi;
    const modal = document.getElementById('reroute-confirm-modal');
    if (!modal) return;

    const iconBubble = document.getElementById('reroute-icon-bubble');
    const nameEl = document.getElementById('reroute-poi-name');
    const badgeEl = document.getElementById('reroute-poi-badge');

    let icon = poi.type === 'police' ? '🚓' : (poi.type === 'hospital' ? '🏥' : '🚌');
    let typeName = poi.type === 'police' ? 'Police Station' : (poi.type === 'hospital' ? 'Hospital' : 'Bus Stand');
    let bgGradient = poi.type === 'police' ? 'linear-gradient(135deg, #1e40af, #3b82f6)' : (poi.type === 'hospital' ? 'linear-gradient(135deg, #b91c1c, #ef4444)' : 'linear-gradient(135deg, #d97706, #f59e0b)');

    if (iconBubble) {
        iconBubble.innerHTML = icon;
        iconBubble.style.background = bgGradient;
        iconBubble.style.color = '#fff';
    }
    if (nameEl) nameEl.textContent = poi.name;

    // Determine distance from current vehicle or starting location
    let fromPos = null;
    let state = window.guardPathState;
    if (state && state.tripMarker) {
        let p = state.tripMarker.getLatLng();
        fromPos = [p.lat, p.lng];
    } else if (state && state.routeLatLngs && state.routeLatLngs.length > 0) {
        fromPos = state.routeLatLngs[0];
    } else {
        const srcVal = document.getElementById("source")?.value;
        if (srcVal && AREA_COORDS[srcVal]) fromPos = AREA_COORDS[srcVal];
    }

    let distText = "";
    if (fromPos && state && state.map) {
        let dKm = (state.map.distance(fromPos, [poi.lat, poi.lng]) / 1000).toFixed(1);
        distText = ` &bull; ${dKm} km away`;
    }
    if (badgeEl) badgeEl.innerHTML = `${typeName} Safe Haven${distText}`;

    modal.style.display = 'flex';
}
window.promptRerouteToPoi = promptRerouteToPoi;

function cancelReroute() {
    const modal = document.getElementById('reroute-confirm-modal');
    if (modal) modal.style.display = 'none';
    window._pendingPoiReroute = null;
}
window.cancelReroute = cancelReroute;

function findNearestArea(lat, lng, areaCoords) {
    let nearest = null;
    let minDist = Infinity;
    Object.entries(areaCoords).forEach(([name, coords]) => {
        let d = haversineKm([lat, lng], coords);
        if (d < minDist) {
            minDist = d;
            nearest = name;
        }
    });
    return nearest || Object.keys(areaCoords)[0];
}

async function confirmReroute() {
    const poi = window._pendingPoiReroute;
    if (!poi) return;
    const modal = document.getElementById('reroute-confirm-modal');
    if (modal) modal.style.display = 'none';
    window._pendingPoiReroute = null;

    const state = window.guardPathState;
    if (!state) return;

    await executeSafeHavenDetour(state, poi);
}
window.confirmReroute = confirmReroute;

async function executeSafeHavenDetour(state, poi) {
    // 1. Determine origin coordinates (where the passenger currently is)
    let originCoords = null;
    let isLiveTrip = false;

    if (state.tripMarker) {
        const p = state.tripMarker.getLatLng();
        originCoords = [p.lat, p.lng];
        isLiveTrip = true;
    } else if (state.routeLatLngs && state.routeLatLngs.length > 0) {
        originCoords = state.routeLatLngs[0];
    } else {
        const srcVal = document.getElementById("source")?.value;
        originCoords = (srcVal && AREA_COORDS[srcVal]) ? AREA_COORDS[srcVal] : Object.values(AREA_COORDS)[0];
    }

    const destCoords = [poi.lat, poi.lng];
    const nearestArea = findNearestArea(poi.lat, poi.lng, AREA_COORDS);

    // 2. Update destination dropdown
    const destSelect = document.getElementById("destination");
    if (destSelect) destSelect.value = nearestArea;

    // 3. Clear existing route layers and stop any active animation
    if (state.animationFrame) cancelAnimationFrame(state.animationFrame);
    state.animationFrame = null;
    state.isPaused = false;
    if (state.tripMarker) {
        state.map.removeLayer(state.tripMarker);
        state.tripMarker = null;
    }
    clearRouteLayers(state);

    document.getElementById("map-status").textContent = `Recalculating detour to ${poi.name}…`;
    const tripProgress = document.getElementById("trip-progress");
    if (tripProgress) tripProgress.textContent = `Diverting to ${poi.name}…`;

    // 4. Fetch real road geometry from current location to exact POI coordinates
    let latlngs = [];
    let distanceKm = 0;
    try {
        const resp = await fetch(`${OSRM_URL}${originCoords[1]},${originCoords[0]};${destCoords[1]},${destCoords[0]}?overview=full&geometries=geojson&steps=false`);
        if (resp.ok) {
            const data = await resp.json();
            if (data.routes && data.routes.length > 0) {
                latlngs = data.routes[0].geometry.coordinates.map(([lon, lat]) => [lat, lon]);
                distanceKm = (data.routes[0].distance / 1000).toFixed(1);
            }
        }
    } catch (e) {
        console.warn("OSRM direct detour fetch error:", e);
    }

    if (!latlngs.length) {
        latlngs = [originCoords, destCoords];
        distanceKm = haversineKm(originCoords, destCoords).toFixed(1);
    }

    // 5. Draw Detour Line on map in vibrant Emerald Safe Haven Green
    const detourLine = L.polyline(latlngs, {
        color: "#10b981",
        weight: 8,
        opacity: 0.96,
        lineCap: "round"
    }).addTo(state.map);
    detourLine.bindTooltip(`🚨 Detour to ${poi.name} · ${distanceKm} km`, { sticky: true });
    state.routeLayers.push(detourLine);

    // Pins for diversion point and destination
    const originPin = L.marker(latlngs[0], { title: "Diversion Point" }).addTo(state.map);
    originPin.bindTooltip(`<b>DIVERSION POINT</b><br>${isLiveTrip ? 'Vehicle Position' : 'Origin'}`);
    const safeHavenPin = L.marker(destCoords, { title: poi.name }).addTo(state.map);
    safeHavenPin.bindTooltip(`<b>SAFE HAVEN DESTINATION</b><br>${poi.name} (${poi.type.toUpperCase()})`);
    state.routeLayers.push(originPin, safeHavenPin);

    // 6. Setup new trip state
    const travelMode = document.getElementById("travel_mode")?.value || "car";
    const speed = MODE_SPEEDS[travelMode] || 35;
    const etaMin = Math.max(1, Math.round((distanceKm / speed) * 60));

    state.selectedRoute = {
        route_id: "DETOUR-" + poi.type.toUpperCase(),
        path: ["Current Position", nearestArea],
        distance_km: distanceKm,
        eta_minutes: etaMin,
        eta_text: `${etaMin} mins`,
        safety_score: 99,
        status: "Safe",
        recommended: true
    };
    state.routeLatLngs = latlngs;
    state.progressDistances = cumulativeDistances(latlngs);

    // 7. Voice / Speech guidance alert
    if ('speechSynthesis' in window) {
        try {
            window.speechSynthesis.cancel();
            let utter = new SpeechSynthesisUtterance(`Emergency detour confirmed. Navigating to ${poi.name}.`);
            utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        } catch(e) {}
    }

    // 8. Update UI controls & start navigating immediately
    document.getElementById("start-simulation").disabled = false;
    document.getElementById("stop-simulation").disabled = false;
    document.getElementById("pause-simulation").disabled = false;
    document.getElementById("pause-simulation").textContent = "⏸ Pause";
    document.getElementById("map-status").textContent = `🚨 Diverting to ${poi.name}`;

    state.map.fitBounds(detourLine.getBounds(), { padding: [45, 45] });

    // Begin navigating to the Safe Haven immediately!
    startTrip(state, travelMode);
}

function startTrip(state, travelMode) {
    if (!state.routeLatLngs.length) return;
    if (state.animationFrame) cancelAnimationFrame(state.animationFrame);
    if (state.tripMarker) state.map.removeLayer(state.tripMarker);

    // Ensure Safety POIs and Coverage Zones are plotted
    renderAllSafetyPois(state);

    const icon = L.divIcon({
        className: "moving-trip-icon",
        html: `<div class="moving-car">${travelMode === "walking" ? "●" : "➤"}</div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 17],
    });
    state.tripMarker = L.marker(state.routeLatLngs[0], { icon, zIndexOffset: 1000 }).addTo(state.map);

    // Use saved parent email for SOS without repeatedly prompting
    if (!window.parentEmail) {
        window.parentEmail = localStorage.getItem('guardpath_parent_email') || 'krishnagopi5600@gmail.com';
    }

    // Google Maps Navigation Mode: Hide panels, zoom in
    const leftPanel = document.querySelector('.left-panel');
    if(leftPanel) leftPanel.style.display = 'none';
    state.map.setZoom(17);

    const totalKm = state.progressDistances[state.progressDistances.length - 1];
    
    // Set to REAL time (eta_minutes * 60000)
    let etaMinutes = Number(state.selectedRoute.eta_minutes || 1);
    const duration = etaMinutes * 60000; 

    // Handle pausing logic
    state.isPaused = false;
    let timeSpentPaused = 0;
    let lastTickTime = performance.now();
    let accumulatedTime = 0;

    const progressEl = document.getElementById("trip-progress");
    const statusEl = document.getElementById("map-status");
    const policeStatusEl = document.getElementById("police-status");
    const hospitalStatusEl = document.getElementById("hospital-status");
    const busStatusEl = document.getElementById("bus-status");
    const poiStatusWrapper = document.getElementById("safety-poi-status");
    
    statusEl.textContent = "Google Maps Navigation Mode Active";
    if (poiStatusWrapper) poiStatusWrapper.style.display = "flex";

    function tick(now) {
        if (!state.isPaused) {
            accumulatedTime += (now - lastTickTime);
        }
        lastTickTime = now;

        const p = Math.min(1, accumulatedTime / duration);
        const position = interpolateLatLng(state.routeLatLngs, state.progressDistances, totalKm * p);
        state.tripMarker.setLatLng(position);
        
        // Navigation lock: pan map to follow marker
        if (!state.isPaused) state.map.panTo(position, {animate: true, duration: 0.1});

        progressEl.textContent = `Navigating · ${Math.round(p * 100)}% · ${Math.max(0, Math.ceil(etaMinutes * (1 - p)))} min remaining`;
        
        // Find Nearest POIs
        if (poiStatusWrapper && state.map) {
            let minPolice = Infinity, minHosp = Infinity, minBus = Infinity;
            
            SAFETY_POIS.forEach(st => {
                let d = state.map.distance(position, [st.lat, st.lng]);
                if (st.type === 'police' && d < minPolice) minPolice = d;
                if (st.type === 'hospital' && d < minHosp) minHosp = d;
                if (st.type === 'bus' && d < minBus) minBus = d;
            });

            if(policeStatusEl) policeStatusEl.textContent = `🚓 Police: ${(minPolice / 1000).toFixed(1)} km`;
            if(hospitalStatusEl) hospitalStatusEl.textContent = `🏥 Hospital: ${(minHosp / 1000).toFixed(1)} km`;
            if(busStatusEl) busStatusEl.textContent = `🚌 Bus Stop: ${(minBus / 1000).toFixed(1)} km`;
        }

        if (p < 1) {
            state.animationFrame = requestAnimationFrame(tick);
        } else {
            state.animationFrame = null;
            progressEl.textContent = `Arrived · ${state.selectedRoute.eta_text}`;
            statusEl.textContent = "Arrived safely";
            if (window.tripArrived) window.tripArrived();
        }
    }
    state.animationFrame = requestAnimationFrame(tick);
}

function stopTrip(state) {
    if (state.animationFrame) cancelAnimationFrame(state.animationFrame);
    state.animationFrame = null;
    state.isPaused = false;
    
    if (window._pauseTimeout) clearTimeout(window._pauseTimeout);

    const leftPanel = document.querySelector('.left-panel');
    if (leftPanel) leftPanel.style.display = 'block';

    const poiStatusWrapper = document.getElementById("safety-poi-status");
    if (poiStatusWrapper) poiStatusWrapper.style.display = "none";
    if (state.tripMarker) {
        state.map.removeLayer(state.tripMarker);
        state.tripMarker = null;
    }
    document.getElementById("map-status").textContent = "Trip stopped";
    document.getElementById("trip-progress").textContent = "Trip stopped";
    if (window.tripStopped) window.tripStopped();
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("route-form");
    const errorEl = document.getElementById("form-error");
    const loadingEl = document.getElementById("loading");
    const resultsPanel = document.getElementById("results-panel");
    const resultsSummary = document.getElementById("results-summary");
    const resultsList = document.getElementById("results-list");
    const travelTimeInput = document.getElementById("travel_time");
    const toggleGroup = document.getElementById("travel-time-group");
    const sourceSelect = document.getElementById("source");
    const destinationSelect = document.getElementById("destination");
    const mapHint = document.getElementById("map-hint");
    const state = createMap(AREA_COORDS, AREA_INFO);
    window.map = state.map;
    window.guardPathState = state;
    renderAllSafetyPois(state);

    window.guardPathSelectNode = function(name) {
        if (!window._picking) window._picking = { source: null, destination: null };
        let picking = window._picking;
        
        if (!picking.source || (picking.source && picking.destination)) {
            // Set new source
            picking.source = name;
            picking.destination = null;
            sourceSelect.value = name;
            destinationSelect.value = "";
            mapHint.textContent = `Source: ${name}. Click another node to set the destination.`;
        } else if (name !== picking.source) {
            // Set destination
            picking.destination = name;
            destinationSelect.value = name;
            mapHint.textContent = `${name} selected as destination. Click "Find Safest Route".`;
        }
        
        window._picking = picking;

        // Visually update markers on the map instantly
        Object.entries(state.markers).forEach(([mName, marker]) => {
            if (mName === picking.source) setMarkerStyle(marker, "source");
            else if (mName === picking.destination) setMarkerStyle(marker, "destination");
            else setMarkerStyle(marker, "normal");
        });
    };

    toggleGroup.querySelectorAll(".toggle-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            toggleGroup.querySelectorAll(".toggle-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            travelTimeInput.value = btn.dataset.value;
        });
    });

    document.getElementById("start-simulation").addEventListener("click", () => {
        document.getElementById("pause-simulation").textContent = "⏸ Pause";
        document.getElementById("pause-simulation").disabled = false;
        startTrip(state, document.getElementById("travel_mode").value);
    });

    document.getElementById("pause-simulation").addEventListener("click", (e) => {
        if(!state.animationFrame && !state.isPaused) return; // Not active
        
        state.isPaused = !state.isPaused;
        e.target.textContent = state.isPaused ? "▶ Resume" : "⏸ Pause";
        
        if (state.isPaused) {
            document.getElementById("map-status").textContent = "Trip Paused · Vehicle Stationary (30s until Safety Check)";
            window._pauseTimeout = setTimeout(() => {
                if(state.isPaused) {
                    if (window.showSafetyCheckModal) {
                        window.showSafetyCheckModal("Vehicle stationary for 30 seconds. Please confirm your safety.");
                    } else if (window.triggerSOS) {
                        window.triggerSOS();
                    }
                }
            }, 30000);
        } else {
            document.getElementById("map-status").textContent = "Google Maps Navigation Mode Active";
            if(window._pauseTimeout) clearTimeout(window._pauseTimeout);
        }
    });

    document.getElementById("stop-simulation").addEventListener("click", () => {
        stopTrip(state);
        document.getElementById("pause-simulation").disabled = true;
    });

    document.getElementById("reset-map").addEventListener("click", () => {
        stopTrip(state);
        clearRouteLayers(state);
        state.selectedRoute = null;
        state.routeLatLngs = [];
        document.getElementById("start-simulation").disabled = true;
        document.getElementById("pause-simulation").disabled = true;
        document.getElementById("stop-simulation").disabled = true;
        Object.entries(state.markers).forEach(([name, marker]) => setMarkerStyle(marker, "normal"));
        state.map.fitBounds(Object.values(AREA_COORDS).map(([lat, lon]) => [lat, lon]), { padding: [20, 20] });
        mapHint.textContent = "Map reset. Select a source and destination.";
        document.getElementById("map-status").textContent = "Ready";
    });

    form.addEventListener("submit", async e => {
        e.preventDefault();
        errorEl.textContent = "";
        const source = sourceSelect.value;
        const destination = destinationSelect.value;
        const travel_mode = document.getElementById("travel_mode").value;
        const travel_time = travelTimeInput.value;

        if (!source || !destination) {
            errorEl.textContent = "Please select both a source and a destination.";
            return;
        }
        if (source === destination) {
            errorEl.textContent = "Source and destination cannot be the same.";
            return;
        }

        resultsPanel.hidden = true;
        loadingEl.hidden = false;
        document.getElementById("map-status").textContent = "Finding road route…";

        try {
            const res = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ source, destination, travel_time, travel_mode }),
            });
            const data = await res.json();
            if (!res.ok) {
                errorEl.textContent = data.error || "Something went wrong. Please try again.";
                return;
            }

            renderResults(data);
            await drawRoutes(state, data.routes, AREA_COORDS, AREA_INFO, source, destination);
            mapHint.textContent = `Recommended route avoids the highest-risk path where the prototype data allows. Red/orange areas indicate higher traffic or risk.`;
        } catch (err) {
            console.error(err);
            errorEl.textContent = "Could not calculate the route. Check your internet connection for the street-map service.";
            document.getElementById("map-status").textContent = "Routing unavailable";
        } finally {
            loadingEl.hidden = true;
        }
    });

    function renderResults(data) {
        resultsSummary.textContent = `${data.routes.length} route(s) found from ${data.source} to ${data.destination} (${data.travel_time === "night" ? "Night" : "Day"} · ${formatMode(data.travel_mode)})`;
        resultsList.innerHTML = "";

        data.routes.forEach(route => {
            const card = document.createElement("div");
            card.className = "route-card" + (route.recommended ? " recommended" : "");
            
            card.style.cssText = `background: white; border-radius: 16px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 2px solid ${route.recommended ? 'var(--accent)' : 'transparent'}; cursor: pointer; transition: 0.2s;`;
            
            const statusColor = route.status === "Safe" ? "#10b981" : (route.status === "Moderate" ? "#f59e0b" : "#ef4444");
            const riskText = route.status === "Safe" ? "Low Risk" : (route.status === "Moderate" ? "Medium Risk" : "High Risk");

            let recTag = route.recommended ? `<div style="position:absolute; top:-12px; right: 20px; background: var(--accent); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">Recommended</div>` : '';

            card.innerHTML = `
                <div style="position: relative;">
                    ${recTag}
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                        <div>
                            <h3 style="margin: 0 0 5px 0; font-size: 18px; color: var(--primary);">Route ${route.route_id}</h3>
                            <div style="font-size: 14px; color: var(--muted); font-weight: 500;">${route.distance_km} km • ${route.eta_text}</div>
                        </div>
                    </div>
                    
                    <div style="font-size: 13px; color: var(--muted); margin-bottom: 15px; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;">
                        ${route.path.map(escapeHtml).join(' &rarr; ')}
                    </div>

                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 15px;">
                        <div style="font-size: 12px; color: var(--muted);">
                            Safety Score<br>
                            <strong style="font-size: 16px; color: var(--text);">${route.safety_score}/100</strong>
                        </div>
                        <div style="color: ${statusColor}; font-weight: bold; font-size: 14px;">
                            ${riskText}
                        </div>
                    </div>
                </div>
            `;

            if (route.status === "Unsafe") {
                const warning = document.createElement("div");
                warning.style.cssText = "background: #fee2e2; color: #991b1b; padding: 12px; border-radius: 8px; border: 1px solid #f87171; font-weight: 600; margin-bottom: 20px; font-size: 14px;";
                warning.textContent = "⚠ Higher-risk route — GuardPath recommends avoiding this path.";
                card.appendChild(warning);
            }

            const reasons = document.createElement("ul");
            reasons.className = "route-reasons";
            route.reasons.forEach(reason => {
                const li = document.createElement("li");
                li.textContent = reason;
                reasons.appendChild(li);
            });
            card.appendChild(reasons);
            resultsList.appendChild(card);
        });
        resultsPanel.hidden = false;
    }
});
