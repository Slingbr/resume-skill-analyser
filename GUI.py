import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from resume_analyser import POTENTIAL_HIRES_PATH, analyze_job_and_resume


class ResumeAnalyserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Analyzer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        

        self.root.configure(bg="#f7f7f7")

        self.mode = tk.StringVar(value="employer")


        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="AI Resume Analyzer", font=("Helvetica", 24, "bold"), bg="#f7f7f7", fg="#4a4a4a")
        title_label.pack(pady=20)

        
        mode_frame = tk.Frame(self.root, bg="#f7f7f7")
        mode_label = tk.Label(mode_frame, text="Select Mode:", font=("Helvetica", 14), bg="#f7f7f7", fg="#4a4a4a")
        mode_label.pack(side=tk.LEFT, padx=5)
        
        employer_button = tk.Radiobutton(mode_frame, text="Employer", variable=self.mode, value="employer", font=("Helvetica", 12), bg="#f7f7f7")
        employer_button.pack(side=tk.LEFT, padx=5)
        
        job_seeker_button = tk.Radiobutton(mode_frame, text="Job Seeker", variable=self.mode, value="job_seeker", font=("Helvetica", 12), bg="#f7f7f7")
        job_seeker_button.pack(side=tk.LEFT, padx=5)

        mode_frame.pack(pady=10)

       
        upload_button = tk.Button(self.root, text="Upload Job/Resume", command=self.upload_files, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="raised")
        upload_button.pack(pady=20, ipadx=20, ipady=10)

        
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f7f7f7", fg="#4a4a4a")
        self.result_label.pack(pady=20)

        
        self.potential_hires_button = tk.Button(self.root, text="View Potential Hires", command=self.view_potential_hires, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="raised")
        self.potential_hires_button.pack(pady=20, ipadx=20, ipady=10)

    def upload_files(self):
        # Asking for files based on mode
        if self.mode.get() == "employer":
            job_file_path = filedialog.askopenfilename(title="Select Job Listing", filetypes=[("All Files", "*.*")])
            if not job_file_path:
                return
            job_file = open(job_file_path, "rb")
            resume_file_path = filedialog.askopenfilename(title="Select Resume", filetypes=[("All Files", "*.*")])
            if not resume_file_path:
                return
            resume_file = open(resume_file_path, "rb")
        else:  # Job Seeker Mode
            #asking the user  job listing file 
            job_file_path = filedialog.askopenfilename(title="Select Job Listing", filetypes=[("All Files", "*.*")])
            if not job_file_path:
                messagebox.showwarning("Warning", "Please upload the job listing file first.")
                return
            
            # After job listing upload resume file
            resume_file_path = filedialog.askopenfilename(title="Select Resume", filetypes=[("All Files", "*.*")])
            if not resume_file_path:
                messagebox.showwarning("Warning", "Please upload your resume.")
                return
            
        
            job_file = open(job_file_path, "rb")
            resume_file = open(resume_file_path, "rb")

  
        try:
            missing_skills, extra_skills, match_percentage, is_potential_hire = analyze_job_and_resume(job_file, resume_file)

            if self.mode.get() == "employer":
                if is_potential_hire:
                    result_message = f"Potential Hire! Applicant's resume matches {match_percentage:.2f}% of the job listing skills."
                else:
                    result_message = f"Applicant's resume matches {match_percentage:.2f}% of the job listing skills."
            else: 
                result_message = f"Your resume matches {match_percentage:.2f}% of the job listing skills.\n\nMissing Skills: {', '.join(missing_skills)}"

            self.result_label.config(text=result_message)

        except Exception as e:
            messagebox.showerror("Error", f"Error analyzing files: {e}")
        finally:
            job_file.close() if job_file else None
            resume_file.close()

    def view_potential_hires(self):
        try:
            with open(POTENTIAL_HIRES_PATH, "r") as file:
                potential_hires = file.readlines()

            if potential_hires:
                hire_list = "".join([f"{i+1}. {line.strip()}\n" for i, line in enumerate(potential_hires)])
                messagebox.showinfo("Potential Hires", hire_list)
            else:
                messagebox.showinfo("Potential Hires", "No potential hires yet.")
        except FileNotFoundError:
            messagebox.showinfo("Potential Hires", "No potential hires yet.")
