
# FluNet Dashboard
Interactive dashboard for exploring global influenza surveillance data from the WHO FluNet database.

### Dependencies
- Python 3.12 
- Streamlit 1.64.0
- Plotly 7.1.0
- FluNet API (`https://xmart-api-public.who.int/FLUMART/VIW_FNT?$format=csv`)

### Installation and Usage
```cmd
pip install -r requirements.txt  
streamlit run app.py
```

### Overview
The dashboard provides a concise view of recent influenza activity across countries and regions, with tools for exploring historical trends and identifying countries Flu activity.

### Features
- 🌍 Global influenza surveillance overview
- 🔎 Country-level trend analysis
- 📊 Identification of recent activity 
- 🧮 Baseline and trend calculations
- ⚡ Interactive Plotly visualizations
- 🔄 Data retrieved directly from the WHO FluNet API

### Data
Data are retrieved from the [WHO FluNet](https://www.who.int/tools/flunet) surveillance database.

### License
MIT



