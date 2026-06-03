# SECE AI Assistant

A multilingual AI chatbot for Sri Eshwar College of Engineering (SECE) with voice input/output support.

## Features

- **Multilingual Support**: English, Tamil, Hindi, Telugu, Kannada, Malayalam
- **Voice Input**: Chrome Web Speech API integration
- **Text-to-Speech**: Audio responses via gTTS
- **Semantic Search**: Intelligent information retrieval using sentence-transformers
- **Auto Translation**: Automatic language detection and translation
- **Session-based Chat**: Persistent conversation history

## Tech Stack

- **Backend**: Django 5.2.9
- **NLP**: sentence-transformers, langdetect
- **Translation**: googletrans
- **TTS**: gTTS (Google Text-to-Speech)
- **Frontend**: Vanilla JS + HTML/CSS

## Setup

### 1. Clone Repository
```bash
cd d:\mysite\mysite
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create `.env` file from template:
```bash
copy .env.example .env
```

Edit `.env` and set your configuration:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Project Structure

```
mysite/
├── mysite/              # Django project settings
│   ├── settings.py      # Configuration (env-based)
│   └── urls.py          # URL routing
├── chatbot/             # Main application
│   ├── views.py         # Request handlers
│   ├── simple_style.py  # Q&A logic with caching
│   ├── retrieval.py     # Semantic search engine
│   ├── translation_service.py  # Translation layer
│   ├── tts_service.py   # Audio generation
│   ├── utils.py         # Helper functions
│   └── templates/       # HTML templates
├── media/               # Generated audio files
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template
```

## Configuration

### Data File
Place college information in:
```
chatbot/college_data.txt
```

### Session Timeout
Configure in `settings.py`:
```python
SESSION_COOKIE_AGE = 3600  # 1 hour
```

### Audio Cleanup
Audio files older than 24 hours are automatically deleted on "New Chat" click.

## Performance Optimizations

1. **Model Caching**: SentenceTransformer loaded once at startup
2. **Audio Cleanup**: Automatic deletion of old MP3 files
3. **Session Storage**: Chat history stored in Django sessions
4. **Singleton Pattern**: Retrieval store cached globally

## Security Notes

- SECRET_KEY loaded from environment (never commit)
- DEBUG=False for production
- ALLOWED_HOSTS configured via environment
- No credentials in codebase

## Browser Support

- **Voice Input**: Chrome/Edge only (Web Speech API)
- **Audio Playback**: All modern browsers

## Known Limitations

- Voice input requires Chrome/Chromium browsers
- Translation accuracy depends on googletrans API
- First request slower (model loading)
- Session-based storage (no persistent DB)

## Future Enhancements

- [ ] Audio caching by text hash
- [ ] Database models for chat history
- [ ] Admin dashboard
- [ ] User authentication
- [ ] Export chat transcripts
- [ ] Mobile app integration

## License

Proprietary - Sri Eshwar College of Engineering

## Contact

For issues or questions, contact the development team.
