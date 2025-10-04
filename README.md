# 🚀 AI-Powered CV Parser & Form Autofill

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Angular](https://img.shields.io/badge/Angular-17+-red.svg)](https://angular.io/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Cohere](https://img.shields.io/badge/Cohere-LLM-purple.svg)](https://cohere.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful CV/Resume parser that uses **Cohere's LLM** for intelligent entity extraction and automatically fills job application forms. Built with Angular frontend and Flask backend.

<img width="auto" height="auto" alt="cv-parser-ai" src="https://github.com/user-attachments/assets/81950ba1-fb23-478d-90ad-3c7c20c41f95" />


## ✨ Features

- 🤖 **AI-Powered Parsing** - Uses Cohere's Command-R-Plus LLM for accurate extraction
- 📄 **Multiple Formats** - Supports PDF, DOCX, and TXT files
- 🎯 **Smart Extraction** - Extracts personal info, education, experience, and skills
- 🔄 **Auto-Fill Forms** - Instantly populates job application forms
- 🎨 **Beautiful UI** - Modern, responsive Angular interface with drag-and-drop
- 🔙 **Intelligent Fallback** - Uses regex parsing if LLM unavailable
- ⚡ **Real-time Progress** - Live upload and parsing progress indicators
- 🛡️ **Error Handling** - Comprehensive error handling and validation

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Cohere AI** - LLM for entity extraction
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **Angular 17+** - Frontend framework
- **TypeScript** - Type-safe JavaScript
- **RxJS** - Reactive programming
- **Tailwind CSS** - Utility-first styling

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 18+ and npm
- Angular CLI (`npm install -g @angular/cli`)
- Cohere API key ([Get free key](https://dashboard.cohere.com/api-keys))

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/cv-parser-ai.git
cd cv-parser-ai

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export COHERE_API_KEY='your-cohere-api-key-here'

# Run the server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend/cv-parser-frontend

# Install dependencies
npm install

# Run development server
ng serve
```

Frontend will run on `http://localhost:4200`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Required
COHERE_API_KEY=your_cohere_api_key_here

# Optional
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
```

### Cohere API Key

1. Sign up at [Cohere Dashboard](https://dashboard.cohere.com/)
2. Navigate to [API Keys](https://dashboard.cohere.com/api-keys)
3. Create or copy your API key
4. Add to environment variables

**Free Tier:** 100 API calls per month (perfect for testing)

### Without Cohere (Optional)

The system automatically falls back to regex-based parsing if no API key is provided:

```bash
# Simply run without setting COHERE_API_KEY
python app.py
```

## 🚀 Usage

### 1. Start Both Servers

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend
cd frontend/cv-parser-frontend
ng serve
```

### 2. Open Application

Navigate to `http://localhost:4200` in your browser

### 3. Upload CV

- Drag and drop your CV file, or
- Click to browse and select file
- Supported formats: PDF, DOCX, TXT

### 4. Parse & Auto-Fill

- Click "Parse CV & Auto-Fill Form"
- Wait for processing (usually 2-5 seconds)
- Form fields will automatically populate

### 5. Review & Submit

- Review extracted information
- Edit any fields as needed
- Add/remove education or experience entries
- Submit application

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Parse CV

**POST** `/parse-cv`

Upload and parse a CV file.

**Request:**
```http
POST /api/parse-cv
Content-Type: multipart/form-data

file: <CV file (PDF/DOCX/TXT)>
```

**Response:**
```json
{
  "success": true,
  "method": "cohere",
  "data": {
    "personalInfo": {
      "fullName": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123"
    },
    "education": [
      {
        "degree": "Bachelor of Science in Computer Science",
        "institution": "MIT",
        "year": "2020"
      }
    ],
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "period": "2020 - Present"
      }
    ],
    "skills": ["Python", "JavaScript", "React", "Docker"]
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Unsupported file format"
}
```

#### 2. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok",
  "cohere_available": true
}
```

#### 3. Configuration Status

**GET** `/config`

Check Cohere configuration status.

**Response:**
```json
{
  "cohere_configured": true,
  "cohere_available": true
}
```

## 📁 Project Structure

```
cv-parser-ai/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (create this)
│   └── README.md             # Backend documentation
│
├── frontend/
│   └── cv-parser-frontend/
│       ├── src/
│       │   ├── app/
│       │   │   ├── app.component.ts    # Main component
│       │   │   └── app.config.ts       # App configuration
│       │   ├── index.html
│       │   └── main.ts
│       ├── angular.json
│       ├── package.json
│       └── README.md         # Frontend documentation
│
├── docs/
│   ├── demo.png
│   ├── upload.gif
│   └── architecture.md
│
├── tests/
│   ├── test_parser.py
│   └── sample_cvs/
│
├── .gitignore
├── LICENSE
└── README.md                 # This file
```

## 🧠 How It Works

### Architecture Overview

```
┌─────────────┐        ┌──────────────┐        ┌─────────────┐
│   Angular   │───────>│    Flask     │───────>│  Cohere AI  │
│  Frontend   │<───────│   Backend    │<───────│     LLM     │
└─────────────┘        └──────────────┘        └─────────────┘
                               │
                               ▼
                       ┌──────────────┐
                       │ File Parsers │
                       │ (PDF/DOCX)   │
                       └──────────────┘
```

### Processing Pipeline

1. **File Upload**
   - User uploads CV via Angular interface
   - File sent to Flask backend via HTTP POST

2. **Text Extraction**
   - PDF: PyPDF2 extracts text from pages
   - DOCX: python-docx reads paragraphs
   - TXT: Direct UTF-8 decoding

3. **AI-Powered Parsing (Primary)**
   - Send extracted text to Cohere LLM
   - LLM analyzes context and structure
   - Returns structured JSON with entities

4. **Regex Fallback (If needed)**
   - Pattern matching for emails, phones
   - Keyword detection for skills
   - Date range extraction for experience

5. **Data Validation**
   - Validate JSON structure
   - Fill missing fields with regex
   - Ensure minimum required data

6. **Form Auto-Fill**
   - Angular receives parsed data
   - Maps data to form fields
   - Creates dynamic sections
   - User reviews and edits

### Cohere LLM Parsing

The system uses a carefully crafted prompt to instruct Cohere:

```python
prompt = """You are a CV/Resume parser. Extract the following 
information from the CV text below and return ONLY a valid JSON 
object with no additional text or explanation.

CV Text:
[CV content]

Extract and return JSON in this exact format:
{
  "personalInfo": {...},
  "education": [...],
  "experience": [...],
  "skills": [...]
}
"""
```

**Why Cohere?**
- Context-aware understanding
- Handles non-standard formats
- Better than regex for creative CVs
- Free tier available
- High accuracy

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/

# Run specific test
python -m pytest tests/test_parser.py -v

# With coverage
python -m pytest --cov=. tests/
```

### Frontend Tests

```bash
cd frontend/cv-parser-frontend

# Unit tests
ng test

# E2E tests
ng e2e
```

### Manual Testing

Sample CVs are provided in `tests/sample_cvs/`:

```bash
# Test with sample CV
curl -X POST http://localhost:5000/api/parse-cv \
  -F "file=@tests/sample_cvs/john_doe_cv.pdf"
```

## 🌐 Deployment

### Backend (Python/Flask)

#### Option 1: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create cv-parser-backend
heroku config:set COHERE_API_KEY=your_key
git push heroku main
```

#### Option 2: Docker

```bash
# Build image
docker build -t cv-parser-backend ./backend

# Run container
docker run -p 5000:5000 \
  -e COHERE_API_KEY=your_key \
  cv-parser-backend
```

#### Option 3: AWS Lambda + API Gateway

Use Zappa for serverless deployment:

```bash
pip install zappa
zappa init
zappa deploy
```

### Frontend (Angular)

#### Option 1: Netlify

```bash
# Build production
ng build --configuration production

# Deploy to Netlify
npm install -g netlify-cli
netlify deploy --prod --dir=dist/cv-parser-frontend
```

#### Option 2: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

#### Option 3: GitHub Pages

```bash
ng build --configuration production --base-href=/cv-parser-ai/
npx angular-cli-ghpages --dir=dist/cv-parser-frontend
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use Angular style guide for TypeScript
- Write tests for new features
- Update documentation
- Keep commits atomic and meaningful

### Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on our code of conduct.

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- Scanned PDFs without OCR won't extract text properly
- Some creative CV layouts may not parse perfectly
- Cohere free tier limited to 100 calls/month

## 🗺️ Roadmap

- [ ] Add OCR support for scanned PDFs
- [ ] Support for more file formats (RTF, HTML)
- [ ] Resume scoring and matching
- [ ] Skill gap analysis
- [ ] Multiple language support
- [ ] Database storage for applications
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Batch processing
- [ ] API rate limiting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [@yourusername](https://github.com/yourusername)

See also the list of [contributors](https://github.com/yourusername/cv-parser-ai/contributors) who participated in this project.

## 🙏 Acknowledgments

- [Cohere AI](https://cohere.com/) for the amazing LLM API
- [Flask](https://flask.palletsprojects.com/) community
- [Angular](https://angular.io/) team
- All contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cv-parser-ai/issues)


If you found this project helpful, please consider giving it a ⭐️!
