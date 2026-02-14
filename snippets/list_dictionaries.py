# Write function that calculates average temperature for sensors of type "B" 
# that located from 12 to 60 kilometers

data = [
{"type": "A", "distance": 12, "temp": 25},
{"type": "B", "distance": 1,  "temp": 31},
{"type": "B", "distance": 24,  "temp": 16},
{"type": "D", "distance": 24,  "temp": 73},
{"type": "A", "distance": 115,  "temp": 3}
]

sum = 0
count=0
result=0

for record in data:
    print(record["type"])
    if record["type"]=="B":
        t=record["temp"]
        d=record["distance"]
        if ((12<d) and (d<60)):
           sum += t
           count+=1
if count>0:
    result = sum/count

print(result)