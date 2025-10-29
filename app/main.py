import streamlit as st

import sys
import os
ajdsfhn;sfkls
# Add the parent directory to Python path to enable imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import modules
from app.st_theme import apply_crypto_theme
from app.pages import landing_page

from students.student_1_Agam import bitcoin_detail_page
from students.student_2_Atyant import ethereum_detail_page
from students.student_3_Vaibhav import xrp_detail_page



# Apply the beautiful crypto theme
apply_crypto_theme()

# Page configuration
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application logic - routes to different pages"""
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    # Page routing
    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "crypto_detail":
        # Route to specific crypto pages based on selected crypto
        if 'selected_crypto' in st.session_state:
            crypto_id = st.session_state.selected_crypto['id']
            if crypto_id == 'bitcoin':
                bitcoin_detail_page()
            elif crypto_id == 'ethereum':
                ethereum_detail_page()
            elif crypto_id == 'ripple':  # XRP
                xrp_detail_page()
            elif crypto_id == 'solana':
                solana_detail_page()
            else:
                st.error("Unknown cryptocurrency selected")
        else:
            st.error("No cryptocurrency selected")

if __name__ == "__main__":
    main()
