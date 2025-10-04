from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import PyPDF2
import docx
import io
import cohere
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize Cohere client
# Set your API key as environment variable: export COHERE_API_KEY='your-key-here'
COHERE_API_KEY = ''
cohere_client = cohere.Client(COHERE_API_KEY) if COHERE_API_KEY else None

class CVParserWithCohere:
    def __init__(self, text):
        self.text = text
        self.lines = text.split('\n')
        self.use_cohere = cohere_client is not None
        
    def extract_with_cohere(self):
        """Use Cohere LLM for intelligent entity extraction"""
        if not self.use_cohere:
            return None
            
        try:
            prompt = f"""You are a CV/Resume parser. Extract the following information from the CV text below and return ONLY a valid JSON object with no additional text or explanation.

CV Text:
{self.text}  # Limit text to avoid token limits

Extract and return JSON in this exact format:
{{
  "personalInfo": {{
    "fullName": "extracted full name",
    "email": "extracted email",
    "phone": "extracted phone number"
  }},
  "education": [
    {{
      "degree": "degree name",
      "institution": "university/college name",
      "year": "graduation year"
    }}
  ],
  "experience": [
    {{
      "title": "job title",
      "company": "company name",
      "period": "start year - end year or Present"
    }}
  ],
  "skills": ["skill1", "skill2", "skill3"]
}}

Rules:
- Extract up to 3 education entries
- Extract up to 3 work experiences
- Extract up to 15 relevant technical skills
- If information is not found, use empty string ""
- Return ONLY valid JSON, no markdown formatting, no explanations"""

            response = cohere_client.chat(
                model="command-a-03-2025",
                message=prompt,
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            print(f"Cohere response: {response_text}")  # Log first 200 chars
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            parsed_data = json.loads(response_text)
            
            # Validate structure
            if 'personalInfo' in parsed_data and 'education' in parsed_data:
                return parsed_data
            else:
                print("Invalid JSON structure from Cohere")
                return None
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {response_text[:200]}")
            return None
        except Exception as e:
            print(f"Cohere extraction error: {e}")
            return None
    
    def extract_email(self):
        """Fallback: Extract email address using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, self.text)
        return match.group(0) if match else ""
    
    def extract_phone(self):
        """Fallback: Extract phone number using regex"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}'
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, self.text)
            if match:
                return match.group(0)
        return ""
    
    def extract_name(self):
        """Fallback: Extract name from first lines"""
        for line in self.lines:
            line = line.strip()
            if line and len(line) > 2 and not '@' in line:
                name = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof)\.?\s*', '', line, flags=re.IGNORECASE)
                if 2 <= len(name.split()) <= 4:
                    return name
        return ""
    
    def extract_education_fallback(self):
        """Fallback: Extract education using regex"""
        education = []
        degree_keywords = ['bachelor', 'master', 'phd', 'b.s', 'm.s', 'b.a', 'm.a', 
                          'degree', 'diploma', 'university', 'college', 'institute']
        
        for i, line in enumerate(self.lines):
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in degree_keywords):
                degree = line.strip()
                
                year = ""
                for j in range(max(0, i-2), min(len(self.lines), i+3)):
                    year_match = re.search(r'\b(19|20)\d{2}\b', self.lines[j])
                    if year_match:
                        year = year_match.group(0)
                        break
                
                institution = ""
                for j in range(max(0, i-1), min(len(self.lines), i+2)):
                    if any(word in self.lines[j].lower() for word in ['university', 'college', 'institute']):
                        institution = self.lines[j].strip()
                        break
                
                education.append({
                    'degree': degree,
                    'institution': institution,
                    'year': year
                })
        
        return education[:3]
    
    def extract_experience_fallback(self):
        """Fallback: Extract experience using regex"""
        experiences = []
        
        job_patterns = [
            r'\b(Senior|Junior|Lead|Chief)?\s*(Software|Data|Web|Mobile|Full[- ]?Stack)?\s*(Engineer|Developer|Architect|Analyst|Manager|Director|Designer)\b',
            r'\b(Project Manager|Product Manager|Team Lead|CEO|CTO|CFO|VP)\b'
        ]
        
        for i, line in enumerate(self.lines):
            for pattern in job_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    title = line.strip()
                    
                    company = ""
                    for j in [i+1, i-1, i+2]:
                        if 0 <= j < len(self.lines):
                            potential_company = self.lines[j].strip()
                            if potential_company and len(potential_company) > 2:
                                company = potential_company
                                break
                    
                    date_range = ""
                    for j in range(max(0, i-2), min(len(self.lines), i+4)):
                        date_match = re.search(r'\b(19|20)\d{2}\s*[-–—]\s*((19|20)\d{2}|Present|Current)\b', 
                                              self.lines[j], re.IGNORECASE)
                        if date_match:
                            date_range = date_match.group(0)
                            break
                    
                    experiences.append({
                        'title': title,
                        'company': company,
                        'period': date_range
                    })
                    break
        
        return experiences[:3]
    
    def extract_skills_fallback(self):
        """Fallback: Extract skills using keyword matching"""
        skills = []
        
        tech_keywords = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
            'SQL', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'Git', 'CI/CD', 'Agile', 'Scrum', 'REST', 'GraphQL',
            'TensorFlow', 'PyTorch', 'Machine Learning', 'Data Science', 'DevOps'
        ]
        
        text_lower = self.text.lower()
        for skill in tech_keywords:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        return skills[:15]
    
    def parse(self):
        """Parse CV using Cohere LLM with fallback to regex"""
        # Try Cohere first
        if self.use_cohere:
            print("Using Cohere LLM for parsing...")
            cohere_result = self.extract_with_cohere()
            
            if cohere_result:
                # Validate and clean Cohere results
                result = {
                    'personalInfo': cohere_result.get('personalInfo', {}),
                    'education': cohere_result.get('education', []),
                    'experience': cohere_result.get('experience', []),
                    'skills': cohere_result.get('skills', [])
                }
                
                # Fill in missing personal info with regex fallbacks
                if not result['personalInfo'].get('email'):
                    result['personalInfo']['email'] = self.extract_email()
                if not result['personalInfo'].get('phone'):
                    result['personalInfo']['phone'] = self.extract_phone()
                if not result['personalInfo'].get('fullName'):
                    result['personalInfo']['fullName'] = self.extract_name()
                
                # Ensure we have at least one education/experience entry
                if not result['education']:
                    result['education'] = [{'degree': '', 'institution': '', 'year': ''}]
                if not result['experience']:
                    result['experience'] = [{'title': '', 'company': '', 'period': ''}]
                
                print("Successfully parsed with Cohere")
                return result
            else:
                print("Cohere parsing failed, using fallback...")
        else:
            print("Cohere not available, using regex fallback...")
        
        # Fallback to regex-based parsing
        return {
            'personalInfo': {
                'fullName': self.extract_name(),
                'email': self.extract_email(),
                'phone': self.extract_phone()
            },
            'education': self.extract_education_fallback() or [{'degree': '', 'institution': '', 'year': ''}],
            'experience': self.extract_experience_fallback() or [{'title': '', 'company': '', 'period': ''}],
            'skills': self.extract_skills_fallback()
        }

def extract_text_from_pdf(file_stream):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file_stream):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_stream)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

@app.route('/api/parse-cv', methods=['POST'])
def parse_cv():
    """Endpoint to parse CV/resume"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get file extension
        filename = file.filename.lower()
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(io.BytesIO(file.read()))
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(io.BytesIO(file.read()))
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return jsonify({'error': 'Unsupported file format. Please upload PDF, DOCX, or TXT'}), 400
        
        # Parse the CV with Cohere
        parser = CVParserWithCohere(text)
        parsed_data = parser.parse()
        
        return jsonify({
            'success': True,
            'data': parsed_data,
            'method': 'cohere' if parser.use_cohere and cohere_client else 'regex'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'cohere_available': cohere_client is not None
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration status"""
    return jsonify({
        'cohere_configured': COHERE_API_KEY != '',
        'cohere_available': cohere_client is not None
    })

if __name__ == '__main__':
    if not COHERE_API_KEY:
        print("\n" + "="*70)
        print("⚠️  WARNING: COHERE_API_KEY not set!")
        print("="*70)
        print("The parser will use regex fallback methods.")
        print("\nTo enable Cohere LLM parsing:")
        print("1. Get API key from: https://dashboard.cohere.com/api-keys")
        print("2. Set environment variable:")
        print("   export COHERE_API_KEY='your-key-here'")
        print("3. Restart the server")
        print("="*70 + "\n")
    else:
        print("\n✅ Cohere API key configured - Using LLM parsing\n")
    
    app.run(debug=True, port=5000)