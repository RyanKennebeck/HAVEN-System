# ui/streamlit_app.py

import streamlit as st
import pandas as pd
import cv2
import os

st.set_page_config(layout="wide", page_title="HAVEN Dashboard")
st.title("🛡️ HAVEN Surveillance Event Viewer")

LOG_PATH = "logs/events.csv"
VIDEO_PATH = "input/test_footage.mp4"

# Load event logs
if os.path.exists(LOG_PATH):
    df = pd.read_csv(LOG_PATH)
    st.subheader("📋 Event Log")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No event log found.")

# Video viewer
if os.path.exists(VIDEO_PATH):
    st.subheader("🎥 Video Playback")
    with open(VIDEO_PATH, 'rb') as f:
        video_bytes = f.read()
    st.video(video_bytes)
else:
    st.warning("No video file found in input/ directory.")
