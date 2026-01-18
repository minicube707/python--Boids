# 🐦 Boids Simulation

## General Description

This project is a simple **Boids simulation** (collective behavior model) implemented in **Python** using **Pygame** and **NumPy**.

Each boid represents an autonomous agent moving on the screen according to local rules inspired by the collective behavior of bird flocks.  
Despite the simplicity of each rule, complex and realistic group dynamics emerge from their combination.

---

## Boids Simulation Concept

Each boid updates its velocity and orientation based on three classic Reynolds rules:

- **Separation** – avoid collisions with nearby boids  
- **Alignment** – align direction with neighboring boids  
- **Cohesion** – move toward the group when too far away  

Small random perturbations are sometimes added to avoid perfectly deterministic motion and improve visual realism.

---

## File Descriptions

### `Boids_01.py`
Defines the `Boids` class and implements a basic boids simulation.

- A global distance table between all boids is recomputed at each frame to detect neighbors  
- A small amount of randomness is added to movement  
- Boids wrap around the screen (teleport to the opposite side)  
- Each boid’s behavior is influenced by **all** other boids  

---

### `Boids_02.py`
Same as `Boids_01.py`, but randomness is applied **only when the boid is not affected by separation, alignment, or cohesion**.

---

### `Boids_03.py`
Same as `Boids_02.py`, but implements a **vector-based Reynolds model**:

- Separation, alignment, and cohesion act as continuous steering forces  
- The distance table is removed  
- Distances are recomputed for each boid at every frame  
- Each boid is influenced only by neighbors within a given perception radius  

---

### `Boids_04.py`
Same as `Boids_03.py`, but boids can no longer leave the screen.  
They smoothly turn back when reaching the borders instead of wrapping around.

---

### `Boids_05.py`
Same as `Boids_04.py`, but performance is improved by introducing a **shared distance table** that stores already computed distance vectors.

---

### `Boids_06.py`
Same as `Boids_05.py`, with additional code optimizations and cleanup.

---

### `Boids_06+.py`
Same as `Boids_06.py`, but:

- Distances between boids are stored as **scalar norms** instead of vectors  
- This improves performance at the cost of numerical precision  
- Additional boundary steering improves realism near screen edges  

---

### `Boids_06++.py`
Same as `Boids_06+.py`, but:

- Safer numerical handling using an **epsilon** to avoid division by zero  
- Reduced memory usage by storing distances as `int16`  
- Improved stability and realism near boundaries  

---

### `Boids_07.py`
Same as `Boids_06++.py`, but introduces **distinct interaction distances** for:

- Separation  
- Alignment  
- Cohesion  

This decouples short-range repulsion from mid- and long-range coordination, resulting in more realistic flocking behavior.

---

### `Boids_08.py`
Same as `Boids_07.py`, but:

- Border proximity is anticipated  
- Steering forces are accumulated before applying movement  
- Final velocity is applied only after boundary adjustments  

This results in smoother and more realistic motion.  
Borders can be toggled on/off by pressing the **B** key.

---

### `Boids_09.py`
Same as `Boids_08.py`, but each boid is influenced **only by its six closest neighbors**, improving both realism and performance.

---

### `Boids_10.py`
Same as `Boids_09.py`, but adds **type annotations** to function signatures for improved readability and maintainability.

---

## Notes

This project focuses on:
- Progressive optimization
- Behavioral realism
- Performance vs precision trade-offs
- Clear experimentation with different flocking strategies
