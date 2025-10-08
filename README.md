# 🎥 Enhanced YouTube Video Summarizer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Google AI](https://img.shields.io/badge/Google%20AI-Gemini-green.svg)](https://ai.google.dev)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

A powerful AI-powered tool that extracts transcripts from YouTube videos and generates intelligent summaries using Google's Gemini AI. Perfect for content creators, researchers, students, and anyone who needs to quickly understand video content.

## ✨ Features

### 🔍 **Multiple Summary Types**
- **Bullet Points**: Concise key points (250 words)
- **Detailed**: Comprehensive summary (500 words) 
- **Key Insights**: Important takeaways and actionable points (300 words)
- **Timeline**: Chronological progression of topics (400 words)

### 📊 **Advanced Analysis**
- **Video Metadata**: Title, ID, URL extraction
- **Transcript Statistics**: Word count, character count, speaking speed
- **Keyword Extraction**: AI-powered topic and key phrase identification
- **Sentiment Analysis**: Positive/negative/neutral content analysis
- **Word Frequency**: Most common words visualization

### 🔄 **Batch Processing**
- Process multiple YouTube videos simultaneously
- Progress tracking with visual indicators
- Batch results export and comparison

### 💾 **Export Options**
- **Text Files**: Download summaries and transcripts
- **JSON Files**: Complete analysis data in structured format
- **Batch Results**: Processed multiple videos data

### 🎯 **Smart Features**
- Support for multiple YouTube URL formats
- Robust error handling and validation
- Professional UI with configurable options
- Real-time processing with progress indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google AI API key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd youtube-summarizer
   ```

2. **Create virtual environment**
   ```bash
   conda create -n venv python=3.10
   conda activate venv/
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 How to Use

### Single Video Analysis
1. Enter a YouTube video URL in the input field
2. Choose your preferred summary type from the sidebar
3. Configure analysis options (metadata, keywords, sentiment)
4. Click "🔍 Analyze Video"
5. View results and export as needed

### Batch Processing
1. Scroll to the "Batch Processing" section
2. Enter multiple YouTube URLs (one per line)
3. Click "🚀 Process Batch"
4. Monitor progress and export results

### Export Options
- **📄 Export Summary**: Download summary as text file
- **📋 Export Full Data**: Download complete analysis as JSON
- **📝 Export Transcript**: Download raw transcript

## 🛠️ Configuration

Use the sidebar to customize your analysis:

- **Summary Type**: Choose from 4 different summary formats
- **Show Video Metadata**: Display video information
- **Show Transcript Analysis**: Display statistics and word frequency
- **Extract Keywords**: Enable AI-powered keyword extraction
- **Analyze Sentiment**: Enable sentiment analysis

## 📋 Requirements

```
youtube_transcript_api
streamlit
google-generativeai
python-dotenv
requests
pandas
```

## 🔑 API Setup

### Google AI API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

## 🎯 Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## 📊 Example Output

### Summary Types
- **Bullet Points**: Quick, scannable key points
- **Detailed**: Comprehensive analysis with context
- **Key Insights**: Actionable takeaways and main concepts
- **Timeline**: Chronological breakdown of content

### Analysis Metrics
- Word count and character count
- Speaking speed (words per minute)
- Most frequent words chart
- Sentiment analysis results
- Extracted keywords and topics

---

**Made with ❤️ for the content creation community**
