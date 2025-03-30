# Automated WhatsApp Eid Greetings Sender

## Description

This Python script automates the process of sending personalized Eid Mubarak greetings via WhatsApp Web. It reads contact information and corresponding image filenames from a CSV file, selects a random greeting message from a predefined list (customized with the contact's name), and sends both the specific image and the personalized caption to each contact.

This script utilizes the `pywhatkit` library, which automates browser interactions with WhatsApp Web.

**Note:** This project uses unofficial methods to interact with WhatsApp Web. Use it responsibly and be aware of WhatsApp's Terms of Service regarding automation. Excessive use might lead to temporary or permanent blocking of your WhatsApp number.

## Features

- Reads contact details (Name, Phone Number) from a `contacts.csv` file.
- Reads the specific image filename associated with each contact from the CSV.
- Supports personalization using the contact's name in messages.
- Selects randomly from a list of predefined Eid greeting messages (written in Sudanese Arabic in the example).
- Sends a unique, pre-defined image to each contact.
- Sends the randomly selected message as a caption with the image.
- Uses `pywhatkit` to automate sending via WhatsApp Web.
- Configurable delays between messages and wait times for loading.
- Handles UTF-8 encoding for names and messages (important for Arabic script).

## Technology Stack

- Python 3.x
- Libraries:
  - `pywhatkit`
  - `pyautogui` (usually installed as a dependency of `pywhatkit`)
  - `pywin32` (Required on **Windows** for clipboard operations used by `pywhatkit` for images)
  - `random` (Standard library)
  - `csv` (Standard library)
  - `os` (Standard library)
  - `sys` (Standard library)

## Prerequisites

1.  **Python 3:** Make sure you have Python 3 installed.
2.  **WhatsApp Account:** A functioning WhatsApp account.
3.  **Web Browser:** A standard web browser (like Chrome, Firefox, Edge). `pywhatkit` usually opens the default system browser.
4.  **WhatsApp Web Session:** You need to be logged into WhatsApp Web (`web.whatsapp.com`) in the browser the script will use _before_ running the script.
5.  **Phone Connectivity:** Your phone must remain unlocked and connected to the internet while the script is running.
6.  **Required Python Libraries:** Install the necessary packages using pip:
    ```bash
    pip install pywhatkit pyautogui
    # On Windows, you ALSO need pywin32:
    pip install pywin32
    ```
    _(Note: If you encounter permission errors, try running your terminal/command prompt as Administrator on Windows or use `pip install --user ...`)_

## File Structure

Your project directory should look like this:

your_project_folder/
├── your_script_name.py # The main Python script (e.g., send_eid_wishes.py)
├── contacts.csv # CSV file containing contact information
└── images/ # Folder containing all the images to be sent
├── image_for_contact1.jpg
├── image_for_contact2.png
└── ... (other image files)

## Configuration

Before running, you might need to adjust settings within the Python script (`your_script_name.py`):

1.  **`CONTACTS_FILE = 'contacts.csv'`:** Ensure this matches the name of your CSV file.
2.  **`IMAGES_FOLDER = 'images'`:** Ensure this matches the name of your images directory.
3.  **`EID_MESSAGE_TEMPLATES = [...]`:** Modify, add, or remove message templates in this list. Ensure each template uses `{name}` for personalization. Ensure correct UTF-8 encoding if using non-ASCII characters.
4.  **Timing Delays (Crucial):**
    - `DELAY_BETWEEN_MESSAGES`: Seconds to wait _between_ sending messages to different contacts. **Increase** if script fails on subsequent contacts or if you want to be safer regarding WhatsApp limits.
    - `WAIT_TIME_BEFORE_SEND`: Seconds `pywhatkit` waits _after_ opening the chat/image dialog before typing/sending. **Increase** significantly if messages/images aren't sending reliably (e.g., caption typed but not sent, image upload fails).
    - `CLOSE_TIME_AFTER_SEND`: Seconds `pywhatkit` waits _after_ sending before trying to close the tab. Increase slightly if tabs seem to close too early.

## Preparing the `contacts.csv` File

1.  Create a file named `contacts.csv`.
2.  **Encoding:** Save the file with **UTF-8 encoding**, especially if using Arabic names.
3.  **Columns:** The file **must** contain the following columns with these exact headers:
    - `Name`: The name of the contact for personalization (e.g., `أحمد علي`).
    - `PhoneNumber`: The full phone number including the country code with a `+` sign and no spaces/symbols (e.g., `+249123456789`).
    - `ImageFile`: The exact filename (including extension like `.png` or `.jpg`) of the image file located in the `images` folder for this contact (e.g., `ahmed_eid.png`).
4.  **Example Row:**
    ```csv
    Name,PhoneNumber,ImageFile
    ابو الشعور,+249xxxxxxxxxx,abu_shurooq.png
    بركيتة,+249yyyyyyyyy,barkita.jpg
    ```

## Usage

1.  **Prepare Files:** Ensure your `contacts.csv` file is ready and correctly formatted (UTF-8) and that all corresponding images are placed in the `images` folder.
2.  **Configure Script:** Adjust message templates and delays in the `.py` script if needed.
3.  **Log in to WhatsApp Web:** Open your browser and log in to `web.whatsapp.com`. Keep this tab/window open.
4.  **Run the Script:** Open your terminal or command prompt, navigate to the project directory, and run the script:
    ```bash
    python your_script_name.py
    ```
5.  **Follow Prompts:** The script will print initial information and wait for you to press Enter.
6.  **Monitor:** Watch the script execution. It will open new browser tabs for each message/image. **Avoid using your mouse or keyboard** while the script is actively interacting with the browser, as it can interfere with `pyautogui`.
7.  **Completion:** The script will print a summary of successful and failed attempts when finished.

## Important Considerations & Warnings

- **WhatsApp Terms of Service:** Automated messaging can violate WhatsApp's ToS. Use this script responsibly, avoid sending to unknown contacts or spamming, and use significant delays between messages to minimize the risk of getting blocked.
- **Reliability:** This script depends on the structure of the WhatsApp Web interface. If WhatsApp updates its website, the script (especially `pywhatkit`'s interaction) might break and require updates to the library or the script logic. This is **not** an official WhatsApp API.
- **Timing is Key:** Sending images requires more time than text. You will likely need to experiment with the `WAIT_TIME_BEFORE_SEND` and `DELAY_BETWEEN_MESSAGES` values to find what works reliably on your system and network connection. Start with larger values.
- **Error Handling:** Basic error handling is included, but unexpected issues can occur. Check the terminal output for error messages.
- **Testing:** Always test with 1-2 contacts (perhaps your own number) before running on a large list.
- **UTF-8 Encoding:** Ensure both the script (`.py`) and the `contacts.csv` file are saved with UTF-8 encoding to handle special characters (like Arabic) correctly.

## Troubleshooting Common Issues

- **`ModuleNotFoundError: No module named 'win32clipboard'` (Windows Only):** You need to install `pywin32`. Run `pip install pywin32`.
- **Script sends only to the first contact and stops:** Usually a timing issue or an error after the first send.
  - Drastically increase `DELAY_BETWEEN_MESSAGES` and `WAIT_TIME_BEFORE_SEND`.
  - Set `tab_close=False` in the `send_whatsapp_image_with_caption` function for debugging to see what happens on the second attempt.
  - Check the terminal for _any_ error messages after the first successful send.
- **Image/Caption is prepared but not sent:**
  - Increase `WAIT_TIME_BEFORE_SEND` significantly.
  - Ensure the browser window running WhatsApp Web remains focused (don't click elsewhere while it's trying to send).
  - Increase `CLOSE_TIME_AFTER_SEND`.
- **Image not found error / Skipping contact due to missing file:**
  - Verify the `IMAGES_FOLDER` name in the script matches the actual folder name.
  - Double-check that the filenames in the `ImageFile` column of `contacts.csv` exactly match the filenames (including extensions) in the `images` folder. Check for typos and case sensitivity issues.
- **Errors reading CSV (`AttributeError: 'NoneType'`, `KeyError`, etc.):**
  - Check `contacts.csv` for blank rows (especially at the end).
  - Ensure all required columns (`Name`, `PhoneNumber`, `ImageFile`) exist with the correct headers.
  - Make sure no essential cells are completely empty in a way that causes issues.
  - Verify the file is saved as UTF-8.

## License

(Optional - Add a license if you wish, e.g., MIT)
