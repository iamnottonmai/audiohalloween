import streamlit as st
import os
import base64
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
    
    /* Audio container */
    .audio-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .audio-box h3 {
        margin-top: 0;
        color: #333;
    }
    
    /* Play button */
    .play-button {
        width: 120px;
        height: 120px;
        border-radius: 20px;
        background: linear-gradient(145deg, #666, #999);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }
    
    .play-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    
    .play-button:active {
        transform: scale(0.98);
    }
    
    .play-icon {
        width: 0;
        height: 0;
        border-left: 30px solid #333;
        border-top: 20px solid transparent;
        border-bottom: 20px solid transparent;
        margin-left: 8px;
    }
    
    .pause-icon {
        width: 30px;
        height: 40px;
        display: flex;
        gap: 8px;
    }
    
    .pause-bar {
        width: 8px;
        height: 40px;
        background-color: #333;
    }
    
    /* Volume control */
    .volume-control {
        margin-top: 15px;
    }
    
    .volume-label {
        font-size: 0.9em;
        color: #666;
        margin-bottom: 8px;
        transform: rotate(-90deg);
        display: inline-block;
    }
    
    .volume-slider {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        background: #ddd;
        outline: none;
        -webkit-appearance: none;
    }
    
    .volume-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #4CAF50;
        cursor: pointer;
    }
    
    .volume-slider::-moz-range-thumb {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #4CAF50;
        cursor: pointer;
        border: none;
    }
    
    .volume-value {
        font-size: 0.9em;
        color: #333;
        font-weight: bold;
        margin-top: 5px;
    }
    
    .mode-info {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.1em;
        color: #1976d2;
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

# Mode toggle button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button(f"Switch to Mode {2 if st.session_state.mode == 1 else 1}", use_container_width=True):
        st.session_state.mode = 2 if st.session_state.mode == 1 else 1
        st.rerun()

# Mode info
if st.session_state.mode == 1:
    st.markdown('<div class="mode-info">🔊 Mode 1: Only one audio plays at a time</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="mode-info">🔊 Mode 2: Multiple audios can play simultaneously</div>', unsafe_allow_html=True)

# Audio folder path
audio_folder = Path("audio")

# Check if audio folder exists
if not audio_folder.exists():
    st.warning("⚠️ 'audio' folder not found. Please create an 'audio' folder and add audio1.m4a to audio10.m4a files.")
    st.stop()

# Function to encode audio file to base64
def get_audio_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

# Collect all audio files and encode them
audio_data = {}
for i in range(1, 11):
    audio_file = audio_folder / f"audio{i}.m4a"
    if audio_file.exists():
        audio_data[i] = get_audio_base64(audio_file)

# Create HTML with embedded audio players
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .grid-item-centered {{
            grid-column: 2;
        }}
    </style>
</head>
<body>
    <div class="grid-container">
"""

# Add audio players
for i in range(1, 11):
    centered_class = ' grid-item-centered' if i == 10 else ''
    
    if i in audio_data:
        html_content += f"""
        <div class="audio-box{centered_class}">
            <h3>Audio #{i}</h3>
            <button class="play-button" onclick="togglePlay({i})" id="playBtn{i}">
                <div class="play-icon" id="playIcon{i}"></div>
            </button>
            <audio id="audio{i}" preload="auto">
                <source src="data:audio/m4a;base64,{audio_data[i]}" type="audio/m4a">
            </audio>
            <div class="volume-control">
                <label class="volume-label">Volume control</label>
                <input type="range" min="0" max="100" value="100" class="volume-slider" 
                       id="volume{i}" oninput="setVolume({i}, this.value)">
                <div class="volume-value" id="volumeValue{i}">100%</div>
            </div>
        </div>
        """
    else:
        html_content += f"""
        <div class="audio-box{centered_class}">
            <h3>Audio #{i}</h3>
            <p style="color: red;">File not found: audio{i}.m4a</p>
        </div>
        """

html_content += """
    </div>
    
    <script>
        const mode = """ + str(st.session_state.mode) + """;
        let currentlyPlaying = null;
        
        function togglePlay(num) {
            const audio = document.getElementById('audio' + num);
            const playBtn = document.getElementById('playBtn' + num);
            const playIcon = document.getElementById('playIcon' + num);
            
            if (audio.paused) {
                // Mode 1: Stop other audio files
                if (mode === 1) {
                    stopAllExcept(num);
                }
                
                audio.play();
                playIcon.innerHTML = '<div class="pause-icon"><div class="pause-bar"></div><div class="pause-bar"></div></div>';
                currentlyPlaying = num;
            } else {
                audio.pause();
                playIcon.innerHTML = '';
                playIcon.className = 'play-icon';
            }
        }
        
        function stopAllExcept(exceptNum) {
            for (let i = 1; i <= 10; i++) {
                if (i !== exceptNum) {
                    const audio = document.getElementById('audio' + i);
                    const playIcon = document.getElementById('playIcon' + i);
                    if (audio && !audio.paused) {
                        audio.pause();
                        audio.currentTime = 0;
                        playIcon.innerHTML = '';
                        playIcon.className = 'play-icon';
                    }
                }
            }
        }
        
        function setVolume(num, value) {
            const audio = document.getElementById('audio' + num);
            const volumeValue = document.getElementById('volumeValue' + num);
            audio.volume = value / 100;
            volumeValue.textContent = value + '%';
        }
        
        // Initialize volumes
        for (let i = 1; i <= 10; i++) {
            const audio = document.getElementById('audio' + i);
            if (audio) {
                audio.volume = 1.0;
                
                // Reset play button when audio ends
                audio.addEventListener('ended', function() {
                    const playIcon = document.getElementById('playIcon' + i);
                    playIcon.innerHTML = '';
                    playIcon.className = 'play-icon';
                });
            }
        }
    </script>
</body>
</html>
"""

# Display the HTML
st.components.v1.html(html_content, height=1400, scrolling=True)

# Footer
st.markdown("---")
st.markdown("""
### Instructions:
- **Mode 1**: Click play on any audio. Playing another will stop the first one.
- **Mode 2**: Click play on multiple audios to play them simultaneously.
- Drag the volume sliders to adjust each audio file's volume independently.
- Place your audio files (audio1.m4a to audio10.m4a) in the 'audio' folder.
""")
st.markdown("*🎃 Haunted House Audio Controller 👻*")
