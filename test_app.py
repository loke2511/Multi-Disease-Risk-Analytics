"""Simple test - output key results line by line"""
import urllib.request, urllib.parse, http.cookiejar, json

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Register + Login
data = urllib.parse.urlencode({'username':'t3','email':'t3@t.com','password':'test1234','confirm_password':'test1234'}).encode()
opener.open('http://localhost:5000/auth/register', data)
data2 = urllib.parse.urlencode({'username':'t3','password':'test1234'}).encode()
opener.open('http://localhost:5000/auth/login', data2)
print("AUTH: OK")

# Predict diabetes
pred = json.dumps({'Pregnancies':2,'Glucose':138,'BloodPressure':72,'SkinThickness':35,'Insulin':120,'BMI':33.6,'DiabetesPedigreeFunction':0.627,'Age':50}).encode()
req = urllib.request.Request('http://localhost:5000/predict/api/diabetes', data=pred, headers={'Content-Type':'application/json'})
r = opener.open(req)
res = json.loads(r.read().decode())
for k, v in res.items():
    print(k + ": " + str(v))

# Test result page
pid = str(res['prediction_id'])
r2 = opener.open('http://localhost:5000/predict/result/' + pid)
print("result_page: " + str(r2.status))
r3 = opener.open('http://localhost:5000/predict/history')
print("history: " + str(r3.status))
r4 = opener.open('http://localhost:5000/analytics/')
print("analytics: " + str(r4.status))
print("DONE")
