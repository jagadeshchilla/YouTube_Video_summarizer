import streamlit as st
from dotenv import load_dotenv
import os
from pathlib import Path
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json
import re
from datetime import datetime
import pandas as pd
from collections import Counter
import io

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Different prompt templates for various summary types
prompts = {
    "bullet_points": """You are a YouTube video summarizer. Create a concise bullet-point summary of the video transcript within 250 words. Focus on key points and main ideas.""",
    
    "detailed": """You are a YouTube video summarizer. Provide a comprehensive detailed summary of the video transcript within 500 words. Include context, examples, and explanations.""",
    
    "key_insights": """You are a YouTube video summarizer. Extract the most important insights, takeaways, and actionable points from the video transcript within 300 words.""",
    
    "timeline": """You are a YouTube video summarizer. Create a chronological timeline summary of the video content, highlighting the progression of topics discussed within 400 words."""
}

# Enhanced functions for video analysis and processing

def extract_video_id(video_url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    return None

def get_video_metadata(video_id):
    """Get video metadata using YouTube Data API (requires API key) or web scraping"""
    try:
        # Using web scraping as fallback (YouTube Data API requires additional setup)
        url = f"https://www.youtube.com/watch?v={video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Extract title from HTML
        title_match = re.search(r'<title>([^<]+)</title>', response.text)
        title = title_match.group(1).replace(' - YouTube', '') if title_match else "Unknown Title"
        
        return {
            'title': title,
            'video_id': video_id,
            'url': url
        }
    except Exception as e:
        return {
            'title': "Unknown Title",
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}"
        }

def analyze_transcript(transcript_text):
    """Analyze transcript for various metrics"""
    words = transcript_text.split()
    word_count = len(words)
    
    # Calculate speaking speed (words per minute) - assuming average video length
    # This is an approximation since we don't have exact duration
    estimated_duration = len(transcript_text) / 200  # Rough estimate
    speaking_speed = (word_count / estimated_duration) * 60 if estimated_duration > 0 else 0
    
    # Extract most common words (excluding common stop words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    word_freq = Counter([word.lower() for word in words if word.lower() not in stop_words and len(word) > 3])
    top_words = word_freq.most_common(10)
    
    return {
        'word_count': word_count,
        'character_count': len(transcript_text),
        'speaking_speed': round(speaking_speed, 2),
        'top_words': top_words,
        'estimated_duration': round(estimated_duration, 2)
    }

def extract_keywords(transcript_text):
    """Extract key phrases and topics using Gemini"""
    try:
        model = genai.GenerativeModel("models/gemma-3-27b-it")
        prompt = f"""Extract the main topics and key phrases from this video transcript. Return them as a comma-separated list of the most important topics and keywords: {transcript_text[:1000]}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Unable to extract keywords"

def analyze_sentiment(transcript_text):
    """Basic sentiment analysis using Gemini"""
    try:
        model = genai.GenerativeModel("models/gemma-3-27b-it")
        prompt = f"""Analyze the sentiment of this video transcript. Determine if it's positive, negative, or neutral and provide a brief explanation: {transcript_text[:1000]}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Unable to analyze sentiment"

def generate_gemini_content(transcript_text, prompt):
    """Generate content using Gemini model"""
    model = genai.GenerativeModel("models/gemma-3-27b-it")
    response = model.generate_content(transcript_text + prompt)
    return response.text

def extract_transcript(video_url):
    """Extract transcript from YouTube video"""
    try:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL format")
            return None, None
            
        transcript = YouTubeTranscriptApi().fetch(video_id)
        transcript_text = " ".join([snippet.text for snippet in transcript])
        return transcript_text, video_id
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None, None

def export_to_text(content, filename):
    """Export content to text file"""
    return io.BytesIO(content.encode())

def export_to_json(data, filename):
    """Export data to JSON file"""
    json_str = json.dumps(data, indent=2)
    return io.BytesIO(json_str.encode())


# Main Application Interface
st.title("🎥 Enhanced YouTube Video Summarizer")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    summary_type = st.selectbox(
        "Choose Summary Type:",
        ["bullet_points", "detailed", "key_insights", "timeline"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    st.header("📊 Analysis Options")
    show_metadata = st.checkbox("Show Video Metadata", value=True)
    show_analysis = st.checkbox("Show Transcript Analysis", value=True)
    show_keywords = st.checkbox("Extract Keywords", value=True)
    show_sentiment = st.checkbox("Analyze Sentiment", value=True)

# Main input area
col1, col2 = st.columns([2, 1])

with col1:
    youtube_url = st.text_input("Enter YouTube video URL:", placeholder="https://www.youtube.com/watch?v=...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
    analyze_button = st.button("🔍 Analyze Video", type="primary")

# Process single video
if analyze_button and youtube_url:
    with st.spinner("Processing video..."):
        transcript_text, video_id = extract_transcript(youtube_url)
        
        if transcript_text and video_id:
            # Get video metadata
            metadata = get_video_metadata(video_id)
            
            # Display video thumbnail and basic info
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
            
            with col2:
                st.subheader(f"📺 {metadata['title']}")
                st.write(f"**Video ID:** {video_id}")
                st.write(f"**URL:** {metadata['url']}")
            
            st.markdown("---")
            
            # Generate summary
            st.subheader("📝 Summary")
            summary = generate_gemini_content(transcript_text, prompts[summary_type])
            st.write(summary)
            
            # Show additional analysis if requested
            if show_analysis:
                st.markdown("---")
                st.subheader("📊 Transcript Analysis")
                analysis = analyze_transcript(transcript_text)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Word Count", analysis['word_count'])
                with col2:
                    st.metric("Character Count", analysis['character_count'])
                with col3:
                    st.metric("Speaking Speed (WPM)", analysis['speaking_speed'])
                
                # Top words visualization
                if analysis['top_words']:
                    st.write("**Most Frequent Words:**")
                    words_df = pd.DataFrame(analysis['top_words'], columns=['Word', 'Count'])
                    st.bar_chart(words_df.set_index('Word'))
            
            if show_keywords:
                st.markdown("---")
                st.subheader("🔑 Key Topics & Keywords")
                keywords = extract_keywords(transcript_text)
                st.write(keywords)
            
            if show_sentiment:
                st.markdown("---")
                st.subheader("😊 Sentiment Analysis")
                sentiment = analyze_sentiment(transcript_text)
                st.write(sentiment)
            
            # Export options
            st.markdown("---")
            st.subheader("💾 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Export Summary"):
                    text_file = export_to_text(summary, f"summary_{video_id}.txt")
                    st.download_button(
                        label="Download Summary",
                        data=text_file.getvalue(),
                        file_name=f"summary_{video_id}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("📋 Export Full Data"):
                    full_data = {
                        'metadata': metadata,
                        'summary': summary,
                        'analysis': analyze_transcript(transcript_text),
                        'keywords': extract_keywords(transcript_text),
                        'sentiment': analyze_sentiment(transcript_text),
                        'timestamp': datetime.now().isoformat()
                    }
                    json_file = export_to_json(full_data, f"analysis_{video_id}.json")
                    st.download_button(
                        label="Download Full Analysis",
                        data=json_file.getvalue(),
                        file_name=f"analysis_{video_id}.json",
                        mime="application/json"
                    )
            
            with col3:
                if st.button("📝 Export Transcript"):
                    transcript_file = export_to_text(transcript_text, f"transcript_{video_id}.txt")
                    st.download_button(
                        label="Download Transcript",
                        data=transcript_file.getvalue(),
                        file_name=f"transcript_{video_id}.txt",
                        mime="text/plain"
                    )

# Batch processing section
st.markdown("---")
st.subheader("🔄 Batch Processing")

batch_urls = st.text_area(
    "Enter multiple YouTube URLs (one per line):",
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.youtube.com/watch?v=...",
    height=100
)

if st.button("🚀 Process Batch") and batch_urls:
    urls = [url.strip() for url in batch_urls.split('\n') if url.strip()]
    
    if urls:
        batch_results = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, url in enumerate(urls):
            status_text.text(f"Processing video {i+1}/{len(urls)}")
            
            transcript_text, video_id = extract_transcript(url)
            if transcript_text and video_id:
                metadata = get_video_metadata(video_id)
                summary = generate_gemini_content(transcript_text, prompts[summary_type])
                
                batch_results.append({
                    'url': url,
                    'video_id': video_id,
                    'title': metadata['title'],
                    'summary': summary,
                    'word_count': len(transcript_text.split())
                })
            
            progress_bar.progress((i + 1) / len(urls))
        
        status_text.text("Batch processing complete!")
        
        # Display batch results
        if batch_results:
            st.subheader("📊 Batch Results")
            
            # Create a summary table
            results_df = pd.DataFrame(batch_results)
            st.dataframe(results_df[['title', 'word_count']], use_container_width=True)
            
            # Export batch results
            if st.button("📊 Export Batch Results"):
                batch_json = export_to_json(batch_results, "batch_results.json")
                st.download_button(
                    label="Download Batch Results",
                    data=batch_json.getvalue(),
                    file_name="batch_results.json",
                    mime="application/json"
                )
