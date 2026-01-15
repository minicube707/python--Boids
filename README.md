# 🐦 Boids Simulation

This project aims to reproduce the **emergent behavior of Boids**, inspired by this video from the Youtube channel **Fouloscopie**:  
👉 https://www.youtube.com/watch?v=w-Oy4TYDnoQ

Boids are simple entities which, by following a few local rules, generate complex collective behaviors such as bird flocks or fish schools.

---

## 🎯 Project Goals

- Understand and implement the core rules of the Boids model
- Optimize simulation performance
- Study emergent behaviors
- Add more complex interactions (predators, escape, hunting)

---

## 📁 Repository Structure

This repository is divided into **two sub-projects**:

### 🐤 `Boids`
- Classic Boids model implementation
- Reproduction of the fundamental rules:
  - **Separation** (avoid collisions)
  - **Alignment** (match neighbors’ direction)
  - **Cohesion** (stay close to the group)
- Focus on code optimization and readability

### 🦅 `Boids Predateur`
- Introduction of **two types of Animoids**:
  - **Boids**: try to survive
  - **Predators**: hunt the Boids
- Goals:
  - Predators must catch Boids
  - Boids must detect and escape predators
- Exploration of prey–predator dynamics

---

## 🧠 Inspirations & Concepts

- Craig Reynolds’ Boids model
- Complex systems and emergent behaviors
- Collective intelligence
- Multi-agent simulations

---

## 📌 Notes

This project is mainly **experimental and educational**, aiming to explore how simple rules can lead to rich and realistic behaviors.

---

✨ Feel free to explore, tweak, and experiment!
