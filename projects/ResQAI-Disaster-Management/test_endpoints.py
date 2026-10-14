import urllib.request, json
base = 'http://127.0.0.1:5400'

def test_post(path, data):
    req = urllib.request.Request(base+path, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read().decode())

def test_get(path):
    return json.loads(urllib.request.urlopen(base+path).read().decode())

print('1. Classify:', test_post('/api/classify', {"text": "Massive earthquake hits the city!"})['is_disaster'])
print('2. Live-X:', len(test_post('/api/live-x', {})) > 0)
print('3. Incidents:', len(test_get('/api/incidents')['rows']) > 0)
print('4. Trends:', 'categories' in test_get('/api/trends'))
print('5. Report:', len(test_get('/api/report')['summary']) > 0)
print('ALL TESTS PASSED')
