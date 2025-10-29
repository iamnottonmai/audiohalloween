import streamlit as st
import os
from pathlib import Path

# Page config for mobile
st.set_page_config(
    page_title="Haunted House Audio",
    page_icon="🎃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .stApp {
        max-width: 390px;
        margin: 0 auto;
    }
    
    /* Header with gradient */
    .header-container {
        background: linear-gradient(90deg, #1a1a1a 0%, #b8860b 50%, #daa520 100%);
        padding: 30px 20px;
        text-align: center;
        margin: -70px -100px 20px -100px;
        border-radius: 0 0 15px 15px;
    }
    
    .header-title {
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Mode toggle button */
    .mode-container {
        text-align: center;
        margin: 20px 0;
    }
    
    div[data-testid="stButton"] button {
        background-color: #2c2c2c;
        color: white;
        border: 2px solid #b8860b;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 16px;
        font-weight: bold;
        width: 150px;
        transition: all 0.3s;
    }
    
    div[data-testid="stButton"] button:hover {
        background-color: #b8860b;
        border-color: #daa520;
    }
    
    /* Audio player grid */
    .audio-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        padding: 10px;
    }
    
    .audio-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Volume control label */
    .volume-label {
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        font-size: 10px;
        color: #666;
        margin-right: 5px;
        white-space: nowrap;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        max-width: 100px;
        height: 100px;
        border-radius: 15px;
        background: linear-gradient(135deg, #4a4a4a 0%, #2c2c2c 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Slider styling */
    .stSlider {
        margin-top: 5px;
    }
    
    div[data-baseweb="slider"] {
        margin: 0;
    }
    
    /* Hide default Streamlit slider label */
    .stSlider > label {
        display: none;
    }
    
    /* Audio label */
    .audio-label {
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
    }
    
    /* Responsive adjustments */
    @media (max-width: 390px) {
        .audio-grid {
            gap: 10px;
            padding: 5px;
        }
        
        audio {
            max-width: 90px;
            height: 90px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 1
if 'volumes' not in st.session_state:
    st.session_state.volumes = {i: 100 for i in range(1, 11)}
if 'currently_playing' not in st.session_state:
    st.session_state.currently_playing = None

# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">Haunted House Audio Files</h1>
</div>
""", unsafe_allow_html=True)

# Mode toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button(f"Mode {st.session_state.mode}", key="mode_toggle"):
        st.session_state.mode = 2 if st.session_state.mode == 1 else 1
        st.rerun()

st.markdown(f"<p style='text-align: center; color: #666; margin-top: -10px;'>Current: Mode {st.session_state.mode}</p>", unsafe_allow_html=True)

# Create audio folder path
audio_folder = Path("audio")

# Audio grid
st.markdown('<div class="audio-grid">', unsafe_allow_html=True)

# Create 3 columns for grid layout
for row in range(4):
    cols = st.columns(3)
    
    for col_idx, col in enumerate(cols):
        audio_num = row * 3 + col_idx + 1
        
        if audio_num <= 10:
            with col:
                st.markdown(f'<div class="audio-label">Audio #{audio_num}</div>', unsafe_allow_html=True)
                
                # Audio file path
                audio_path = audio_folder / f"audio{audio_num}.m4a"
                
                if audio_path.exists():
                    # Create container for volume control and audio
                    inner_cols = st.columns([1, 4])
                    
                    with inner_cols[0]:
                        st.markdown('<div class="volume-label">Volume control</div>', unsafe_allow_html=True)
                    
                    with inner_cols[1]:
                        # Audio player
                        if st.session_state.mode == 1:
                            # Mode 1: Only one audio plays at a time
                            audio_html = f'''
                            <audio id="audio{audio_num}" controls 
                                   onplay="stopOtherAudios({audio_num})"
                                   style="width: 100%; max-width: 100px;">
                                <source src="audio/audio{audio_num}.m4a" type="audio/mp4">
                            </audio>
                            '''
                        else:
                            # Mode 2: Multiple audios can play simultaneously
                            audio_html = f'''
                            <audio id="audio{audio_num}" controls style="width: 100%; max-width: 100px;">
                                <source src="audio/audio{audio_num}.m4a" type="audio/mp4">
                            </audio>
                            '''
                        
                        st.markdown(audio_html, unsafe_allow_html=True)
                    
                    # Volume control slider
                    volume = st.slider(
                        "",
                        min_value=0,
                        max_value=100,
                        value=st.session_state.volumes[audio_num],
                        key=f"volume_{audio_num}",
                        label_visibility="collapsed"
                    )
                    st.session_state.volumes[audio_num] = volume
                    
                    # Apply volume to audio element
                    st.markdown(f'''
                    <script>
                        var audio = document.getElementById('audio{audio_num}');
                        if (audio) {{
                            audio.volume = {volume / 100};
                        }}
                    </script>
                    ''', unsafe_allow_html=True)
                else:
                    st.warning(f"Audio {audio_num} not found")

st.markdown('</div>', unsafe_allow_html=True)

# JavaScript for Mode 1 (stop other audios when one plays)
if st.session_state.mode == 1:
    st.markdown('''
    <script>
        function stopOtherAudios(currentAudio) {
            for (let i = 1; i <= 10; i++) {
                if (i !== currentAudio) {
                    var audio = document.getElementById('audio' + i);
                    if (audio && !audio.paused) {
                        audio.pause();
                    }
                }
            }
        }
    </script>
    ''', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown(f"""
**Mode {st.session_state.mode} Active:**
- {'🎵 Only one audio plays at a time' if st.session_state.mode == 1 else '🎵 Multiple audios can play simultaneously'}
- 🔊 Use sliders to adjust individual volumes
- 📱 Optimized for iPhone 13
""")
