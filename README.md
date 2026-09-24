# Esteban Mercado Rachath
**Systems Engineering student · Backend systems · Graph algorithms · Data**  
Barranquilla, Colombia · UTC−5

> Systems Engineering student in my final stage at Universidad de la Costa. I design and build production-grade software with a focus on backend architecture, graph algorithms, and data-driven systems. I care deeply about performance boundaries, clean interfaces, and predictable engineering.

[LinkedIn](https://www.linkedin.com/in/estebandmr) &nbsp;·&nbsp; [GitHub](https://github.com/EstebanDMR) &nbsp;·&nbsp; [Email](mailto:esteban.mercado.r@gmail.com)

---

## ⚡ MOOD MONITOR

A small automated telemetry experiment. A Python engine turns the five most recent completed matches from **FC Barcelona** and **Junior FC de Barranquilla** into a mood score.

<!-- MOOD_START -->
<picture>
  <source media="(max-width: 600px)" srcset="assets/mood-monitor-mobile.svg" />
  <img src="assets/mood-monitor.svg" alt="Mood Monitor: 70/100, GOOD. Barcelona W W W W W; Junior L D D L W." />
</picture>
<!-- MOOD_END -->

<details>
<summary><b>Behind the Engine (How this works)</b></summary>
<br>

* **Data Pipeline:** Pulls fixture schedules via ESPN's public endpoints for LaLiga and Liga BetPlay (no API key required).
* **Algorithmic Weighting:** Extracts the 5 most recent completed matches per club and computes a normalized index ($Win = +2$, $Draw = 0$, $Loss = -2$), mapped strictly to $[0, 100]$.
* **Automated Sync:** Runs twice daily via GitHub Actions (`.github/workflows/update-mood.yml`). The script updates the SVG when the match snapshot changes; the workflow commits the changed asset. The README image reference stays between the `MOOD_START` and `MOOD_END` tags.
* **Fault Isolation:** Bypasses writes safely if the network drops or upstream payloads change.

</details>

---

## SELECTED ENGINEERING WORK

A selection of systems I've architected and implemented, emphasizing algorithmic rigor, architectural isolation, and real scalability problems.

### 01 &nbsp;·&nbsp; [RouteOptimizer](https://github.com/EstebanDMR/RouteOptimizer)
**Urban logistics pathfinding & graph optimization engine**

* **The Problem:** Last-mile urban delivery networks suffer exponential combinatorial overhead. Uninformed search algorithms evaluate too many radial branches, while off-the-shelf pathfinding libraries hide runtime memory consumption.
* **Technical Highlights:**
  * Implemented fundamental data structures **100% from scratch** in strict TypeScript: Adjacency Lists and a **Binary Min-Heap Priority Queue** guaranteeing $O(\log n)$ insertions and extractions.
  * Search engine implementing **Dijkstra** (uninformed baseline) alongside **A\*** heuristic pathfinding with admissible Euclidean and Manhattan distance functions ($f(n) = g(n) + h(n)$).
  * Built an internal **Step-by-Step Playback Recording Engine** that captures graph exploration snapshots for time-travel playback on an interactive SVG canvas.
  * Verified algorithmic parity and edge-case handling with comprehensive **Vitest** test suites.
* **Stack:** TypeScript 5.5 · React 18 · Node.js / Express · Vite · Tailwind CSS · Vitest

[Source Code ↗](https://github.com/EstebanDMR/RouteOptimizer)

---

### 02 &nbsp;·&nbsp; [SalesFlow CRM API](https://github.com/EstebanDMR/salesflow-crm-api)
**Enterprise-grade RESTful API for commercial sales pipelines**

* **The Problem:** Production CRMs require robust transaction isolation, strict validation before persistence, role segregation, and perimeter defenses against brute-force attacks.
* **Technical Highlights:**
  * Modular **Feature-First Layered Architecture** separating routing, authorization middlewares, domain controllers, and data services.
  * Fine-grained **Role-Based Access Control (RBAC)** securing multi-user pipelines, client ownership, and deals.
  * Strict schema validation via **Zod** across `params`, `query`, and `body` before reaching domain handlers.
  * Structured JSON logging via **Pino** featuring request latency metrics and graceful process shutdown.
  * Production hardening with **Helmet**, rate-limiting on authentication endpoints, and containerization via **Docker**.
* **Stack:** Node.js (v24 LTS) · Express.js 5 · PostgreSQL 16 · Prisma ORM · JWT · Docker · Swagger / OpenAPI

[Interactive Swagger Docs ↗](https://salesflow-crm-api-n44y.onrender.com/api/docs) &nbsp;·&nbsp; [Source Code ↗](https://github.com/EstebanDMR/salesflow-crm-api)

---

### 03 &nbsp;·&nbsp; [Base Electoral](https://github.com/EstebanDMR/base-electoral)
**High-volume multi-user election data management platform**

* **The Problem:** The initial version processed voter queries client-side, causing severe Main Thread freezes and high memory churn upon exceeding 1,000+ records.
* **Technical Highlights:**
  * Refactored into a decoupled **Data Access Layer (DAL)** pattern separating UI components from backend queries.
  * Re-engineered data ingestion using **server-side cursor pagination** (`limitToFirst` + `startAt`), reducing Time-to-View (TTV) and bounding client memory to a constant footprint.
  * Multi-tenant role authentication, real-time reactive sync, and high-performance Excel reporting via **ExcelJS**.
* **Stack:** React 19 · Firebase · Vite · Tailwind CSS · ExcelJS · Lucide React

[Live Platform ↗](https://base-electoral.vercel.app/) &nbsp;·&nbsp; [Source Code ↗](https://github.com/EstebanDMR/base-electoral)

---

### Secondary Spotlight &nbsp;·&nbsp; [University Analytics Dashboard](https://github.com/EstebanDMR/university-dashboard)
**Academic trend analytics & data mining engine**

* Interactive multi-year analytics platform exploring university admission, enrollment, student retention, and institutional satisfaction.
* Built during Data Mining coursework (Universidad de la Costa) to empower departmental leadership with visual data-driven insights.
* **Stack:** Python 3 · Streamlit · Pandas · Matplotlib · Seaborn · Jupyter Notebook

[Source Code ↗](https://github.com/EstebanDMR/university-dashboard)

---

## ENGINEERING FOCUS

- **Backend & systems** — Modular REST APIs, transaction boundaries, RBAC, structured logs.
- **Algorithms & graphs** — Custom min-heaps, Dijkstra, A* heuristics, runtime analysis.
- **Data systems** — Cursor pagination, analytical pipelines, PostgreSQL modeling.
- **Web platforms** — TypeScript, React interfaces, interactive SVG, Vite.

---

## TECHNICAL STACK

Technologies used across the projects above, grouped by the work they support.

<h3 align="center">Languages</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=ts,js,py&amp;theme=dark" alt="TypeScript, JavaScript and Python logos" /><br />
  <sub>TypeScript · JavaScript · Python · SQL</sub>
</p>

<h3 align="center">Frontend</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=react,tailwind,vite&amp;theme=dark" alt="React, Tailwind CSS and Vite logos" /><br />
  <sub>React · Tailwind CSS · Vite · Lucide React</sub>
</p>

<h3 align="center">Backend</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=nodejs,express,prisma&amp;theme=dark" alt="Node.js, Express and Prisma logos" /><br />
  <sub>Node.js · Express.js · Prisma ORM · REST APIs · JWT · Zod</sub>
</p>

<h3 align="center">Databases</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=postgres,firebase&amp;theme=dark" alt="PostgreSQL and Firebase logos" /><br />
  <sub>PostgreSQL 16 · Firebase Realtime Database · Firestore</sub>
</p>

<h3 align="center">Data / Analytics</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=py&amp;theme=dark" alt="Python logo" /><br />
  <sub>Pandas · NumPy · Matplotlib · Seaborn · Streamlit · Jupyter</sub>
</p>

<h3 align="center">Testing</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=vitest,jest&amp;theme=dark" alt="Vitest and Jest logos" /><br />
  <sub>Vitest · Jest · Supertest</sub>
</p>

<h3 align="center">DevOps / Tooling</h3>
<p align="center">
  <img src="https://skillicons.dev/icons?i=docker,git,githubactions,postman,vercel&amp;theme=dark" alt="Docker, Git, GitHub Actions, Postman and Vercel logos" /><br />
  <sub>Docker · Git · GitHub Actions · Postman · Vercel · Render · Swagger / OpenAPI</sub>
</p>

---

## ENGINEERING PRINCIPLES

1. **Understand the domain before writing syntax.** Code is cheap to write and expensive to maintain; clear mental models prevent premature refactors.
2. **Favor simple, decoupled boundaries.** Monolith or modular, keeping business logic isolated from data access pays dividends as systems evolve.
3. **Algorithms matter when abstractions hit hardware limits.** Standard library helpers are great until you need guaranteed $O(\log n)$ operations or bounded memory.
4. **Data should reveal operational truth.** Metrics and dashboards exist to answer concrete architectural and business questions, not just look pretty.
5. **Resilient software fails gracefully.** Catch boundary errors, log with structured context, and build systems that degrade without corrupting state.

---

## TELEMETRY & GET IN TOUCH

I am open to software engineering and backend roles, collaborative open-source projects, and technical discussions around algorithms and systems design.

* **LinkedIn:** [linkedin.com/in/estebandmr](https://www.linkedin.com/in/estebandmr)
* **GitHub:** [github.com/EstebanDMR](https://github.com/EstebanDMR)
* **Location:** Barranquilla, Colombia (UTC-5) &nbsp;·&nbsp; Remote ready

**Build → Measure → Optimize → Scale → Repeat**
