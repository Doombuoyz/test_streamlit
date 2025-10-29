# Crypto Dashboard - Streamlit Application

A modern, interactive cryptocurrency dashboard built with Streamlit that allows users to track crypto prices, analyze trends, and customize the application theme.

## Features

### 🎨 Theme Customization
- Upload custom Streamlit theme files (.toml)
- Manual theme configuration with color pickers
- Pre-built theme options (Dark, Light, Neon, Crypto)
- Real-time theme application

### 📊 Crypto Dashboard
- **Landing Page**: Overview of top cryptocurrencies
- **Real-time Data**: Live prices and 24h price changes
- **Market Metrics**: Market cap, volume, and rankings
- **Interactive Selection**: Click to view detailed crypto information

### 🔍 Detailed Crypto Analysis
- **Price History**: Interactive charts with multiple timeframes (7d, 30d, 90d, 1y)
- **Key Statistics**: All-time high/low, circulating supply, max supply
- **Market Data**: Volume, market cap, and market ranking
- **Descriptions**: Detailed information about each cryptocurrency

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   poetry run streamlit run app/main.py
   ```

## Usage

### 1. Theme Configuration
- Use the sidebar to upload a custom theme file or manually adjust colors
- Sample theme files are provided in the `themes/` folder
- Apply changes and refresh to see the new theme

### 2. Crypto Exploration
- Browse the landing page to see top cryptocurrencies
- Click on any crypto card to view detailed analysis
- Use the time period selector to view different chart timeframes
- Navigate back to the landing page using the back button

## File Structure

```
AT3_Group2_Streamlit_Application/
├── app/
│   └── main.py                 # Main Streamlit application
├── themes/                     # Sample theme files
│   ├── dark_theme.toml
│   ├── light_theme.toml
│   ├── neon_theme.toml
│   ├── crypto_theme.toml
│   └── README.md
├── .streamlit/
│   └── config.toml            # Default theme configuration
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive plotting library
- **yfinance**: Financial data from Yahoo Finance

## Data Sources

- **CoinGecko API**: Real-time cryptocurrency data
- **Yahoo Finance**: Historical price data (fallback)
- **Fallback Data**: Sample data when APIs are unavailable

## Features in Detail

### Theme System
The application supports dynamic theme switching through:
- File upload functionality for `.toml` theme files
- Manual color picker interface
- Predefined theme templates
- Real-time theme preview

### Navigation System
- Session state management for page routing
- Smooth transitions between landing and detail pages
- Persistent crypto selection across page reloads

### Data Caching
- 5-minute cache for cryptocurrency list
- 10-minute cache for historical price data
- Automatic fallback data when APIs are unavailable

## Customization

### Adding New Themes
Create a new `.toml` file in the `themes/` folder with the following structure:

```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
secondaryBackgroundColor = "#YOUR_COLOR"
textColor = "#YOUR_COLOR"
font = "sans serif"  # or "serif" or "monospace"

[server]
enableCORS = false
enableXsrfProtection = false
```

### Adding New Cryptocurrencies
The application automatically fetches the top 50 cryptocurrencies from CoinGecko. To modify this:
1. Edit the `get_crypto_list()` function in `main.py`
2. Adjust the `per_page` parameter for more/fewer cryptos
3. Modify the `order` parameter to change sorting criteria

## Troubleshooting

### API Issues
If cryptocurrency data isn't loading:
- Check your internet connection
- The app will automatically use fallback sample data
- API rate limits may apply for frequent requests

### Theme Not Applying
- Ensure the theme file is valid TOML format
- Refresh the page after applying theme changes
- Check that all required theme properties are present

### Performance Issues
- The app uses caching to improve performance
- Large datasets may take longer to load
- Consider reducing the number of displayed cryptocurrencies

## License

This project is for educational purposes as part of the MDSI AMLA Assignment 3.