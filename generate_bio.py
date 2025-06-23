import os
import pdfplumber
import json
import re

def extract_resume_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    
    # Extract basic information
    name = re.search(r"^([A-Z][a-z]+ [A-Z][a-z]+)", text, re.MULTILINE)
    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.search(r"(\+?\d[\d\s-]{7,}\d)", text)
    
    # Extract experience (simplified)
    experience = []
    exp_pattern = r"(?P<title>[^\n]+)\n(?P<company>[^\n]+)\n(?P<dates>[^\n]+)\n(?P<location>[^\n]+)\n(?P<description>(?:\n.*)+?)(?=\n\n|\Z)"
    for match in re.finditer(exp_pattern, text, re.DOTALL):
        experience.append({
            "title": match.group("title").strip(),
            "company": match.group("company").strip(),
            "dates": match.group("dates").strip(),
            "location": match.group("location").strip(),
            "description": [line.strip() for line in match.group("description").split('\n') if line.strip()]
        })
    
    # Extract skills (simplified)
    skills = []
    if "SKILLS" in text or "TECHNICAL SKILLS" in text:
        skills_section = re.split(r"SKILLS|TECHNICAL SKILLS", text, flags=re.IGNORECASE)[1]
        skills_section = re.split(r"\n\n", skills_section)[0]
        skills = [skill.strip() for skill in re.split(r",|\n|•", skills_section) if skill.strip()]
    
    return {
        "name": name.group(1) if name else "Your Name",
        "email": email.group(0) if email else "your.email@example.com",
        "phone": phone.group(0) if phone else "+1234567890",
        "experience": experience,
        "skills": skills
    }

def generate_html(resume_data):
    # Generate HTML from template
    with open("template.html", "r") as f:
        template = f.read()
    
    # Replace placeholders with actual data
    html = template.replace("{{name}}", resume_data["name"])
                 .replace("{{email}}", resume_data["email"])
                 .replace("{{phone}}", resume_data["phone"])
                 .replace("{{skills}}", "\n".join(
                     f'<span class="skill-pill bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-4 py-2 rounded-full">{skill}</span>'
                     for skill in resume_data["skills"]
                 ))
    
    # Generate experience section
    experience_html = ""
    for exp in resume_data["experience"]:
        experience_html += f"""
        <div class="glass-card p-8 rounded-3xl shadow-xl relative mb-6">
            <h3 class="text-2xl font-bold mb-2">{exp['title']}</h3>
            <p class="text-primary font-medium mb-4">{exp['company']} | {exp['dates']} | {exp['location']}</p>
            <ul class="space-y-2">
                {''.join(f'<li class="flex items-start"><i class="fas fa-check-circle text-primary mt-1 mr-2"></i><span>{item}</span></li>' for item in exp['description'])}
            </ul>
        </div>
        """
    
    html = html.replace("{{experience}}", experience_html)
    return html

def main():
    print("""
    Bio Page Generator
    ------------------
    This script will generate a personal bio page from your resume PDF.
    """)
    
    pdf_path = input("Enter path to your resume PDF: ").strip('"')
    if not os.path.exists(pdf_path):
        print("Error: File not found")
        return
    
    print("Processing your resume...")
    resume_data = extract_resume_data(pdf_path)
    
    print("Generating HTML...")
    html = generate_html(resume_data)
    
    output_path = "index.html"
    with open(output_path, "w") as f:
        f.write(html)
    
    print(f"Success! Your bio page has been generated at {output_path}")
    print("Upload this file along with the assets folder to GitHub Pages or your hosting provider.")

if __name__ == "__main__":
    main()