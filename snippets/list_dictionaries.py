# Write function that calculates average temperature for sensors of type "B" 
# that located from 12 to 60 kilometers

from typing import TypedDict


class SensorRecord(TypedDict):
    type: str
    distance: int
    temp: int


data: list[SensorRecord] = [
{"type": "A", "distance": 12, "temp": 25},
{"type": "B", "distance": 1,  "temp": 31},
{"type": "B", "distance": 24,  "temp": 16},
{"type": "D", "distance": 24,  "temp": 73},
{"type": "A", "distance": 115,  "temp": 3}
]


def calculate_average_temperature(min_distance: int, max_distance: int) -> float:
    total = 0
    count = 0
    for record in data:
        print(record["type"])
        if record["type"] == "B":
            t = record["temp"]
            d = record["distance"]
            if min_distance < d < max_distance:
                total += t
                count += 1
    if count > 0:
        return total / count
    return 0.0


result = calculate_average_temperature(12, 60)
print(result)