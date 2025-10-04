import { Component } from '@angular/core';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

interface PersonalInfo {
  fullName: string;
  email: string;
  phone: string;
}

interface Education {
  degree: string;
  institution: string;
  year: string;
}

interface Experience {
  title: string;
  company: string;
  period: string;
}

interface ParsedCV {
  personalInfo: PersonalInfo;
  education: Education[];
  experience: Experience[];
  skills: string[];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  selectedFile: File | null = null;
  isDragging = false;
  isUploading = false;
  uploadProgress = 0;
  errorMessage = '';
  successMessage = '';
  skillsText = '';

  formData: ParsedCV = {
    personalInfo: {
      fullName: '',
      email: '',
      phone: ''
    },
    education: [{ degree: '', institution: '', year: '' }],
    experience: [{ title: '', company: '', period: '' }],
    skills: []
  };

  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.selectedFile = files[0];
      this.errorMessage = '';
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.errorMessage = '';
    }
  }

  uploadAndParse() {
    if (!this.selectedFile) return;

    this.isUploading = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.uploadProgress = 0;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<any>(`${this.apiUrl}/parse-cv`, formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round(100 * event.loaded / event.total);
        } else if (event.type === HttpEventType.Response) {
          if (event.body.success) {
            this.autofillForm(event.body.data);
            this.successMessage = 'CV parsed successfully! Form has been auto-filled.';
            this.uploadProgress = 100;
          }
        }
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Failed to parse CV. Please try again.';
        this.isUploading = false;
        this.uploadProgress = 0;
      },
      complete: () => {
        this.isUploading = false;
        setTimeout(() => this.uploadProgress = 0, 2000);
      }
    });
  }

  autofillForm(data: ParsedCV) {
    this.formData.personalInfo = { ...data.personalInfo };

    if (data.education && data.education.length > 0) {
      this.formData.education = data.education.map(edu => ({ ...edu }));
    }

    if (data.experience && data.experience.length > 0) {
      this.formData.experience = data.experience.map(exp => ({ ...exp }));
    }

    if (data.skills && data.skills.length > 0) {
      this.formData.skills = [...data.skills];
      this.skillsText = data.skills.join(', ');
    }
  }

  addEducation() {
    this.formData.education.push({ degree: '', institution: '', year: '' });
  }

  removeEducation(index: number) {
    this.formData.education.splice(index, 1);
  }

  addExperience() {
    this.formData.experience.push({ title: '', company: '', period: '' });
  }

  removeExperience(index: number) {
    this.formData.experience.splice(index, 1);
  }

  removeSkill(skill: string) {
      this.formData.skills = this.formData.skills.filter(s => s !== skill);
      this.skillsText = this.formData.skills.join(', ');
    }

  submitApplication() {
      // Sync skills from text area
      if (this.skillsText) {
        this.formData.skills = this.skillsText
          .split(',')
          .map(s => s.trim())
          .filter(s => s.length > 0);
      }

      console.log('Application submitted:', this.formData);
      alert('Application submitted successfully!');
  }
}