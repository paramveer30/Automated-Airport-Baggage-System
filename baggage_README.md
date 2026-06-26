# Automated Airport Baggage Management System

A Python-based airport operations management system that parses passenger and fleet data, computes per-flight statistics (oversold seats, overweight baggage, layover passengers, time delays), and renders a live graphical dashboard using the Turtle graphics library.

---

## Background

Air travel is projected to reach 4.9 billion passengers in 2024, while mishandled baggage rates have increased to 7.6 per 1000 passengers at a cost of 2.5 billion USD annually to the industry. This project was part of a broader airport automation challenge tackling three problems: Q-arm robotic baggage sorting, a 3D-printed drawbridge transfer mechanism, and a software system to track and manage passenger and fleet data.

This repo covers the software component. The system reads two input files, runs them through a pipeline of processing functions, and renders a per-flight summary using Python Turtle.

---

## Features

- Parses `passenger_data.txt` and `fleet_data.txt` into structured 2D lists
- Computes sold seat counts by gate and class (business / economy)
- Detects oversold flights per seating class
- Identifies passengers with overweight baggage and calculates excess weight
- Counts layover passengers per flight
- Flags passengers who are both late and have a layover (time delay risk)
- Renders a full graphical summary window using Python Turtle with airplane icons drawn via parametric ellipse equations

---

## Functions

| Function | Description |
|---|---|
| `passenger_data()` | Reads `passenger_data.txt` into a 2D list of passenger records |
| `fleet_data()` | Reads `fleet_data.txt` into a 2D list of plane records |
| `daily_data(passenger_list)` | Counts business and economy seat sales per gate |
| `oversold(passenger_data, fleet_data, daily_data)` | Returns two lists: oversold business and economy seats per plane |
| `overweight(passenger_list, fleet_list)` | Returns per-flight overweight counts and individual excess weight details |
| `layover(passenger_list, fleet_list)` | Returns per-flight layover passenger counts and individual layover details |
| `time_delay(fleet_list, passenger_list)` | Returns per-flight count of passengers who are both late and have a layover |
| `graphical_teamID(...)` | Renders a Turtle graphics dashboard with all flight stats and airplane icons |

### Data pipeline

```
passenger_data.txt ──► passenger_data() ──┐
                                           ├──► daily_data()
fleet_data.txt     ──► fleet_data()    ──┬┘    oversold()
                                         │      overweight()
                                         │      layover()
                                         │      time_delay()
                                         │           │
                                         └───────────▼
                                              graphical_teamID()
                                                     │
                                                     ▼
                                         Turtle graphics window
```

The outputs of `passenger_data()` and `fleet_data()` feed into every downstream function, so consistent formatting across both was critical. Functions were developed and tested individually, then integrated and debugged together to resolve any variable naming or data type mismatches.

---

## Input File Format

### `passenger_data.txt`

One passenger per line, comma-separated:

```
FirstName,LastName,Gate,SeatClass,Destination,ArrivalStatus,BaggageWeight,LayoverStatus
```

| Field | Type | Values |
|---|---|---|
| FirstName | string | e.g. `John` |
| LastName | string | e.g. `Smith` (first character used as initial) |
| Gate | string | e.g. `G1` |
| SeatClass | string | `B` (business) or `E` (economy) |
| Destination | string | e.g. `Toronto` |
| ArrivalStatus | string | `On Time` or `Late` |
| BaggageWeight | float | weight in kg |
| LayoverStatus | string | `Layover` or `No Layover` |

### `fleet_data.txt`

One plane per line, comma-separated:

```
Model,BusinessSeats,EconomySeats,TotalSeats,Gate,Destination,ArrivalStatus,MaxBaggageWeight
```

| Field | Type | Notes |
|---|---|---|
| Model | string | Aircraft model name |
| BusinessSeats | int | Capacity for business class |
| EconomySeats | int | Capacity for economy class |
| TotalSeats | int | Total seat capacity |
| Gate | string | Must match gate in passenger data |
| Destination | string | |
| ArrivalStatus | string | |
| MaxBaggageWeight | int | Per-passenger baggage limit in kg |

---

## Setup and Usage

### Requirements

- Python 3.x
- No external libraries; uses only `turtle` and `math` from the standard library

### Running

1. Place `passenger_data_v1 (1).txt` and `fleet_data.txt` in the same directory as `AutomatedBaggageCode.py`
2. Run:

```bash
python AutomatedBaggageCode.py
```

3. A Turtle graphics window (2200 x 800px, light blue background) will open displaying a per-flight summary with airplane icons

---

## Repo Structure

```
automated-airport-baggage/
├── AutomatedBaggageCode.py        # Main program: all 8 functions + graphical display
├── passenger_data_v1 (1).txt      # Sample passenger data (required at runtime)
├── fleet_data.txt                 # Sample fleet data (required at runtime)
└── README.md
```

---

## Known Limitations

- The `oversold()` function contains a reference to an undefined variable `a`, which was a known bug from the original submission that would cause a runtime error. A fix would be to initialize `a = 0` before the loop or remove the reference
- The graphical display is hardcoded for exactly 7 planes (`fleet_list[0]` through `fleet_list[6]`); running with a different fleet size will cause an index error
- Turtle rendering is slow at high speeds; `screen.tracer(0)` and `screen.update()` are used to batch draw calls but the window can still lag with large datasets

---

## Context

This project was part of a larger airport automation system that also included a Q-arm robotic system controlled by a barcode scanner that sorted luggage to a platform or rejection bin, and a 3D-printed drawbridge mechanism powered by a linear actuator to transfer luggage between platforms. This repo covers the data pipeline and graphical display portion of that system.
