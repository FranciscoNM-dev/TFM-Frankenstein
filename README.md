Frankenstein: Similarity-Based Football Scouting Engine
This project implements a scouting tool designed to identify statistical matches ("twins") for professional football players. It uses a data-driven approach to compare performance metrics across multiple leagues, providing objective recruitment insights based on vector proximity.

Project Overview
The engine addresses the problem of finding replacements or similar profiles for specific players by analyzing performance data. It allows for multi-player profile synthesis (creating a "Frankenstein" target) and ranks potential candidates based on their statistical proximity to that target.

Technical Implementation
Mathematical Framework
Feature Scaling: Implementation of normalization techniques to ensure fair comparisons across different leagues and positions, neutralizing the bias of raw volume and different metric scales.

Distance Metrics: Use of Euclidean Distance and Cosine Similarity to calculate the proximity between players in a multi-dimensional feature space.

Feature Engineering: Transformation of performance metrics into "Per 90 Minutes" statistics to ensure time-independent analysis.

Methodology
Data Acquisition: Processing and cleaning of large-scale football datasets from fbref and Transfermarkt.

Scoring Logic: User-defined weighting system for different performance metrics, allowing for customized scouting priorities (e.g., weighing passing accuracy over defensive actions).

Visualization: Interactive dashboard built to visualize the statistical comparison between the target profile and the top candidates.

Tech Stack
Language: Python

Libraries: Pandas, NumPy, Scikit-learn

Interface: Dash (Plotly), HTML, CSS

Academic Background
This software was developed as a Master's Thesis for the MSc in Big Data for Football Analytics and Scouting at the Real Madrid Graduate School.

Author
Francisco Alfonso Navarro Martinelli
