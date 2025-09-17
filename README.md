# Reddit Image Scraper

This project scrapes Reddit posts that contain images and saves them into JSON files. A small Flask web application lets you browse the latest results in a responsive grid and filter them. If you need an images-only export, use the `filter_images.py` helper script or request `/download-images-json` directly.

---

## What is included

- `scraper.py` - background worker that saves posts with images to `output/`.
- `display.py` - Flask server that renders the UI and exposes helper endpoints.
- `templates/` - HTML templates for the grid view and list view.

---

## Step-by-step guide for Windows 
Follow the steps in order. When you see text inside a gray box, it is a command you can copy and paste into Command Prompt.

### 0. How to copy and paste commands
- To copy from this document: place your cursor at the start of the command, hold the left mouse button, drag to the end, release, and press `Ctrl + C`.
- To paste into Command Prompt: click inside the Command Prompt window and either right-click the mouse or press `Ctrl + V`, then press `Enter`.

**Before you continue, turn on your Wi-Fi or wired internet connection. Python updates and dependency installs need an active connection.**

### 1. Install Python (one time only)
1. Open your browser and go to https://www.python.org/downloads/windows/
2. Click the latest Python 3 release (version 3.10 or newer) and download the 64-bit installer.
3. Run the installer. **Important:** on the first screen check the box that says `Add Python 3.x to PATH`, then click **Install Now**.
4. When the installation finishes, close the installer.
5. Confirm the install: press the Windows key, type `cmd`, press Enter, and run:
   ```
   python --version
   ```
   You should see a version number like `Python 3.11.6`.

### 2. Download and extract the project
1. Choose a location. For this guide we will use a folder on the Desktop.
2. On your Desktop, right-click an empty space, choose **New > Folder**, type `reddit-image-scrapper`, and press Enter.
3. Go to the project download page (GitHub or the location provided to you).
4. Click the green **Code** button and choose **Download ZIP**. The ZIP file usually appears in your **Downloads** folder (for example `reddit-image-scrapper-main.zip`).
5. Open File Explorer, browse to **Downloads**, right-click the ZIP, choose **Extract All...**, and when asked where to extract, click **Browse**, select the folder you created on the Desktop, and click **Extract**.
6. Open the extracted folder and confirm it contains files like `display.py`, `scraper.py`, `requirements.txt`, and the `templates` directory. Leave this File Explorer window open - we will refer to the exact path shortly.

#### Critical files and folders to keep together
Make sure everything listed below stays inside the same `reddit-image-scrapper` folder. Do not rename them.
- `display.py` - launches the web viewer. Must stay in the project root.
- `scraper.py` - handles scraping. Lives beside `display.py`.
- `filter_images.py` - helper script used when exporting images-only JSON.
- `templates/` - contains `index.html` and `list.html`. The folder name must remain `templates` so Flask can find the pages.
- `output/` - where JSON files are stored. Keep the folder; the app creates new files inside it.
- `requirements.txt` - list of Python packages needed during installation.
- `README.md`, `CHANGELOG.md`, and other documentation - optional but recommended to keep for reference.
If you move or rename any of these items, the program may not start or certain features will fail.

### 3. Open Command Prompt in the project folder
1. Press the Windows key, type `cmd`, and press Enter. A black Command Prompt window opens and usually shows `C:\Users\<YourName>`.
2. Change the directory to the project folder. If you followed the Desktop example, run:
   ```
   cd "%USERPROFILE%\Desktop\reddit-image-scrapper"
   ```
   After pressing Enter you should see the prompt change to `C:\Users\<YourName>\Desktop\reddit-image-scrapper>`.
3. Keep this window open. Every remaining command will be typed here.

### 4. Create a virtual environment
This creates an isolated Python environment stored in a folder called `venv`.
```
python -m venv venv
```
- If the command succeeds nothing else prints; check File Explorer to see a new `venv` folder.
- If you get an error saying Python is not recognized, return to step 1.

### 5. Activate the virtual environment
Activation ensures the correct Python interpreter and libraries are used. Copy the command below and paste it into Command Prompt:
```
venv\Scripts\activate
```
- The prompt now starts with `(venv)`. Example: `(venv) C:\Users\ASUS\Desktop\reddit-image-scrapper>`.
- If you see a message like "cannot be loaded because running scripts is disabled", copy and run:
  ```
  Set-ExecutionPolicy -Scope Process RemoteSigned
  ```
  When prompted, type `Y` and press Enter, then run the activate command again.

### 6. (Optional but recommended) Upgrade pip
```
python -m pip install --upgrade pip
```

### 7. Install project dependencies
```
pip install -r requirements.txt
```
- You will see progress bars such as `Collecting flask==3.0.0`. Wait until you see `Successfully installed ...` and the `(venv)` prompt returns.

### 8. Start the web viewer
Copy the command below and paste it into Command Prompt. Make sure `(venv)` appears to the left of the path before you run it.
```
python display.py
```
- The terminal prints several lines. When you see the line with `http://localhost:5000`, copy that address and paste it into your browser's address bar after the command finishes:
  ```
  Open http://localhost:5000
   * Serving Flask app 'display'
   * Debug mode: on
  ```
- Leave this Command Prompt window open. It keeps the web app running and shows the scraping progress messages you'll monitor in the next step.

### 9. Open the browser interface and verify the scrape
1. Open your web browser (Edge, Chrome, Firefox, etc.).
2. Click the address bar, erase any existing text, type `http://localhost:5000`, and press Enter.
3. The home page displays the most recent JSON file as image cards.
4. To scrape a new subreddit: fill in the **Subreddit** box (do not include `r/`), choose the number of **Pages**, and click **Scrape**. Switch back to the Command Prompt window that is running `python display.py` and watch the log lines. When you see a line like `[scrape] Finished r/malaysia pages=3`, return to your browser and reload `http://localhost:5000` to load the new data.
5. Click **List View** to browse the same data in a focussed grid. The filter box hides cards that do not match your text.
6. (Optional) Generate an images-only file with the helper script if you need a trimmed list of images:
   ```
   python filter_images.py output\<subreddit>_posts.json
   ```
   The script saves a matching `_images_only.json` file in the `output/` folder.
7. Confirm the scrape worked: open the `output` folder inside `reddit-image-scrapper`. A new file such as `<subreddit>_posts.json` should have a fresh timestamp. Double-click the file to inspect the raw JSON in Notepad if you are curious.

### 10. Stop the web app and deactivate the virtual environment
1. In the Command Prompt window running `python display.py`, press `Ctrl + C` (hold Control and press C). You will see `^C` and the prompt `(venv)` returns, indicating the server stopped.
2. Exit the virtual environment so future commands use your regular Python. Copy the command below, paste it into Command Prompt, and press Enter:
   ```
   deactivate
   ```
   After pressing Enter the `(venv)` prefix disappears. You can now close the Command Prompt window.

### 11. Running it again later
1. Open Command Prompt.
2. Change into the project folder (adjust the path if you saved it elsewhere):
   ```
   cd "%USERPROFILE%\Desktop\reddit-image-scrapper"
   ```
3. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Run the server:
   ```
   python display.py
   ```
You do not need to reinstall dependencies unless `requirements.txt` changes.

---

## Housekeeping and verification

- **Check the API quickly:** While the server is running, visit `http://localhost:5000/api/posts` to view the JSON output directly in your browser. This confirms the backend is serving data.
- **Keep the `output/` folder tidy:** Delete older JSON files manually from the `output` folder if you no longer need them. The newest scrape always loads automatically, so removing unused files keeps the dropdown lists short.
- **Back up important scrapes:** Copy the JSON files you want to keep to another folder before deleting or re-scraping.

---

## Step-by-step guide for macOS or Linux

1. Install Python 3. macOS users can run `brew install python@3.11` if Homebrew is installed. Linux users can use their package manager (for example `sudo apt install python3 python3-venv`).
2. Download and extract the ZIP to a location you prefer, e.g. `~/Downloads/reddit-image-scrapper`.
3. Open Terminal and run the following commands one by one (copy each line, paste with `Cmd + V` on macOS or `Ctrl + Shift + V` on Linux, then press Enter):
   ```
   cd ~/Downloads/reddit-image-scrapper
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   python display.py
   ```
4. Open your browser to `http://localhost:5000`.
5. When finished, return to Terminal, press `Ctrl + C` to stop the server, and run `deactivate` to leave the virtual environment.

---

## Frequently Asked Questions

- **Do I need a Reddit account or API key?** No. The scraper uses Reddit's public JSON endpoints. Private or quarantined subreddits will not return data.
- **Can I change where files are saved?** Yes. Open `display.py` and `scraper.py` and search for the `output` folder name if you want to point to a different directory. Make sure the folder exists before running.
- **How do I capture more than 50 pages?** The UI limits the value to 50 to respect Reddit's rate limits. If you truly need more, adjust the `max` attribute in `templates/index.html` or call `scraper.py` directly with a larger `num_pages`, but be mindful of Reddit's policies.
- **Nothing appears after scraping. What should I check?** Ensure the subreddit actually has recent image posts, verify your internet connection, watch the Command Prompt for error messages, and confirm the `output` folder has a newly updated JSON file.

---

## Optional: run the scraper by itself

If you want to run the scraper without the UI (for automation or scheduled tasks), activate the virtual environment and run:
```
python scraper.py
```
Adjust the constants at the bottom of `scraper.py` to change the subreddit or number of pages. Alternatively, import the class directly:
```
python - <<"PY"
from scraper import RedditScraper
s = RedditScraper("malaysia")
s.scrape(num_pages=3)
print(s.save_to_json("malaysia_posts.json"))
PY
```

---

## Troubleshooting tips

- `python` is not recognized: close Command Prompt, reopen it, or try using the `py` launcher by running `py --version`.
- `pip` cannot connect: ensure you are connected to the internet. Corporate networks may require proxy settings.
- Activation error on Windows: run `Set-ExecutionPolicy -Scope Process RemoteSigned` before activating the virtual environment.
- No posts appear: the subreddit might be private or have no recent images. Try a different subreddit or increase the page count.

---

## License

MIT

