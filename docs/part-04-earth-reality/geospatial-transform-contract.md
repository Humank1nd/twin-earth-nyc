# Geospatial Transform Contract

**Document:** Part 04 — Earth Reality Layer
**Status:** v0 Draft
**Scope:** Coordinate system definitions, transform pipeline, floating origin policy, units contract
**Authority:** This contract is binding for all code that reads, writes, or transforms positional data in Twin Earth NYC.

---

## 1. Coordinate Systems

### 1.1 Cesium Source (Ingestion)

| Property | Value |
|---|---|
| Datum | WGS84 ellipsoid (GRS80-derived) |
| Horizontal CRS | EPSG:4326 — geodetic latitude/longitude in degrees |
| Vertical CRS | EGM96 geoid model — orthometric height in meters above mean sea level |
| Precision | float64 for lat/lon/height at ingestion |
| Tile Format | Cesium 3D Tiles v1.1 (glTF payloads, quantized positions) |

### 1.2 Engine Internal (Runtime)

| Property | Value |
|---|---|
| Frame | East-North-Up (ENU) local tangent plane |
| Origin | Times Square center: **40.7580 N, 73.9855 W, 10.0 m ASL** |
| Units | Meters |
| Axis Convention | **Y-up** (engine standard: X = East, Y = Up, Z = South*) |
| Precision | float32 for entity positions; float64 for origin and geo-reference anchors |

*Note: Z points South (negative North) to maintain a right-handed coordinate system with X-East and Y-Up.*

### 1.3 Omniverse / USD (Export & DCC)

| Property | Value |
|---|---|
| Units | Meters |
| Axis Convention | **Z-up** (USD/Omniverse standard: X = East, Y = North, Z = Up) |
| Transform at Import | Swap Y and Z axes; apply ENU offset from declared origin |
| Stage metersPerUnit | 1.0 |

---

## 2. Transform Pipeline

The full pipeline converts a WGS84 geodetic coordinate into every downstream representation:

```
Cesium WGS84 (lat, lon, h)
    → Step 1: ECEF (geocentric XYZ)
    → Step 2: ENU (local meters, origin at Times Square)
    → Step 3: Engine Y-up (axis swap for runtime)
    → Step 4: USD Z-up (axis swap for Omniverse export)
```

### Step 1: WGS84 Geodetic to ECEF

Convert geodetic coordinates (latitude phi, longitude lambda, ellipsoidal height h) to Earth-Centered Earth-Fixed (ECEF) Cartesian coordinates.

**WGS84 ellipsoid constants:**

```
a  = 6378137.0              (semi-major axis, meters)
f  = 1 / 298.257223563      (flattening)
b  = a * (1 - f)            (semi-minor axis)
e2 = 1 - (b^2 / a^2)       (first eccentricity squared)
```

**Prime vertical radius of curvature:**

```
N(phi) = a / sqrt(1 - e2 * sin^2(phi))
```

**Conversion (phi and lambda in radians):**

```
X_ecef = (N(phi) + h) * cos(phi) * cos(lambda)
Y_ecef = (N(phi) + h) * cos(phi) * sin(lambda)
Z_ecef = (N(phi) * (1 - e2) + h) * sin(phi)
```

### Step 2: ECEF to ENU (Local Tangent Plane)

Translate to local origin, then rotate into East-North-Up.

**Origin point (Times Square center):**

```
phi_0    = 40.7580 degrees  = 0.711341 radians
lambda_0 = -73.9855 degrees = -1.291160 radians
h_0      = 10.0 meters (ASL, approximated as ellipsoidal for vertical slice)
```

**Compute ECEF of origin** using Step 1 formulas to obtain `(X0, Y0, Z0)`.

**Delta vector:**

```
dX = X_ecef - X0
dY = Y_ecef - Y0
dZ = Z_ecef - Z0
```

**Rotation matrix R (ECEF to ENU):**

```
R = | -sin(lambda_0)              cos(lambda_0)             0           |
    | -sin(phi_0)*cos(lambda_0)  -sin(phi_0)*sin(lambda_0)  cos(phi_0)  |
    |  cos(phi_0)*cos(lambda_0)   cos(phi_0)*sin(lambda_0)  sin(phi_0)  |
```

**Apply rotation:**

```
| E |       | dX |
| N | = R * | dY |
| U |       | dZ |
```

Result: `(E, N, U)` in meters, where E = East, N = North, U = Up, relative to Times Square origin.

### Step 3: ENU to Engine Y-up

The engine uses X-East, Y-Up, Z-South (right-handed Y-up):

```
X_engine =  E
Y_engine =  U
Z_engine = -N
```

**As a matrix:**

```
| X_engine |   | 1   0   0 |   | E |
| Y_engine | = | 0   0   1 | * | N |
| Z_engine |   | 0  -1   0 |   | U |
```

### Step 4: Engine Y-up to USD Z-up

USD / Omniverse uses X-East, Y-North, Z-Up (right-handed Z-up):

```
X_usd = X_engine    =  E
Y_usd = -Z_engine   =  N
Z_usd = Y_engine    =  U
```

**As a matrix (applied to engine coordinates):**

```
| X_usd |   | 1   0   0 |   | X_engine |
| Y_usd | = | 0   0  -1 | * | Y_engine |
| Z_usd |   | 0   1   0 |   | Z_engine |
```

**Net effect (ENU to USD):** This is the identity mapping `(E, N, U) -> (X, Y, Z)`, confirming USD Z-up aligns directly with ENU when the engine Y-up intermediate step is composed.

---

## 3. Floating Origin Policy

| Rule | Specification |
|---|---|
| **Default Origin** | Times Square center `(40.7580 N, 73.9855 W, 10.0m)`. Fixed for the vertical slice. |
| **Rebase Trigger** | Camera moves > **5 km** from current origin (reserved for future expansion beyond Manhattan). |
| **Rebase Procedure** | 1. Snapshot current origin ECEF. 2. Compute new origin ECEF at camera position. 3. Subtract delta from all entity ENU positions atomically. 4. Update origin declaration. 5. Log rebase event to ledger. |
| **Entity Storage** | All entity positions stored as **ENU offsets** (float32) from the declared origin. |
| **Ledger Entry** | Every origin rebase writes: `{ timestamp, old_origin_ecef, new_origin_ecef, delta_enu, entity_count_rebased }` |
| **Coordinate Audit** | Any system reading positions must check `origin_version` counter. Stale reads are fatal errors in debug builds, warnings in release. |

**Vertical Slice Note:** For the Times Square vertical slice (< 1 km extent), no rebase will trigger. The policy exists to ensure the architecture scales to boroughs or full NYC without retrofit.

---

## 4. Units Contract

All subsystems in Twin Earth NYC must use the following units internally. Conversion to display units happens exclusively at the UI layer.

| Quantity | Internal Unit | Config / Serialization Unit | Notes |
|---|---|---|---|
| Distance | **meters** (float64 geo, float32 local) | meters | SI base |
| Angle | **radians** (float64) | degrees in config files, YAML, JSON | Convert at parse/serialize boundary |
| Mass | **kilograms** (float32) | kilograms | SI base |
| Time | **seconds** (float64) | seconds | Unix epoch for absolute timestamps |
| Temperature | **Kelvin** (float32) | Celsius in UI display | K = C + 273.15 |
| Speed | **meters/second** (float32) | displayed as km/h or mph per user pref | |
| Force | **Newtons** (float32) | Newtons | SI derived |
| Luminous intensity | **candela** (float32) | lux at surface for lighting config | |
| Frequency | **Hertz** (float32) | Hertz | Signal timing cycles |

**Enforcement:** A compile-time units wrapper (or runtime assertion layer) should tag all positional and physical values with their unit type. Bare `float` values in geo-related code paths are treated as lint errors.

---

## 5. Summary Cheat Sheet

```
Source:    WGS84 (lat 40.7580, lon -73.9855, h 10.0m)
  ↓       Step 1: Geodetic → ECEF
ECEF:     (X, Y, Z) meters from Earth center
  ↓       Step 2: ECEF → ENU (subtract origin ECEF, rotate by R)
ENU:      (East, North, Up) meters from Times Square
  ↓       Step 3: ENU → Engine (X=E, Y=U, Z=-N)
Engine:   Y-up, meters, float32
  ↓       Step 4: Engine → USD (X=X, Y=-Z, Z=Y)
USD:      Z-up, meters — ready for Omniverse
```

All transforms are invertible. Reverse the pipeline for export back to WGS84 (e.g., for map overlays or external GIS integration).

---

*End of Geospatial Transform Contract.*
