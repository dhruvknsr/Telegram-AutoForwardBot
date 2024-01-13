# Import necessary modules
from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession
import asyncio


# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Print starting message
print("Starting...")

# Read configuration from environment variables
APP_ID = config("APP_ID", default=0, cast=int)
API_HASH = config("API_HASH", default=None, cast=str)
SESSION = config("SESSION", default="", cast=str)
FROM_ = config("FROM_CHANNEL", default="", cast=str)
TO_ = config("TO_CHANNEL", default="", cast=str)

BLOCKED_TEXTS = config("BLOCKED_TEXTS", default="", cast=lambda x: [i.strip().lower() for i in x.split(',')])
MEDIA_FORWARD_RESPONSE = config("MEDIA_FORWARD_RESPONSE", default="yes").lower()

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

YOUR_ADMIN_USER_ID = config("YOUR_ADMIN_USER_ID", default=0, cast=int)
BOT_API_KEY = config("BOT_API_KEY", default="", cast=str)

# Initialize Telethon client
try:
    steallootdealUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    steallootdealUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Global Sets
photo_id = set() #photo_id
photo_set = [] #photos
event_counter = [] #events
group_id = set() #groups of messages
messages = []
num_photos = 0
event_text = ''

async def count_event(event):
    event_counter.append(event)
    if(event.grouped_id != None):
        group_id.add(event.grouped_id)
    
    #print(event)
    print(f"Event count : {len(event_counter)}")
    return len(event_counter)

async def count_photo(event):
        global photo_id, photo_set  
        if event.media:

            photo_id_value = event.media.photo.id

            if photo_id_value not in photo_id:
                photo_id.add(photo_id_value)
                photo_set.append(event)
                print(f"Photo count: {len(photo_id)}")
            else:
                print("Photo already exists in the set.")
        
        elif event.message and event.message.photo:
            photo_id_value = event.message.photo.id
            if photo_id_value not in photo_id:
                photo_id.add(photo_id_value)
                photo_set.append(event)
                print(f"Photo count: {len(photo_id)}")
            else:
                print("Photo ID already exists in the set.")
        else:
            print("No MessageMediaPhoto object or photo found in the event.")
        return len(photo_id)

async def flush_data():
    global num_photos, event_text
    await asyncio.sleep(3)  # Wait for 3 seconds
    print("Flushing data...")
    photo_id.clear()
    event_counter.clear()
    group_id.clear()
    num_photos = 0
    print("Flush Complete")

# Read REPLACE_DICT from environment variables [@dhruvknsr]
replace_dict_str = config("REPLACE_DICT", default="", cast=str)
replace_dict_items = [item.split(':') for item in replace_dict_str.split(',') if item]
replace_dict = {replace_text : replace_with for replace_text, replace_with in replace_dict_items}

# Replacement for Case Insensitive Function [@dhruvknsr]
def replace_case_insensitive(original, pattern, replacement):
    index = original.lower().find(pattern.lower())
    if index != -1:
        return original[:index] + replacement + original[index + len(pattern):]
    return original
print("REPLACE_DICT:", replace_dict)

async def process_text_with_replacements(original_text):
    processed_text = original_text

    # Check for blocked texts
    if any(blocked_text.lower() in original_text.lower() for blocked_text in BLOCKED_TEXTS):
        print(f"Blocked message containing one of the specified texts: {original_text}")
        logging.warning(f"Blocked message containing one of the specified texts: {original_text}")
        return  # Or return an indicator that the text is blocked

    for replace_text, replace_with in replace_dict.items():
        if replace_text.lower() in processed_text.lower():
            processed_text = replace_case_insensitive(processed_text, replace_text, replace_with)
            print(f"Text after replacement: {processed_text}")

    return processed_text

    

@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    global num_photos
    try:
        for i in TO:
            num_events = await count_event(event)

            await asyncio.sleep(1)

            if event.media is None:
                print("Event has no media.")
                num_photos = 0

            for event in event_counter:
                if event.media:
                    num_photos = await count_photo(event)

            media_files = []
            original_message_text = event.raw_text
            message_text = original_message_text

            message_text = await process_text_with_replacements(message_text)

            if message_text is not None:
                if(num_photos < 2):
                    #print text
                    if num_photos == 0:
                        #original_message_text = event.raw_text
                        #message_text = original_message_text
                        await steallootdealUser.send_message(i, message_text)
                        print(f"Forwarded text message to channel {i}")
                        await flush_data()

                    elif num_photos == 1:

                        if event.media:
                            user_response = MEDIA_FORWARD_RESPONSE
                            if user_response != 'yes':
                                print(f"Media forwarding skipped by user for message: {event.raw_text}")
                                return
                        # print text and photo
                        #media_files = []
                        #original_message_text = event.raw_text
                        #message_text = original_message_text
                        media_files.append(event.media)
                        await steallootdealUser.send_message(i, message_text, file=event.media)
                        print(f"Forwarded media message to channel {i}")
                        await flush_data()
                    # print album
                elif num_photos >= 2:
                    continue
            else:
                print("Message Blocked")

    
    except Exception as e:
        print(e)
        await flush_data()

@steallootdealUser.on(events.Album(chats=FROM))
async def album_handler(event):
    for i in TO:
        try:
            # Create a new album
            received_photos = []
            event_text = '' 

            # Copy images and messages from the incoming album to the new album
            for msg in event.messages:
                if msg.photo:
                    received_photos.append(msg.photo)               
            event_text = await process_text_with_replacements(event.text)
            # Send the new album to the specified destination chat
            if received_photos and event_text is not None:
                await steallootdealUser.send_file(i, received_photos, caption=event_text)
                print("Album Sent")
                await flush_data()
        except Exception as e:
            print(f"Error handling album: {e}")
    

# Run the bot
print("Bot has started.")
steallootdealUser.run_until_disconnected()