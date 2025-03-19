- Python 3.x
- Required libraries: `tkinter`, `spacy`, `docx`, `PyPDF2`


1. Install Python 3.x if not already installed.
2. Install required dependencies using:
   ```
   pip install spacy python-docx PyPDF2
   ```
3. Download the English language model for spaCy:
   ```
   python -m spacy download en_core_web_sm
   ```

1. Run the application:
   ```
   python main.py
   ```
2. Select either "Employer" or "Job Seeker" mode.
3. Upload the required files:
   - Employers must upload a job listing first, then a resume.
   - Job seekers must upload a resume first, then a job listing.
4. The application will analyze the files and display skill matching results.
5. Employers can view a list of potential hires based on skill matching.


- `main.py`: Launches the GUI.
- `gui.py`: Contains the graphical user interface.
- `resume_analyzer.py`: Handles text extraction, skill analysis, and file processing.


This project is open-source and can be modified as needed by anyone.
