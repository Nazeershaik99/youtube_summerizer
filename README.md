This project is a **Flask-based web application** that allows users to paste a YouTube video URL, generate a **multilingual AI summary** using the **Gemini API**, and **download the summary as a PDF**. It also displays the embedded video and supports various summary styles (Academic, Creative, etc.).

---

## 🚀 Features

- 🎥 YouTube video audio extraction using `yt-dlp`
- 🧠 Transcription using OpenAI’s `Whisper`
- ✨ Summary generation via Google Gemini Pro (v2.0 Flash)
- 🌐 Supports multiple languages (English, Hindi, Bengali, Tamil)
- 📄 Clean bullet-style PDF summary download (Unicode supported)
- 📺 Embedded YouTube video preview
- 💬 Multiple summary styles: Default, Academic, Creative, Informal
- 🎨 TailwindCSS-powered responsive UI with loading animation

---

## 🛠️ Tech Stack

| Component          | Technology                     |
|-------------------|--------------------------------|
| Backend           | Flask                          |
| Transcription     | OpenAI Whisper                 |
| Summarization     | Google Gemini API              |
| YouTube Audio     | yt-dlp + ffmpeg                |
| Frontend          | HTML, Tailwind CSS, JavaScript |
| PDF Generation    | fpdf2 (Unicode-safe fonts)     |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-video-summarizer.git
cd youtube-video-summarizer
2. Set up Python Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
3. Install FFmpeg
Download FFmpeg: https://ffmpeg.org/download.html

Extract and add to your system path (or update path in app.py)

4. Set Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
5. Run the Application
bash
Copy
Edit
python app.py
Visit http://localhost:5000 in your browser.

📄 Usage
Paste a YouTube video URL into the input box.

Choose language and summary style.

Click "Summarize".

Wait for transcription and AI processing.

View embedded video + AI summary.

Click “Download PDF” to save the summary.

🧪 Example Output
vbnet
Copy
Edit
Title: How the Internet Works

Introduction:
In this video, we explore how the Internet functions at a fundamental level.

• The internet is a global network of networks.
• It uses IP addresses to route data packets.
• DNS translates domain names into IP addresses.
• TCP/IP protocol ensures reliability and delivery.

Conclusion:
Understanding how the Internet works helps us appreciate the technology we use daily.
📁 Project Structure
pgsql
Copy
Edit
YouTube_Video_Summarizer/
│
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # Frontend UI
├── static/                 # (Optional: Add CSS/JS here)
├── requirements.txt
├── summary.txt             # Temporary text file
├── summary.pdf             # Generated PDF summary
├── .env                    # API key (not tracked)
└── README.md
✅ To-Do & Improvements
 Add user authentication (optional)

 Add history of past summaries

 Support video upload (non-YouTube)

 Improve error handling and timeouts

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgements
Google Gemini API

OpenAI Whisper

yt-dlp

fpdf2

yaml
Copy
Edit
