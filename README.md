---
**Developer:** Shreyash Singhai
---

# 🎙️ Meet-Summarizer (Nexus Module)

**Meet-Summarizer** is a high-performance AI agent designed to bridge the gap between verbal communication and structured project management. Developed as a specialized module within the **Nexus** AI ecosystem, his tool automates the extraction of intelligence from meeting audio and synchronizes it across professional workspaces.

## 🛠️ The Problem & The Solution
In fast-paced environments, manual meeting documentation is a bottleneck. This project implements a robust **"Ear-Brain-Hands"** architecture to:
1.  **Ear (Transcription):** Use optimized ASR to convert audio to text.
2.  **Brain (Reasoning):** Apply LLMs to categorize insights and tasks.
3.  **Hands (Automation):** Trigger API-driven workflows for Notion and Slack.

## 🚀 Key Features & Performance Optimizations
*   **Audio Pre-processing Pipeline:** Implements mono-conversion, **16kHz downsampling**, and **silent stripping** using `pydub` to reduce processing overhead for the transcription model.
*   **High-Speed Inference:** Leverages **Groq’s LPU** (Language Processing Unit) architecture with the **Llama 3.1 8B Instant** model for near-instantaneous JSON-structured analysis.
*   **Production-Grade Architecture:** Designed for **Python 3.13+** compatibility using `audioop-lts` for legacy audio manipulation support.
*   **Dual-Channel Integration:**
    *   **Notion:** Automatically generates structured pages with formatted headers, bulleted analysis, and interactive to-do lists.
    *   **Slack:** Sends executive summaries and conclusions directly to team channels via Webhooks.

## 🏗️ Technical Stack
*   **Frontend:** Streamlit
*   **Inference Engines:** OpenAI Whisper (ASR), Groq API (LLM)
*   **Audio Processing:** Pydub + FFmpeg
*   **External APIs:** Notion SDK, Slack Webhooks
*   **DevOps:** Dockerized for environment-agnostic deployment

## 📦 Installation & Setup

### Prerequisites
*   Python 3.13+
*   **FFmpeg** (Required for audio manipulation)
*   A Groq API Key, Notion Integration Token, and Slack Webhook URL

### Local Deployment
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SHREYASHSINGHAI/Meet-Summarizer.git](https://github.com/SHREYASHSINGHAI/Meet-Summarizer.git)
    cd Meet-Summarizer
    ```
2.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_key_here
    NOTION_TOKEN=your_token_here
    NOTION_DATABASE_ID=your_id_here
    SLACK_WEBHOOK_URL=your_webhook_here
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Launch the Application:**
    ```bash
    streamlit run app.py
    ```

## 🐋 Docker Deployment
For consistent deployment across environments:
```bash
docker build -t meet-summarizer .
docker run -p 8501:8501 --env-file .env meet-summarizer
