# Distance Between Two Cities

**Category:** Numbers

## Problem

Calculates the distance between two cities and allows the user to specify a unit of distance. This program may require finding coordinates for the cities like latitude and longitude.

## Solution

Ships a 36-city offline gazetteer of latitude/longitude pairs and computes great-circle distance with the haversine formula (mean Earth radius 6371.0088 km). Units: km, miles, nautical miles. Unknown cities can be resolved through OpenStreetMap Nominatim with `--geocode`.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --from "new york" --to london --unit mi
python3 main.py --demo
```

## Example

```text
New York -> London: 5,570 km / 3,461 mi
Tokyo -> Sydney: 7,826 km / 4,863 mi
Paris -> Berlin: 877 km / 545 mi
```
