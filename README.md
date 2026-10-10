
# FluNet Dashboard


### Overview
Interactive dashboard for exploring global influenza surveillance data from the WHO FluNet database.
The dashboard provides a summarizing view of recent influenza activity across countries and regions, with tools for exploring historical trends and identifying countries Flu activity.

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
- FluNet API (`https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv`)

### Installation
1. **Download or clone the repository**  
2. **Create and activate a virtual environment**  
3. **Install dependencies**  
```bash
pip install -r requirements.txt
# or 
pip install --upgrade -r requirements.txt
```

### Usage
Start the dashboard locally with:
```bash
streamlit run app.py
```

### Project Structure

```text
10_flunet_dashboard/
├── .streamlit/          # Streamlit configuration and theme
├── historical_data/     # Historical data files
├── pages/               # Dashboard pages 
├── pics/                # Images and logos
├── src/                 # Data processing and reusable utilities
├── app.py               # Main app's entry point
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

### Data
Data are retrieved from the [WHO FluNet](https://www.who.int/tools/flunet) surveillance database.

### License
MIT



