### SYSC 4005 COURSE PROJECT
#### **Regional Airport Passenger: Processing Simulation Study**
---

### Authors
|     Name      |     ID    |
| :-----------: | :-------: |
| Teddy Kurita  | 101267498 |
| Declan Koster | 101301649 |
---

### Project Structure
```
sysc_4005_course_project/
├── src/
|   └── sysc_4005_course_project/ (uv project directory)
|       ├── scripts/
|       |   ├── stats_analysis/
|       |   |   ├── [ code used for analysis of model output ]
|       |   |   └── ...
|       |   ├── fig_gen/
|       |   |   ├── [ code for figure generation based on model output ]
|       |   |   └── ...
|       |   ├── [ other scripts ]
|       |   └── ...
|       ├── model/
|       |   ├── [ code for the simulation model ]
|       |   └── ...
|       └── __init__.py
├── config/
|   ├── [ configuration files, so initial model state, etc. ]
|   └── ...
├── seeds/
|   ├── [ random seeds used (.txt) / seed generation ]
|   └── ...
├── data/
|   ├── [ (processed) model output ]
|   └── ...
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── final_report.pdf
```
### Setup
This project was initialized using uv ([documentation](https://docs.astral.sh/uv/)) and will be used for package and project management.