import os
import json
from flask import Flask, request, render_template, jsonify
from groq import Groq
import PyPDF2
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def analyze_resume(resume_text, job_role=""):
    job_context = f"for the role of {job_role}" if job_role else "for a general job application"

    prompt = f"""You are an expert HR consultant and resume coach. Analyze the following resume {job_context}.

Resume:
{resume_text}

Provide a detailed analysis in the following JSON format ONLY (no extra text):
{{
  "score": <number 0-100>,
  "summary": "<2-3 sentence overall summary>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
  "suggestions": ["<actionable suggestion 1>", "<actionable suggestion 2>", "<actionable suggestion 3>"],
  "missing_sections": ["<missing section 1 if any>"],
  "keywords": ["<key skill/keyword found 1>", "<key skill 2>", "<key skill 3>", "<key skill 4>", "<key skill 5>"],
  "ats_score": <number 0-100>,
  "experience_level": "<Fresher / Junior / Mid-level / Senior>"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.choices[0].message.content.strip()
    # Clean up if model wraps in markdown
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    return json.loads(response_text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_role = request.form.get("job_role", "")

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    try:
        file_bytes = file.read()
        resume_text = extract_text_from_pdf(file_bytes)

        if not resume_text or len(resume_text) < 50:
            return jsonify({"error": "Could not extract text from PDF. Make sure it's not a scanned image."}), 400

        result = analyze_resume(resume_text, job_role)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == "__main__":
    print("🚀 Resume Analyzer running at http://localhost:5000")
    app.run(debug=True)