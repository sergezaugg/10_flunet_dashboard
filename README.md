# Global Influenza Explorer 

### Features
- Global influenza surveillance overview
- Baseline and trend calculations
- Geo overview with maps
- Identification of recent activity 
- Country-level trend analysis

### Dependencies
- Python 3.12 
- Streamlit 1.64.0
- Plotly 7.1.0

### Dependencies Data Source
- FluNet API (`https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv`)

### Installation
1. Clone the repository  
2. Create and activate a Python venv
3. Install dependencies with ```pip install -r requirements.txt```

### Set a maintenance code (facultative)
1. Create a file ```.streamlit/secrets.toml``` with one key: ```refreshcode```
2. The value is a string with you code.
3. This is needed to access the data refresh button in running app

### Usage (Easy with VS Code)
1. Open this repo with "Open Folder..."
2. Activate virtual environment (CTRL-SHIFT-P, "Python Select Interpreter") 
3. Open a terminal and type: ```streamlit run app.py```

### Usage (With CMD terminal under windows)
1. Open cmd and navigate to root dir of this repo
3. Activate venv with ```[full-path-to-venv-dir]\Scripts\activate.bat```
4. type: ```streamlit run app.py```

### Project Structure
```text
10_flunet_dashboard/
├── .streamlit/          # Streamlit configuration and theme
├── historical_data/     # Historical data files
├── pages/               # Pages for the frontend 
├── pics/                # Images and logos
├── src/                 # Data processing and reusable utilities
├── app.py               # Main app's entry point
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

### Credits
- Data provided by the [WHO FluNet](https://www.who.int/tools/flunet) 
- Web-app concept, analytics and implementation by Serge Zaugg ([Pollito-ML](https://github.com/sergezaugg))

### License
MIT



