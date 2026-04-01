# Ultimate Media Downloader (Android)

A modern Android application built with Python, KivyMD, and `yt-dlp` to download media from YouTube, Facebook, and other web sources.

## Features
- **Modern UI**: Bootstrap-inspired Material Design interface.
- **Multiple Modes**: Download MP3 (Music), MP4 (Dramas/Web), and full Playlists.
- **Background Downloading**: Downloads run in a separate thread to keep the UI responsive.
- **Real-time Progress**: Shows download percentage, speed, and ETA.

## Project Structure
- `main.py`: The main application logic and UI definition.
- `buildozer.spec`: Configuration for building the Android APK.
- `requirements.txt`: Python dependencies.

## How to Build the APK

To build the Android app, you need a Linux environment (Ubuntu is recommended) with Buildozer installed.

### 1. Install Dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade buildozer
```

### 2. Build the APK
Navigate to the project directory and run:
```bash
buildozer android debug
```
The first build will take some time as it downloads the Android SDK and NDK. Once finished, the APK will be in the `bin/` directory.

### 3. Install on Android
Transfer the `.apk` file to your phone and install it. Make sure to grant **Storage Permissions** when prompted so the app can save files to `/sdcard/muzika`, `/sdcard/dramas`, etc.

## Note on FFmpeg
For high-quality MP3 conversion, `yt-dlp` usually requires FFmpeg. When building with Buildozer, you may need to include `ffmpeg-android` or similar recipes if the default conversion fails on some devices.
