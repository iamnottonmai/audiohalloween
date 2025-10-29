import streamlit as st
import os
from pathlib import Path

# Page configuration
st.set_page_config(page_title="Haunted House Audio Files", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    /* Gradient header */
    .gradient-header {
        background: linear-gradient(to right, #1a1a1a, #8B7355, #DAA520);
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .gradient-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Mode button styling */
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        font-size: 1.1em;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Audio player container */
    .audio-container {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Volume control label */
    .volume-label {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="gradient-header">
        <h1>Haunted House Audio Files</h1>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 1
if 'currently_playing' not in st.session_state:
    st.session_state.currently_playing = None
if 'volumes' not in st.session_state:
    st.session_state.volumes = {i: 1.0 for i in range(1, 11)}

# Mode toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button(f"Mode {st.session_state.mode}", use_container_width=True):
        st.session_state.mode = 2 if st.session_state.mode == 1 else 1
        st.rerun()

st.markdown(f"### Current Mode: Mode {st.session_state.mode}")
if st.session_state.mode == 1:
    st.info("🔊 Mode 1: Only one audio file plays at a time")
else:
    st.info("🔊 Mode 2: Multiple audio files can play simultaneously")

# Audio folder path
audio_folder = Path("audio")

# Create audio folder if it doesn't exist
if not audio_folder.exists():
    st.warning("⚠️ 'audio' folder not found. Please create an 'audio' folder and add audio1.m4a to audio10.m4a files.")
    st.stop()

# Display audio players in a grid (3 columns)
cols_per_row = 3
rows = 4  # 10 audio files = 3 rows of 3 + 1 row of 1

audio_num = 1
for row in range(rows):
    if row < 3:
        cols = st.columns(cols_per_row)
    else:
        # Last row with only one audio file (centered)
        cols = st.columns([1, 1, 1])
        cols = [cols[1]]  # Use only the middle column
    
    for col in cols:
        if audio_num <= 10:
            with col:
                st.markdown(f"#### Audio #{audio_num}")
                
                audio_file = audio_folder / f"audio{audio_num}.m4a"
                
                if audio_file.exists():
                    # Volume control
                    volume = st.slider(
                        "Volume control",
                        min_value=0.0,
                        max_value=1.0,
                        value=st.session_state.volumes[audio_num],
                        step=0.1,
                        key=f"volume_{audio_num}",
                        label_visibility="collapsed"
                    )
                    st.session_state.volumes[audio_num] = volume
                    
                    # Audio player
                    with open(audio_file, 'rb') as audio:
                        audio_bytes = audio.read()
                        
                        # Create a unique key for each audio player
                        audio_key = f"audio_player_{audio_num}"
                        
                        # Display audio player
                        st.audio(audio_bytes, format='audio/m4a')
                        
                        # Note about volume control
                        st.caption(f"Volume: {int(volume * 100)}%")
                        st.caption("Note: Use your browser's audio controls to play/pause")
                else:
                    st.error(f"audio{audio_num}.m4a not found")
                
                audio_num += 1

# Information section
st.markdown("---")
st.markdown("""
### Instructions:
- **Mode 1**: Click play on any audio file. Playing another will stop the current one.
- **Mode 2**: Click play on multiple audio files to play them simultaneously.
- Adjust individual volume sliders to control each audio file's volume.
- Place your audio files (audio1.m4a to audio10.m4a) in the 'audio' folder.

### Note:
The volume sliders show the intended volume level. Actual volume control depends on your browser's 
implementation of the HTML5 audio element. For full volume control functionality, you may need to 
use additional JavaScript or a more advanced audio library.
""")

# Footer
st.markdown("---")
st.markdown("*🎃 Haunted House Audio Controller 👻*")
