# BirdViz

**BirdViz: Data Visualization Tool for Bird Sightings in US Ecological Centers**

## Overview

BirdViz is a comprehensive data visualization tool developed as part of the CSE 5544: Introduction to Data Visualization course by Group 10. The creators of this project are Anirudh Potlapally, Mona Gandhi, and Suchit Gupte. The primary goal of BirdViz is to develop a tool that enables users to explore and interpret bird sightings data effectively.

## Data Sources

BirdViz utilizes data from the following sources:

- **Macaulay Library**: A vast archive of wildlife media including photos, audio recordings, and videos collected from citizen scientists worldwide.
- **National Ecological Observatory Network (NEON) Breeding Birds Dataset**: This dataset provides quality-controlled records of species identification and metadata useful for modeling detectability.

## Key Features

- **Maps and Graphical Visualization**: Interactive maps and charts to visualize bird sightings across various ecological centers.
- **Identification Analysis**: Tools to help identify bird species from the data.
- **Species Distribution Visualization**: Visual representations of species distribution patterns.

## Significance

BirdViz addresses the challenge of deriving meaningful insights from vast ecological datasets in the digital age. By providing intuitive visualizations, it aids researchers, conservationists, and bird enthusiasts in understanding complex ecological data.

## How to Run the Code

To set up and run BirdViz on your local machine, follow these steps:

1. Open your command line interface (cmd/terminal).
2. Navigate to the project directory using `cd`.
3. Create a conda environment using the `env.yml` file:
   ```bash
   conda env create -f env.yml
   ```
4. Activate the environment:
    ```bash
    conda activate project
    ```
5. Run the application:
    ```bash
    python app.py
    ```
6. Once the app is running, open the index.html file located in the template folder in your browser.
7. Explore the website as it becomes available.
