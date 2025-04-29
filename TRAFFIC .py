import random
import time
import numpy as np
import matplotlib.pyplot as plt

# constants.py
TIME_STEP = 1  # seconds
MAX_SPEED = 15  # m/s
ROAD_LENGTH = 100  # meters
EMERGENCY_VEHICLE_PROBABILITY = 0.05

# vehicle.py
class Vehicle:
    def _init_(self, id, is_emergency=False):
        self.id = id
        self.speed = random.randint(5, MAX_SPEED)
        self.position = 0
        self.is_emergency = is_emergency

    def move(self):
        self.position += self.speed * TIME_STEP

    def _repr_(self):
        return f"Vehicle {self.id} (Emergency: {self.is_emergency}) at position {self.position}"

# traffic_light.py
class TrafficLight:
    def _init_(self, position):
        self.position = position
        self.state = "RED"
        self.timer = 0

    def update(self, time_step):
        self.timer += time_step
        if self.timer >= 30:
            self.state = "GREEN" if self.state == "RED" else "RED"
            self.timer = 0

    def _repr_(self):
        return f"TrafficLight at {self.position} is {self.state}"

# traffic_system.py
class TrafficSystem:
    def _init_(self):
        self.vehicles = []
        self.traffic_lights = [TrafficLight(30), TrafficLight(60), TrafficLight(90)]
        self.time_elapsed = 0
        self.history = []

    def spawn_vehicle(self):
        if random.random() < EMERGENCY_VEHICLE_PROBABILITY:
            vehicle = Vehicle(len(self.vehicles) + 1, is_emergency=True)
        else:
            vehicle = Vehicle(len(self.vehicles) + 1)
        self.vehicles.append(vehicle)

    def update_traffic_lights(self):
        for light in self.traffic_lights:
            light.update(TIME_STEP)

    def move_vehicles(self):
        for vehicle in self.vehicles:
            for light in self.traffic_lights:
                if light.state == "RED" and light.position - 10 <= vehicle.position < light.position:
                    if not vehicle.is_emergency:
                        vehicle.speed = 0
                        break
            else:
                vehicle.speed = random.randint(5, MAX_SPEED)
            vehicle.move()

    def remove_vehicles(self):
        self.vehicles = [v for v in self.vehicles if v.position < ROAD_LENGTH]

    def log_traffic_data(self):
        self.history.append({
            "time": self.time_elapsed,
            "num_vehicles": len(self.vehicles),
            "avg_speed": np.mean([v.speed for v in self.vehicles]) if self.vehicles else 0
        })

    def visualize_traffic(self):
        times = [entry["time"] for entry in self.history]
        num_vehicles = [entry["num_vehicles"] for entry in self.history]
        avg_speed = [entry["avg_speed"] for entry in self.history]

        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        plt.plot(times, num_vehicles, label="Number of Vehicles")
        plt.xlabel("Time (s)")
        plt.ylabel("Number of Vehicles")
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(times, avg_speed, label="Average Speed (m/s)", color="orange")
        plt.xlabel("Time (s)")
        plt.ylabel("Average Speed (m/s)")
        plt.legend()

        plt.tight_layout()
        plt.show()

    def run_simulation(self, duration):
        for _ in range(duration):
            self.time_elapsed += TIME_STEP
            self.spawn_vehicle()
            self.update_traffic_lights()
            self.move_vehicles()
            self.remove_vehicles()
            self.log_traffic_data()
            time.sleep(0.1)
        self.visualize_traffic()

# main.py
if _name_ == "_main_":
    print("Starting AI-Powered Smart Traffic Management System...")
    system = TrafficSystem()
    system.run_simulation(duration=300)
