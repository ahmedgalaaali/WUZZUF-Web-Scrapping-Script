# WUZZUF-Web-Scrapping-Script
Web scraping is a very powerful choise when it comes to data collection. It automates repetitive tasks, saves time and effort as well. So, when it comes to web scraping and data cleaning automation, Python can take over all of these tasks. It has so many capabilities to just do what you need after defining a script and then the same task will be performed with a button click! To see or download the code navigate to [Wuzzuf_Scrapper](https://github.com/ahmedgalaaali/WUZZUF-Web-Scrapping-Script/blob/main/Wuzzuf_Scrapper.py) file.

**In this project I used many libraries to do the job such as:**
- **requests**: Requests the web page.
- **BeautifulSoup**: Navigates to the needed website, scrape the data after identifying `HTML` elements.
- **Pandas**: Cleans, organises the data, creates a data frame and saves it into an Excel file.
- **os**: Responsible for files and folders management on the system.
- **Tkinter**: Creates a simple GUI that makes it easier than just typing the needed *job* into the terminal.

## Main idea
The main idea of scraping multiple web pages is using an actual web **url** and then putting this **url** inside a `while` loop which keeps scraping and collecting the data until there's no more data to collect, at that point, it **breaks**.
```python
base_url = f"https://wuzzuf.net/search/jobs/?q={job_text}&a=hpb&start="
while True:
  url = base_url + str(page)
  response = requests.get(url)
  if response.status_code != 200:
    break
```
This lie of code `if response.status_code != 200:` is responsible for identifying were to stop, this means that whenever the web response is `200`, the `while` loop keeps working.

There's also a line of code that will be extremely important in page navigation, we must have identified a variable `page=0`, at the end of the `while` loop, we put a `page+=0` to make sure that every time the loop reaches this point it starts over again with a new value of the page to be added to the link.

## Scraping Part
This part contains a `for` loop inside a `while` loop. It's responsible for grapping each element and append it to a `list`, which will later be a part of the data frame we create.
```python
    job_title, company_name, location, date_posted, job_type = [], [], [], [], []
    job_status, years_of_experience, level, skills_required, job_link = [], [], [], [], []
    #...LOOK THE FILE FOR MORE...
        for job in job_card:
                job_title.append(job.h2.text)
                progress["value"] = (len(job_title) / total_jobs) * 100
                window.update_idletasks()
                company_name.append(job.find("div", class_ = "css-d7j1kk").a.text.replace(" -", "").strip())
                #...TO THE END OF THE LOOP...
```

## Data Cleaning
Here pandas would be a great choce in terms of cleaning, organizing the data and putting it into a data frame called `df` and then exporting it as an excel file:
```python
df = pd.DataFrame({"job_title": job_title,"company_name": company_name,"location": location,"duration": date_posted,"job_type": job_type,
        "job_status": job_status,"level": level,"years_of_experience": years_of_experience,"skills_required": skills_required,"job_link": job_link
    })
    df[["num_days", "day_month", "ago"]]=df.duration.str.split(expand=True)
    df["num_days"] = df.num_days.astype(int)
    df["days"] = df.apply(lambda x: x["num_days"]*30 if x["day_month"] == "months" else x["num_days"], axis=1)
    df["month_posted"] = df.apply(lambda x: (datetime.today() - timedelta(days=x["days"])).strftime("%B"), axis=1)
    df.drop(columns=["num_days", "day_month", "ago", "days", "duration"], inplace=True)
    #...TO THE END OF THE CLEANING...
```

## Files and Folders Manipulation
By using `os` library, and after each scraping attempt, this scrript can create a folder that contains a file that carries a path inside the created folder as siple as this:
```python
    global file_path
    file_path = fr"C:\Mine\Wuzzuf Jobs\Wuzzuf {dream_job} {datetime.today().strftime('%d-%m-%Y')}"
    os.makedirs(file_path, exist_ok=True)
    df.to_excel(os.path.join(file_path, f"Wuzzuf {dream_job.title()} {datetime.today().strftime('%d-%m-%Y')}.xlsx"), index=False, header=True)
```
>**Note:** In Python, we use `global` to say that a variable that exists in a loop or in a pre-defined function (`def`) can be used anywhere else in the script.

## GUI Creating
Is mentioned, I used `Tkinter` library to create a GUI that makes is mush easier to do our search and folder navigation without using the terminal, `Tkinter` codes can be found in:
```python
window = Tk()
window.geometry("400x300")
window.resizable(False, False)
window.title("WUZZUF Scrapper App")
window.config(background="#F5F6F7")
#...LOOK THE FILE FOR MORE...
status_label.config(text="The file is ready!")
open_folder_button.config(state=NORMAL)
window.update_idletasks()
#...LOOK THE FILE FOR MEORE...
progress = ttk.Progressbar(window, orient=HORIZONTAL, length=355, mode='determinate')
progress.pack(pady=10)
job_button = ttk.Button(window, text="Find", width=15, command=start_scraping)
job_button.pack(pady=8)
status_label = Label(window, text="", font=("Arial", 10), bg="#F5F6F7")
status_label.pack(pady=5)
open_folder_button = ttk.Button(window, state=DISABLED, text="Open Folder", command=lambda: os.startfile(file_path))
open_folder_button.pack(pady=10)
window.mainloop()
```
And here's the final look of the GUI:

![image](https://github.com/user-attachments/assets/ca051a47-e7a3-4008-ba10-25d9416f42f5)

## Conclusion
- This is an example of data collection and cleaning automation using Python, it can save a lot of time and effort with just some lines of code and websites available APIs.
- This program creates a well organised Excel file with these columns:
  - job_title
  - job_type
  - company_name
  - location
  - job_status
  - level
  - experience
  - month_posted
  - skills_required
  - job_link
