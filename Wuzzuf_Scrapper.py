import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, timedelta
from tkinter import Tk, Label, PhotoImage, HORIZONTAL, NORMAL, DISABLED
from tkinter import ttk
import os
window = Tk()
window.geometry("400x300")
window.resizable(False, False)
window.title("WUZZUF Scrapper App")
window.config(background="#F5F6F7")
icon = PhotoImage(file=r"C:\Mine\My Projects\Wuzzuf Scrapper\channels4_profile.png")
window.iconphoto(True, icon)
Label(window, text="WUZZUF", font=("Gotham Bold", 20, "bold"), fg="white", bg="#0155D9", pady=10).pack(fill="x")
Label(window, text="Browse Jobs:", font=("Arial", 12), fg="#2A394F", bg="#F5F6F7").pack(anchor="w", padx=20, pady=8)
job_txt_box = ttk.Entry(window, width=50, font=("Arial", 10))
job_txt_box.pack(ipady=3)
def start_scraping():
    global base_url
    job_text = job_txt_box.get().strip()
    if not job_text:
        print("Please enter a job title!")
    base_url = f"https://wuzzuf.net/search/jobs/?q={job_text}&a=hpb&start="
    print(f"Searching for: {job_text}")
    scrape_jobs(job_text)
def scrape_jobs(dream_job):
    job_title, company_name, location, date_posted, job_type = [], [], [], [], []
    job_status, years_of_experience, level, skills_required, job_link = [], [], [], [], []
    page = 0
    while True:
        url = base_url + str(page)
        response = requests.get(url)
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, "lxml")
        job_card = soup.find_all("div", class_ = "css-pkv5jc")
        total_jobs = int(soup.find("div", class_="css-9i2afk").find_next("div").find_next("strong").text)
        for job in job_card:
                job_title.append(job.h2.text)
                progress["value"] = (len(job_title) / total_jobs) * 100
                window.update_idletasks()
                company_name.append(job.find("div", class_ = "css-d7j1kk").a.text.replace(" -", "").strip())
                location.append(job.find("span", class_ ="css-5wys0k").text.strip())
                date_posted.append(job.find("div", class_ ="css-laomuu").find_next("span").find_next("div").text)
                job_type.append(job.find("span", class_ ="css-1ve4b75 eoyjyou0").text.strip())
                job_status.append(job.find("div", class_ ="css-1lh32fc").find_next("a").find_next("a").text.strip())
                level.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("div").find("a").text.strip())
                years_of_experience.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("span").find_next("div").find_next("span").text.replace("·", "").replace("Yrs of Exp",""))
                skills_required.append(job.find("div", class_ ="css-y4udm8").find_next("div").find_next("span").find_next("div").text)
                job_link.append(job.find("h2", class_ ="css-m604qf").find_next("a").get("href"))
        if not job_card:
            break
        page +=1
    status_label.config(text="The file is ready!")
    open_folder_button.config(state=NORMAL)
    window.update_idletasks()    
    print("SCRAPPING IS DONE!")
    df = pd.DataFrame({"job_title": job_title,"company_name": company_name,"location": location,"duration": date_posted,"job_type": job_type,
        "job_status": job_status,"level": level,"years_of_experience": years_of_experience,"skills_required": skills_required,"job_link": job_link
    })
    df[["num_days", "day_month", "ago"]]=df.duration.str.split(expand=True)
    df["num_days"] = df.num_days.astype(int)
    df["days"] = df.apply(lambda x: x["num_days"]*30 if x["day_month"] == "months" else x["num_days"], axis=1)
    df["month_posted"] = df.apply(lambda x: (datetime.today() - timedelta(days=x["days"])).strftime("%B"), axis=1)
    df.drop(columns=["num_days", "day_month", "ago", "days", "duration"], inplace=True)
    df[["exp_from", "exp_to"]]=df["years_of_experience"].str.split(" - ", expand=True)
    df["experience"] = df.apply(lambda x: (str(x.exp_from) + "-" + str(x.exp_to)).replace(" ", "") if len(x.exp_from) <= 4 else "Not specified", axis=1).map(lambda z: z.replace("-None", ""))
    df.drop(columns=["years_of_experience", "exp_from", "exp_to"], inplace=True)
    df["skills_required"] = df["skills_required"].map(lambda x: re.sub(r'^.*Yrs of Exp\s*·\s*', '', x))
    df["skills_required"] = df["skills_required"].str.split(" · ")
    df = df[["job_title", "job_type", "company_name", "location", "job_status","level", "experience", "month_posted", "skills_required", "job_link"]]
    global file_path
    file_path = fr"C:\Mine\Wuzzuf Jobs\Wuzzuf {dream_job} {datetime.today().strftime('%d-%m-%Y')}"
    os.makedirs(file_path, exist_ok=True)
    df.to_excel(os.path.join(file_path, f"Wuzzuf {dream_job.title()} {datetime.today().strftime('%d-%m-%Y')}.xlsx"), index=False, header=True)
progress = ttk.Progressbar(window, orient=HORIZONTAL, length=355, mode='determinate')
progress.pack(pady=10)
job_button = ttk.Button(window, text="Find", width=15, command=start_scraping)
job_button.pack(pady=8)
status_label = Label(window, text="", font=("Arial", 10), bg="#F5F6F7")
status_label.pack(pady=5)
open_folder_button = ttk.Button(window, state=DISABLED, text="Open Folder", command=lambda: os.startfile(file_path))
open_folder_button.pack(pady=10)
window.mainloop()