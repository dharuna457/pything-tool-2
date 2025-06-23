from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
import os
from datetime import datetime # Use datetime for current year
import uuid # For unique filenames
from werkzeug.utils import secure_filename # For safe handling of uploaded files

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = 'your_super_secret_and_long_key_here_please_change_this_in_production' # IMPORTANT: Change this!

# Create necessary folders if they don't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(os.path.join(app.config['STATIC_FOLDER'], 'images')):
    os.makedirs(os.path.join(app.config['STATIC_FOLDER'], 'images'))
if not os.path.exists(os.path.join(app.config['STATIC_FOLDER'], 'css')):
    os.makedirs(os.path.join(app.config['STATIC_FOLDER'], 'css'))

# Route to serve files from the 'uploads' directory (for generated content)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Import Tool Functions ---
# Make sure these correspond to your Python files in the 'tools/' directory
from tools.quotation_tool import generate_quotation_pdf
from tools.youtube_downloader_tool import download_youtube_video
from tools.weather_tool import get_weather_and_speak
from tools.qr_with_logo_tool import generate_qr_with_logo
from tools.bulk_certificates_tool import generate_bulk_certificates
from tools.id_card_tool import generate_id_card_pdf
from tools.instagram_dp_tool import download_insta_dp
from tools.youtube_thumbnail_tool import download_youtube_thumbnail
from tools.dictionary_tool import get_word_definition

# from tools.audio_transcriber_tool import transcribe_audio # Uncomment when ready with API/local setup


@app.route('/')
def index():
    current_year = datetime.now().year # Get the current year
    tools = [
        # --- Tools you mentioned previously or are common ---
        # NOTE: If you don't have a template for these yet, they will show a basic "Under Construction" page
        {"name": "PDF Operations", "description": "Merge, split, compress, or convert PDFs.", "url": "/pdf_tools", "icon": "bi-filetype-pdf"},
        {"name": "Password Generator", "description": "Generate strong, random passwords.", "url": "/password_generator", "icon": "bi-key"},
        {"name": "Unit Converter", "description": "Convert between various units of measurement.", "url": "/unit_converter", "icon": "bi-arrow-left-right"},
        {"name": "Date Calculator", "description": "Calculate differences between dates.", "url": "/date_calculator", "icon": "bi-calendar"},
        {"name": "Text Editor", "description": "A simple online text editor.", "url": "/text_editor", "icon": "bi-pencil"},
        {"name": "Image Optimizer", "description": "Optimize images for web use.", "url": "/image_optimizer", "icon": "bi-image"},
        {"name": "URL Shortener", "description": "Shorten long URLs.", "url": "/url_shortener", "icon": "bi-link-45deg"},

        # --- Tools from your templates folder image ---
        {"name": "Audio Transcriber", "description": "Convert spoken audio from a file to text.", "url": "/audio_transcriber", "icon": "bi-mic"},
        {"name": "Bulk Certificates", "description": "Generate multiple personalized PDF certificates from a CSV.", "url": "/bulk_certificates", "icon": "bi-award"},
       
        {"name": "Dictionary", "description": "Look up definitions, synonyms, and antonyms of words.", "url": "/dictionary", "icon": "bi-book"},
        {"name": "ID Card Generator", "description": "Design and print professional ID cards in PDF.", "url": "/id_card", "icon": "bi-person-badge"},
        {"name": "Instagram DP Downloader", "description": "Download high-resolution Instagram Profile Pictures.", "url": "/instagram_dp", "icon": "bi-instagram"},
        {"name": "QR Code with Logo", "description": "Create QR codes with your custom logo embedded.", "url": "/qr_with_logo", "icon": "bi-qr-code-fill"},
        {"name": "Quotation Generator", "description": "Generate professional PDF quotations.", "url": "/quotation", "icon": "bi-receipt"},
        {"name": "Weather Reporter", "description": "Get current weather conditions and listen to a speech summary.", "url": "/weather", "icon": "bi-cloud-sun"},
        {"name": "YouTube Downloader", "description": "Download videos from YouTube.", "url": "/youtube_downloader", "icon": "bi-youtube"},
        {"name": "YouTube Thumbnail Downloader", "description": "Download thumbnails from YouTube videos.", "url": "/youtube_thumbnail", "icon": "bi-image"},
    ]
    return render_template('index.html', tools=tools, current_year=current_year)


# --- TOOL ROUTES ---

# --- Placeholder/Conceptual Tool Routes (If you don't have dedicated .html for these yet) ---
# These will show a simple "Under Construction" page.
# You can replace these with calls to your tool logic and render specific templates later.

@app.route('/pdf_tools')
def pdf_tools():
    return render_template('tool_under_construction.html', tool_name="PDF Operations")

@app.route('/password_generator')
def password_generator():
    return render_template('tool_under_construction.html', tool_name="Password Generator")

@app.route('/unit_converter')
def unit_converter():
    return render_template('tool_under_construction.html', tool_name="Unit Converter")

@app.route('/date_calculator')
def date_calculator():
    return render_template('tool_under_construction.html', tool_name="Date Calculator")

@app.route('/text_editor')
def text_editor():
    return render_template('tool_under_construction.html', tool_name="Text Editor")

@app.route('/image_optimizer')
def image_optimizer():
    return render_template('tool_under_construction.html', tool_name="Image Optimizer")

@app.route('/url_shortener')
def url_shortener():
    return render_template('tool_under_construction.html', tool_name="URL Shortener")


# --- Implemented Tool Routes (Matching your templates folder) ---

# Quotation Generator
@app.route('/quotation', methods=['GET', 'POST'])
def quotation_generator():
    if request.method == 'POST':
        company_name = request.form['company_name']
        client_name = request.form['client_name']
        item_description = request.form['item_description']
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash("Invalid amount. Please enter a number.", "danger")
            return render_template('quotation.html', company_name=company_name, client_name=client_name, item_description=item_description)

        pdf_filename = f"quotation_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        
        try:
            generate_quotation_pdf(company_name, client_name, item_description, amount, output_path)
            return send_file(output_path, as_attachment=True, download_name=pdf_filename)
        except Exception as e:
            flash(f"Error generating quotation: {e}", "danger")
            return render_template('quotation.html', company_name=company_name, client_name=client_name, item_description=item_description)
    return render_template('quotation.html')


# YouTube Downloader
@app.route('/youtube_downloader', methods=['GET', 'POST'])
def youtube_downloader():
    if request.method == 'POST':
        video_url = request.form['video_url']
        download_quality = request.form['quality']
        
        try:
            output_template = os.path.join(app.config['UPLOAD_FOLDER'], f"youtube_video_{uuid.uuid4().hex[:8]}.%(ext)s")
            downloaded_file_path = download_youtube_video(video_url, download_quality, output_template)
            
            if downloaded_file_path and os.path.exists(downloaded_file_path):
                original_filename = os.path.basename(downloaded_file_path)
                return send_file(downloaded_file_path, as_attachment=True, download_name=original_filename)
            else:
                flash("Failed to download video. Please check the URL or try again.", "danger")
                return render_template('youtube_downloader.html')
        except Exception as e:
            flash(f"Error downloading video: {e}. Please check the URL or try again.", "danger")
            return render_template('youtube_downloader.html')
    return render_template('youtube_downloader.html')


# Weather Reporter
@app.route('/weather', methods=['GET', 'POST'])
def weather_reporter():
    weather_info = None
    audio_url = None
    if request.method == 'POST':
        city = request.form['city']
        audio_filename = f"weather_{city.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        try:
            weather_text = get_weather_and_speak(city, audio_path)
            weather_info = weather_text
            audio_url = url_for('uploaded_file', filename=audio_filename)
        except Exception as e:
            flash(f"Error getting weather: {e}. Please ensure the city is valid and API key is set.", "danger")
            if os.path.exists(audio_path):
                os.remove(audio_path)
            return render_template('weather.html', weather_info=None, audio_url=None)
    return render_template('weather.html', weather_info=weather_info, audio_url=audio_url)


# QR Code with Logo
@app.route('/qr_with_logo', methods=['GET', 'POST'])
def qr_code_with_logo_generator():
    qr_code_url = None
    if request.method == 'POST':
        data = request.form['data']
        
        logo_file = request.files.get('logo_file')
        logo_path = None
        if logo_file and logo_file.filename != '':
            filename = secure_filename(logo_file.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_logo_{uuid.uuid4().hex[:8]}_{filename}")
            logo_file.save(logo_path)
        else:
            logo_path = os.path.join(app.config['STATIC_FOLDER'], 'images', 'default_qr_logo.png')
            if not os.path.exists(logo_path):
                flash("Default QR logo not found. Please ensure 'static/images/default_qr_logo.png' exists or upload a logo.", "warning")
                logo_path = None
        
        qr_filename = f"qr_logo_{uuid.uuid4().hex[:8]}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
        
        try:
            generate_qr_with_logo(data, logo_path, output_path)
            qr_code_url = url_for('uploaded_file', filename=qr_filename)
        except Exception as e:
            flash(f"Error generating QR code: {e}", "danger")
            qr_code_url = None
        finally:
            if logo_path and 'temp_logo' in logo_path: # Only remove if it was an uploaded temp file
                os.remove(logo_path)
        
        return render_template('qr_with_logo.html', qr_code_url=qr_code_url)
    return render_template('qr_with_logo.html')


# Bulk Certificates
@app.route('/bulk_certificates', methods=['GET', 'POST'])
def bulk_certificates_generator():
    if request.method == 'POST':
        template_file = request.files.get('template_file')
        csv_file = request.files.get('csv_file')

        if not template_file or template_file.filename == '':
            flash('No certificate template file uploaded.', 'danger')
            return render_template('bulk_certificates.html')
        if not csv_file or csv_file.filename == '':
            flash('No CSV data file uploaded.', 'danger')
            return render_template('bulk_certificates.html')

        if not template_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            flash('Invalid template file type. Please upload a PNG or JPG image.', 'danger')
            return render_template('bulk_certificates.html')
        if not csv_file.filename.lower().endswith('.csv'):
            flash('Invalid CSV file type. Please upload a CSV file.', 'danger')
            return render_template('bulk_certificates.html')

        temp_template_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"temp_cert_template_{uuid.uuid4().hex[:8]}.png"))
        temp_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"temp_cert_data_{uuid.uuid4().hex[:8]}.csv"))
        
        template_file.save(temp_template_path)
        csv_file.save(temp_csv_path)

        output_zip_filename = f"certificates_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}.zip"
        output_zip_path = os.path.join(app.config['UPLOAD_FOLDER'], output_zip_filename)

        try:
            generate_bulk_certificates(temp_template_path, temp_csv_path, output_zip_path)
            # Ensure the zip file exists before sending
            if not os.path.exists(output_zip_path):
                raise FileNotFoundError("Zip file was not created successfully by the tool.")
            return send_file(output_zip_path, as_attachment=True, download_name=output_zip_filename)
        except Exception as e:
            flash(f"Error generating certificates: {e}. Check CSV format and template.", "danger")
            return render_template('bulk_certificates.html')
        finally:
            if os.path.exists(temp_template_path):
                os.remove(temp_template_path)
            if os.path.exists(temp_csv_path):
                os.remove(temp_csv_path)
            # The zip file is sent by Flask, it's generally safe to rely on Flask to manage its lifecycle after send_file.
    return render_template('bulk_certificates.html')


# ID Card Generator
@app.route('/id_card', methods=['GET', 'POST'])
def id_card_generator():
    if request.method == 'POST':
        name = request.form['name']
        id_number = request.form['id_number']
        title = request.form['title']
        organization = request.form['organization']
        
        profile_pic = request.files.get('profile_pic')
        profile_pic_path = None
        if profile_pic and profile_pic.filename != '':
            filename = secure_filename(profile_pic.filename)
            profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'], f"id_pic_{uuid.uuid4().hex[:8]}_{filename}")
            profile_pic.save(profile_pic_path)
        
        card_filename = f"id_card_{name.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], card_filename)
        
        try:
            generate_id_card_pdf(name, id_number, title, organization, profile_pic_path, output_path)
            return send_file(output_path, as_attachment=True, download_name=card_filename)
        except Exception as e:
            flash(f"Error generating ID card: {e}", "danger")
            return render_template('id_card.html', name=name, id_number=id_number, title=title, organization=organization)
        finally:
            if profile_pic_path and os.path.exists(profile_pic_path):
                os.remove(profile_pic_path)
    return render_template('id_card.html')


# Audio Transcriber (Conceptual - uncomment the tool import if you implement this)
@app.route('/audio_transcriber', methods=['GET', 'POST'])
def audio_transcriber():
    transcription_text = None
    if request.method == 'POST':
        audio_file = request.files.get('audio_file')
        if not audio_file or audio_file.filename == '':
            flash("No audio file selected.", "danger")
            return render_template('audio_transcriber.html')
        
        # Save audio temporarily
        filename = secure_filename(audio_file.filename)
        temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_audio_{uuid.uuid4().hex[:8]}_{filename}")
        audio_file.save(temp_audio_path)

        try:
            # THIS IS A PLACEHOLDER. Replace with actual API integration or local ML model.
            # transcription_text = transcribe_audio(temp_audio_path)
            transcription_text = f"Transcription for {filename} completed (conceptual). This requires a real transcription API or model."

        except Exception as e:
            flash(f"Error transcribing audio: {e}. Check API key and file format.", "danger")
            transcription_text = "Transcription failed due to a backend error."
        finally:
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path) # Clean up temp audio file

        return render_template('audio_transcriber.html', transcription_text=transcription_text)
    return render_template('audio_transcriber.html')


# Instagram DP Downloader
@app.route('/instagram_dp', methods=['GET', 'POST'])
def instagram_dp_downloader():
    dp_url = None
    if request.method == 'POST':
        username = request.form['username']
        output_filename = f"insta_dp_{username.replace('.', '_')}_{uuid.uuid4().hex[:8]}.jpg"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        try:
            download_insta_dp(username, output_path)
            dp_url = url_for('uploaded_file', filename=output_filename)
        except Exception as e:
            flash(f"Error downloading DP: {e}. It might be private, not exist, or require login.", "danger")
            if os.path.exists(output_path):
                os.remove(output_path)
            return render_template('instagram_dp.html', dp_url=None)

        return render_template('instagram_dp.html', dp_url=dp_url)
    return render_template('instagram_dp.html')


# YouTube Thumbnail Downloader
@app.route('/youtube_thumbnail', methods=['GET', 'POST'])
def youtube_thumbnail_downloader():
    thumbnail_url = None
    if request.method == 'POST':
        video_url = request.form['video_url']
        thumbnail_filename = f"yt_thumbnail_{uuid.uuid4().hex[:8]}.jpg"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename)
        
        try:
            download_youtube_thumbnail(video_url, output_path)
            thumbnail_url = url_for('uploaded_file', filename=thumbnail_filename)
        except Exception as e:
            flash(f"Error downloading thumbnail: {e}. Please check the YouTube URL.", "danger")
            if os.path.exists(output_path):
                os.remove(output_path)
            return render_template('youtube_thumbnail.html', thumbnail_url=None)
            
    return render_template('youtube_thumbnail.html', thumbnail_url=thumbnail_url)


# Dictionary
@app.route('/dictionary', methods=['GET', 'POST'])
def dictionary_tool():
    word_info = None
    if request.method == 'POST':
        word = request.form['word']
        try:
            word_info = get_word_definition(word)
            if not word_info:
                flash(f"Could not find definition for '{word}'.", "warning")
        except Exception as e:
            flash(f"Error fetching definition: {e}. Try again later.", "danger")
            word_info = None
    return render_template('dictionary.html', word_info=word_info)



if __name__ == '__main__':
    app.run(debug=True)