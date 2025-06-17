import os
import tempfile
import whisper
import google.generativeai as genai
from flask import Flask, render_template, request, send_file, jsonify
from yt_dlp import YoutubeDL
from fpdf import FPDF
import random
import datetime
app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

BULLET_STYLES = ['●', '→', '•']
chosen_bullet = random.choice(BULLET_STYLES)

def download_audio(video_url):
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, 'audio.%(ext)s'),
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin'
    }   
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    for file in os.listdir(temp_dir):
        if file.endswith(".mp3"):
            return os.path.join(temp_dir, file)
    return None

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_text(text, style, language_code):
    prompt = f"""
You are a professional summarizer. Summarize the following transcript in {language_code}.

Summary style: {style}

Provide:
- A title
- A short intro
- Key points using {chosen_bullet} symbol
- A conclusion

Avoid using any symbols other than the {chosen_bullet} symbol.

Transcript:
{text}
"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    video_url = request.form.get('youtube_url')
    style = request.form.get('summary_style', 'Default')
    language_code = request.form.get('language', 'en')

    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    audio_path = download_audio(video_url)
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript, style, language_code)

    with open('summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)

    return jsonify({
        "summary": summary,
        "video_url": video_url
    })

@app.route('/download-pdf')
def download_pdf():
    # Initialize PDF with specific page settings
    pdf = FPDF(orientation='P', unit='pt', format='A4')  # Using points for more precise control
    pdf.add_page()
    
    # Set very conservative margins (1 inch = 72 points)
    margin = 72
    pdf.set_margins(margin, margin, margin)
    pdf.set_auto_page_break(True, margin)
    
    # Use a very basic font with small size
    pdf.set_font('Courier', size=10)  # Courier is a monospace font
    
    try:
        # Read the content
        with open("summary.txt", "r", encoding='utf-8') as f:
            content = f.read()
        
        # Add header with timestamp
        pdf.set_font('Courier', 'B', 10)
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        pdf.cell(0, 15, f'Generated: {timestamp}', ln=True)
        pdf.ln(10)
        
        # Reset font for main content
        pdf.set_font('Courier', size=10)
        
        # Calculate maximum characters per line (Courier is monospace)
        # A4 is 595 points wide, subtract margins, divide by character width
        page_width = 595 - (2 * margin)  # A4 width in points minus margins
        char_width = pdf.get_string_width('0')  # Width of one character
        max_chars = int(page_width / char_width) - 2  # Subtract 2 for safety
        
        # Process content line by line
        for line in content.split('\n'):
            if not line.strip():
                pdf.ln(10)  # Empty line
                continue
            
            # Replace problematic characters
            line = (line.replace('●', '*')
                   .replace('→', '->')
                   .replace('•', '*')
                   .replace('"', '"')
                   .replace('"', '"')
                   .replace(''', "'")
                   .replace(''', "'")
                   .replace('–', '-')
                   .replace('—', '-')
                   .replace('…', '...'))
            
            # Process line in chunks
            while line:
                if len(line) <= max_chars:
                    chunk = line
                    line = ''
                else:
                    # Find last space within max_chars
                    space_pos = line[0:max_chars].rfind(' ')
                    if space_pos == -1:
                        # If no space found, force break at max_chars
                        chunk = line[0:max_chars]
                        line = line[max_chars:]
                    else:
                        chunk = line[0:space_pos]
                        line = line[space_pos+1:]
                
                # Write chunk
                try:
                    # Convert to ASCII only if needed
                    chunk = ''.join(c for c in chunk if ord(c) < 128)
                    pdf.cell(0, 15, chunk, ln=True)
                except Exception as e:
                    print(f"Error writing chunk: {str(e)}")
                    continue
        
        # Save the PDF
        pdf_path = "summary.pdf"
        pdf.output(pdf_path)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"summary_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype="application/pdf"
        )
    
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        return jsonify({
            "error": "PDF generation failed",
            "details": str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)
