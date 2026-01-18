# 🐦 Boids Simulation with Predators

## Overview

This project is a **Boids simulation** (collective behavior model) implemented in **Python** using **Pygame** and **NumPy**.

Each *animoid* represents an autonomous agent moving on the screen according to simple local rules inspired by the collective behavior of bird flocks.  
Although each rule is simple, their combination produces **complex and realistic group dynamics**.

There are two types of animoids:

- **Boids** – follow the classic rules (Separation, Alignment, Cohesion) and have an additional **flee** behavior when a predator is nearby.  
- **Predators** – follow a single **hunt** behavior to chase nearby boids.

---

## Controls

- **Toggle borders on/off:** Press **B**  
- **Exit simulation:** Press **ESC** or close the window

---

## Boids Behavior

Each boid updates its velocity and orientation based on the following rules:

1. **Separation** – avoid collisions with nearby boids  
2. **Alignment** – match direction with neighboring boids  
3. **Cohesion** – move toward the center of the local group  
4. **Flee** – move away from nearby predators  

Random perturbations are added occasionally to avoid perfectly deterministic motion, enhancing visual realism.

---

## Predator Behavior

Each predator follows a simple hunting rule:

- **Hunt** – move toward nearby boids to simulate predation  

Predators also maintain **separation from each other** for more realistic movement.

---

## Project Evolution

The project has evolved through multiple versions, each improving realism and performance:

| Version | Description |
|---------|-------------|
| `Boids_Predateur_1.py` | Initial implementation using code from `Boids_07.py`. |
| `Boids_Predateur_2.py` | Optimized and cleaner version of `Predateur_1`. |
| `Boids_Predateur_3.py` | Added: <br>- Separate distances for Separation, Alignment, Cohesion <br>- Common distance array transformed into norms <br>- Border avoidance vector for realism <br>- Rule of 6 nearest neighbors <br>- Flee condition (boids move faster when escaping predators) |
| `Boids_Predateur_4.py` | Same as version 3, with added **predator separation** for realism. |
| `Boids_Predateur_5.py` | Attempted Numba optimization (not successful). |
| `Boids_Predateur_6.py` | Attempted multiprocessing (not successful). |
| `Boids_Predateur_6_test.py` | Same as version 6, multiprocessing deactivated. |

---

## 📌 Notes

This project is mainly **experimental and educational**, aiming to explore how simple rules can lead to rich and realistic behaviors.

---

✨ Feel free to explore, tweak, and experiment!