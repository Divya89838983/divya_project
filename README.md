# ClearSkies - Air Quality Monitor 🌍

**Real-time air quality monitoring for any location worldwide**

ClearSkies is a web-based air quality monitoring application that helps you check pollution levels in any city or location. Get instant access to current air quality data, EPA-standard AQI calculations, and 5-day forecasts with beautiful, interactive visualizations.

---

## 🌟 Features

- 🌍 **Global Coverage** - Search any location worldwide by city name or address
- 📊 **6 Key Pollutants** - Monitor PM2.5, PM10, Ozone (O3), NO2, SO2, and Carbon Monoxide
- 📈 **EPA AQI Standards** - Industry-standard 0-500 AQI scale with color-coded categories
- 📅 **5-Day Forecast** - Interactive charts showing air quality trends
- 🗺️ **Interactive Maps** - See your searched location on a map
- 🎨 **Color-Coded Cards** - Easy-to-understand visual indicators (Good, Moderate, Unhealthy, etc.)
- ⚡ **Fast & Responsive** - Real-time data with smooth user experience

---

## � Prerequisites

Before you begin, make sure you have:

1. **Python 3.8 or higher** installed on your computer
   - Check your version: `python3 --version`
   - Download from [python.org](https://www.python.org/downloads/) if needed

2. **OpenWeather API Key** (free)
   - Sign up at [OpenWeather](https://openweathermap.org/api)
   - Navigate to "My API Keys" section
   - Copy your API key (it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)
   - Free tier includes 1,000 API calls per day (more than enough for normal use)

---

## 🚀 Installation & Setup

### Step 1: Download the Project

**Option A - Using Git:**
```bash
git clone https://github.com/Divya89838983/divya_project.git
cd divya_project
```

**Option B - Download ZIP:**
1. Go to [https://github.com/Divya89838983/divya_project](https://github.com/Divya89838983/divya_project)
2. Click the green "Code" button → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt and navigate to the extracted folder

### Step 2: Install Dependencies

We recommend using a virtual environment to keep things organized:

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

**Alternative (without virtual environment):**
```bash
pip install -r requirements.txt
```

### Step 3: Configure Your API Key

Create a file named `keys.py` in the project root folder (same location as `main.py`):

```python
# keys.py
appid = "paste_your_actual_openweather_api_key_here"
```

**Example:**
```python
# keys.py
appid = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
```

⚠️ **Important:** 
- Replace the example key with your actual OpenWeather API key
- Keep this file private (it's automatically ignored by Git)
- Do not share your API key publicly

---

## ▶️ Running the Application

### Start the App

1. **Open your terminal** in the project folder

2. **Activate virtual environment** (if you created one):
   ```bash
   # Mac/Linux:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate
   ```

3. **Launch the application**:
   ```bash
   streamlit run main.py
   ```

4. **Access the app:**
   - Your browser should automatically open to `http://localhost:8501`
   - If not, manually open your browser and go to that address

5. **Stop the app** when done:
   - Press `Ctrl + C` in the terminal

---

## 📖 How to Use ClearSkies

### Basic Usage

#### 1. **Search for a Location**

When you first open the app, you'll see a text input box at the top.

**What to enter:**
- City name: `Paris`
- City and country: `Tokyo, Japan`
- City and state: `Ames, IA`
- Full address: `1600 Amphitheatre Parkway, Mountain View, CA`

**Tips:**
- Be specific for better results (e.g., "Portland, Oregon" vs just "Portland")
- Include country names for international locations
- The search uses OpenStreetMap's geocoding, so most place names work

#### 2. **View the Results**

After entering a location and pressing Enter, you'll see:

**A. Location Confirmation**
- ✅ Green success message with the full location name
- 🗺️ Interactive map showing your searched location

**B. Current Air Quality Status**
- **Pollutant Details Grid** - Six cards showing:
  - Pollutant name and description
  - Current AQI value
  - Raw concentration (µg/m³)
  - Color-coded category (Good, Moderate, Unhealthy, etc.)

- **Overall AQI** - Large number showing the worst pollutant's AQI
  - This determines the overall air quality
  - Color-coded badge indicating health concern level

**C. 5-Day Forecast Chart**
- Interactive line graph showing maximum AQI over time
- Colored background zones for AQI categories
- Hover over points to see exact values and timestamps
- Can zoom, pan, and download the chart

### Understanding AQI Categories

The app uses the EPA's Air Quality Index scale:

| AQI Range | Category | Color | Health Implications |
|-----------|----------|-------|---------------------|
| 0-50 | Good | Green | Air quality is satisfactory |
| 51-100 | Moderate | Yellow | Acceptable for most people |
| 101-150 | Unhealthy for Sensitive Groups | Orange | Sensitive groups may experience effects |
| 151-200 | Unhealthy | Red | Everyone may begin to experience effects |
| 201-300 | Very Unhealthy | Purple | Health alert: everyone may experience serious effects |
| 301-500 | Hazardous | Maroon | Health warnings of emergency conditions |

### Example Searches

Try these locations to see the app in action:
- `Beijing, China` - Often shows high PM2.5 levels
- `Los Angeles, CA` - Watch for Ozone levels
- `Reykjavik, Iceland` - Typically excellent air quality
- `New Delhi, India` - High pollution areas
- Your own city!

---

## ⚠️ Troubleshooting Common Issues

### Error: "Could not find coordinates for: [location]"

**Problem:** The geocoding service couldn't find your location.

**Solutions:**
- Try a more specific location (add country/state)
- Check spelling
- Use a major city name instead of small neighborhoods
- Try English name if searching international locations

### Error: "Failed to fetch air quality data"

**Problem:** Can't retrieve data from OpenWeather API.

**Solutions:**
1. **Check your API key:**
   - Verify `keys.py` exists in the project root
   - Confirm the key is correct (copy it again from OpenWeather)
   - Make sure there are no extra spaces or quotes

2. **Check internet connection:**
   - Ensure you're connected to the internet
   - Try accessing [openweathermap.org](https://openweathermap.org) in your browser

3. **API key activation:**
   - New API keys can take 10-15 minutes to activate
   - Wait a bit and try again

4. **Rate limit:**
   - Free tier allows 1,000 calls/day
   - Wait until tomorrow if you've exceeded this

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Problem:** Required packages not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

### Browser doesn't open automatically

**Solution:**
- Manually open your browser
- Go to `http://localhost:8501`
- Check the terminal for the exact URL

### Port 8501 already in use

**Problem:** Another application is using the default port.

**Solution:**
```bash
# Use a different port
streamlit run main.py --server.port 8502
```

### App is slow or not responding

**Solutions:**
- Wait a few seconds - API calls may take time
- Check your internet speed
- Restart the application
- Try a different location

---

## 🔍 Understanding the Pollutants

### PM2.5 (Fine Particulate Matter)
- Particles ≤2.5 micrometers
- From vehicle exhaust, power plants, wildfires
- Most dangerous as they penetrate deep into lungs

### PM10 (Coarse Particulate Matter)
- Particles ≤10 micrometers  
- From dust, pollen, mold
- Can irritate airways

### O3 (Ozone)
- Ground-level ozone (not the protective upper atmosphere ozone)
- Forms from vehicle emissions + sunlight
- Worse in summer and afternoon hours

### NO2 (Nitrogen Dioxide)
- From vehicle emissions and power plants
- Brown haze visible in polluted cities
- Respiratory irritant

### SO2 (Sulfur Dioxide)
- From burning fossil fuels (coal, oil)
- Forms acid rain
- Aggravates asthma

### CO (Carbon Monoxide)
- From incomplete combustion (vehicles, heaters)
- Colorless, odorless gas
- Reduces oxygen delivery to organs

---

## 📊 Technical Details

### What Data Am I Seeing?

- **Data Source:** OpenWeather Air Pollution API
- **Update Frequency:** Real-time (current conditions)
- **Forecast Period:** Up to 5 days ahead
- **Measurement Units:** µg/m³ (micrograms per cubic meter)
- **AQI Calculation:** EPA's standard formula for 0-500 scale

### Privacy & Data

- ✅ No user data is collected or stored
- ✅ No cookies or tracking
- ✅ API calls go directly to OpenWeather
- ✅ Your search locations are not saved
- ✅ Your API key stays on your computer

---

## ❌ Current Limitations

### Not Implemented Yet:
- Historical data analysis (only current + forecast available)
- Save favorite locations
- Comparison between multiple cities
- Push notifications for poor air quality
- Mobile app version
- Hourly forecast granularity (currently 3-hour intervals from API)

### Known Issues:
- Small cities may not always be found by geocoding
- API provides 3-hour forecast intervals, not hourly
- Rare geocoding errors for ambiguous location names
- No offline mode (requires internet connection)

**Note:** These limitations don't affect core functionality. For technical details and workarounds, see the [Developer Guide](docs/DEVELOPER_GUIDE.md).

---

## 🆘 Need More Help?

### For Users:
- Check [OpenWeather Status](https://status.openweathermap.org/) if API seems down
- Re-read the [How to Use](#-how-to-use-clearskies) section
- Try example searches listed above
- Check [Troubleshooting](#-troubleshooting-common-issues)

### For Developers:
- See [Developer Guide](docs/DEVELOPER_GUIDE.md) for technical documentation
- Check inline code comments for implementation details
- Review test files in `tests/` directory
- Project structure and API details in developer docs

---

## 📁 Project Information

- **Python Version:** 3.8+
- **Framework:** Streamlit
- **License:** MIT
- **Repository:** [github.com/Divya89838983/divya_project](https://github.com/Divya89838983/divya_project)

### Dependencies:
- streamlit - Web interface
- requests - API calls
- pandas - Data handling
- plotly - Interactive charts

See `requirements.txt` for complete list with versions.

---

## 📸 Screenshots

**Note:** Screenshots should be added here showing:
1. Location search input
2. Location confirmation with map
3. Current air quality pollutant cards
4. Overall AQI display
5. Interactive forecast chart
6. Different AQI categories (Good, Moderate, Unhealthy examples)

*To add screenshots: Take screenshots while using the app and add them to this README. In GitHub's web editor, simply drag and drop image files into the markdown.*

---

## 💡 Tips for Best Experience

1. **Search specific locations** - "Seattle, WA" works better than just "Seattle"
2. **Wait for loading spinners** - API calls take 1-3 seconds
3. **Check multiple times of day** - Pollution levels vary (especially Ozone)
4. **Compare locations** - Run multiple searches in different browser tabs
5. **Zoom on charts** - Interactive Plotly charts allow detailed inspection

---

## 🎓 Educational Use

This project was created as a college assignment to demonstrate:
- API integration and data fetching
- Data processing and calculations (AQI formulas)
- Interactive web UI development
- Python project structure and documentation
- Real-world application development

Feel free to learn from the code and adapt it for your own projects!

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

This means you can freely use, modify, and distribute this project.

---

**Made with ❤️ using Python and Streamlit**

*Last Updated: December 2025*