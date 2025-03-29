# -*- coding: utf-8 -*-
import pywhatkit
import time
import csv
import sys
import random
import os  # <-- Import the 'os' module for path operations

# --- Configuration ---
CONTACTS_FILE = 'contacts.csv'
IMAGES_FOLDER = 'images'  # <-- Name of the subfolder containing images

# ** List of Sudanese Arabic Eid Message Templates (for caption) **
EID_MESSAGE_TEMPLATES = [
    # Message 1
    """سلام يا {name}! 👋
عيد سعيد وكل سنة وانت والأسرة الكريمة بألف خير وصحة وعافية. 😊
ينعاد علينا وعليكم بالخير واليمن والبركات إن شاء الله. 🌙✨
ربنا يتقبل صيامنا وقيامنا وصالح أعمالنا. 🙏""",

    # Message 2
    """أهلاً {name}! ✨
عيد مبارك عليك وعلى أحبابك. أسأل الله أن يملأ أيامكم فرح وسعادة. 🎉
كل عام وأنتم إلى الله أقرب. ينعاد عليكم بالصحة والسلامة.  Sudanese Arabic dialect""",

    # Message 3
    """{name}، يا هلا! 😃
بمناسبة عيد الفطر المبارك، أرسل ليك أحر التهاني وأطيب الأماني.
أتمنى ليك عيد مليان بهجة وسرور مع الأهل والأصدقاء. 🐑 <0xF0><0x9F><0xAA><0xB2>
ربنا يجعل كل أيامك أعياد. 🙏""",

    # Message 4
    """يا {name}! كل سنة وانت طيب وعيد مبارك! 🥳
فرحة العيد تكتمل بوجودكم يا غاليين. ربنا يديم المحبة والألفة بيناتنا.
أتمنى ليك ولعائلتك عيداً سعيداً ومستقبلاً مشرقاً بإذن الله. 🌟🌙""",

    # Message 5 (Slightly shorter)
    """{name} الغالي/ة، سلام! 💌
عيدكم مبارك وينعاد عليكم بالصحة والعافية والمسرات إن شاء الله.
تقبل الله طاعاتكم وكل عام وأنتم بخير. 😊✨""",

    # Add more message templates here if you wish!
]

# Delay between sending messages (in seconds) - Might need to be longer for images
DELAY_BETWEEN_MESSAGES = 15 # Increased delay recommended for image uploads

# Time pywhatkit waits before sending (after opening WhatsApp Web chat)
WAIT_TIME_BEFORE_SEND = 10 # Increased wait time is crucial for images

# Time pywhatkit waits before closing the tab (after sending)
CLOSE_TIME_AFTER_SEND = 10 # Give more time after potential upload
# --- End Configuration ---

def load_contacts(filename):
    """Loads contacts and image filenames from a CSV file (UTF-8)."""
    contacts = []
    line_number = 1
    required_columns = ['Name', 'PhoneNumber', 'ImageFile'] # <-- Added 'ImageFile'
    try:
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            # Check if all required columns exist
            if not all(col in reader.fieldnames for col in required_columns):
                 missing = [col for col in required_columns if col not in reader.fieldnames]
                 print(f"Error: CSV file '{filename}' is missing required column(s): {', '.join(missing)}")
                 sys.exit(1)

            for row in reader:
                line_number += 1
                name_val = row.get('Name')
                phone_val = row.get('PhoneNumber')
                image_file_val = row.get('ImageFile') # <-- Get image filename

                # Check for None or empty essential values
                if not name_val or not phone_val or not image_file_val:
                    print(f"Warning: Skipping row {line_number}. Missing essential data (Name, PhoneNumber, or ImageFile): {row}")
                    continue # Skip to the next row

                name = name_val.strip()
                phone = phone_val.strip()
                image_file = image_file_val.strip() # <-- Get image filename

                # Basic validation
                if name and phone.startswith('+') and phone[1:].isdigit() and image_file:
                    contacts.append({
                        'name': name,
                        'phone': phone,
                        'image': image_file # <-- Store image filename
                    })
                else:
                    reason = []
                    if not name: reason.append("Name is empty")
                    if not phone.startswith('+'): reason.append("Phone does not start with '+'")
                    if not phone[1:].isdigit(): reason.append("Phone contains non-digit characters after '+'")
                    if not phone: reason.append("Phone is empty")
                    if not image_file: reason.append("ImageFile is empty") # <-- Check image file
                    print(f"Warning: Skipping row {line_number}. Invalid data: {', '.join(reason)}. (Row: {row})")
        return contacts
    except FileNotFoundError:
        print(f"Error: Contacts file '{filename}' not found.")
        print("Please create the CSV file with 'Name', 'PhoneNumber', 'ImageFile' columns, saved as UTF-8.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading/processing the CSV file (around line {line_number}): {e}")
        print("Please check the CSV file format and ensure it's valid UTF-8.")
        sys.exit(1)

def send_whatsapp_image_with_caption(phone_number, image_path, caption):
    """Sends a WhatsApp image with caption using pywhatkit."""
    try:
        print(f"Attempting to send image '{os.path.basename(image_path)}' with caption to {phone_number}...")
        pywhatkit.sendwhats_image(
            receiver=phone_number,
            img_path=image_path,
            caption=caption,
            wait_time=WAIT_TIME_BEFORE_SEND, # Use configured wait time
            tab_close=False,              # Close tab after sending
            close_time=CLOSE_TIME_AFTER_SEND  # Use configured close time
        )
        print("Image and caption queued successfully!")
        # Optional small pause after queuing
        time.sleep(5)
        return True
    except Exception as e:
        # Provide more specific feedback if possible
        print(f"Error sending image to {phone_number}: {e}")
        if "Unable to Locate Assets" in str(e):
             print("-> Common Cause: WhatsApp Web UI might have changed. Try updating pywhatkit: pip install --upgrade pywhatkit")
        elif "Internet Not Connected" in str(e):
             print("-> Check your internet connection.")
        else:
            print("-> Possible issues: WhatsApp Web not logged in? Browser closed? Incorrect phone format? Focus lost? Image path incorrect?")
        return False

# --- Main Script ---
if __name__ == "__main__":
    print("Starting Sudanese Eid Mubarak WhatsApp Sender (Image + Random Caption)...")
    print("=" * 40)
    print("!! REQUIREMENTS !!")
    print(f"1. Ensure '{CONTACTS_FILE}' exists, is UTF-8 encoded, and has columns: Name, PhoneNumber, ImageFile.")
    print(f"2. Ensure a folder named '{IMAGES_FOLDER}' exists in the same directory as this script.")
    print(f"3. Place the image files listed in '{CONTACTS_FILE}' inside the '{IMAGES_FOLDER}' folder.")
    print("4. Ensure you are logged into WhatsApp Web in your default browser.")
    print("5. Keep your phone connected to the internet.")
    print("6. AVOID USING MOUSE/KEYBOARD while the script runs.")
    print("7. BE RESPONSIBLE: Sending too fast/bulk can lead to WhatsApp blocking.")
    print(f"8. Delay between messages: {DELAY_BETWEEN_MESSAGES}s | Wait time for load: {WAIT_TIME_BEFORE_SEND}s")
    print("=" * 40)

    input("Press Enter to start sending messages...")

    contacts = load_contacts(CONTACTS_FILE)

    if not contacts:
        print("No valid contacts found. Exiting.")
        sys.exit(0)
    if not EID_MESSAGE_TEMPLATES:
        print("Error: The EID_MESSAGE_TEMPLATES list is empty.")
        sys.exit(1)
    # Check if images folder exists
    if not os.path.isdir(IMAGES_FOLDER):
        print(f"Error: The image folder '{IMAGES_FOLDER}' was not found in this directory.")
        print("Please create it and place the images inside.")
        sys.exit(1)


    print(f"\nFound {len(contacts)} contacts.")
    successful_sends = 0
    failed_sends = 0

    for i, contact in enumerate(contacts):
        name = contact['name']
        phone = contact['phone']
        image_filename = contact['image'] # Get the image filename from contact data

        # *** Construct the full path to the image ***
        full_image_path = os.path.join(IMAGES_FOLDER, image_filename)

        # *** Check if the specific image file exists ***
        if not os.path.isfile(full_image_path):
            print("-" * 20)
            print(f"Contact {i+1}/{len(contacts)}")
            print(f"SKIPPING: Image file not found for {repr(name)} ({phone}).")
            print(f"Missing file: '{full_image_path}'")
            failed_sends += 1
            # Wait a short time even on skip
            time.sleep(DELAY_BETWEEN_MESSAGES // 4)
            continue # Move to the next contact

        # *** Randomly select and personalize a message template for the caption ***
        chosen_template = random.choice(EID_MESSAGE_TEMPLATES)
        personalized_caption = chosen_template.format(name=name)

        print("-" * 20)
        print(f"Contact {i+1}/{len(contacts)}")
        print(f"Sending to: {repr(name)} ({phone})")
        print(f"Image: '{image_filename}'")
        # print(f"Caption: {personalized_caption}") # Uncomment cautiously

        # *** Send the image with caption ***
        if send_whatsapp_image_with_caption(phone, full_image_path, personalized_caption):
            successful_sends += 1
            if i < len(contacts) - 1:
                 print(f"Waiting for {DELAY_BETWEEN_MESSAGES} seconds before next message...")
                 time.sleep(DELAY_BETWEEN_MESSAGES)
        else:
            failed_sends += 1
            # Wait after failure
            print(f"Waiting for {DELAY_BETWEEN_MESSAGES // 2} seconds after failure...")
            time.sleep(DELAY_BETWEEN_MESSAGES // 2)


    print("\n" + "=" * 30)
    print("Finished Sending Messages!")
    print(f"Successfully sent attempts: {successful_sends}")
    print(f"Failed/Skipped attempts: {failed_sends}")
    print("=" * 30)