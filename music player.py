import speech_recognition as sr
from googleapiclient.discovery import build
import webbrowser

# Set your API key here
api_key = 'AIzaSyCsRIwAnpgBPADtzBhrpMPCPiI_ZhyThjQ'

def search_and_play_song(song_name, youtube):
    query = song_name + " official audio"
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1,
        type='video'
    ).execute()

    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Playing {song_name}...")
        webbrowser.open(video_url)
    else:
        print("Song not found.")

def main():
    recognizer = sr.Recognizer()
    youtube = build('youtube', 'v3', developerKey=api_key)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=100)

            recognized_text = recognizer.recognize_google(audio, language="en").lower()

            print("You said:", recognized_text)

            if recognized_text.startswith("play"):
                song_name = recognized_text.replace("play", "").strip()
                print(f"Searching for: {song_name} on YouTube...")
                search_and_play_song(song_name, youtube)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Error occurred; {0}".format(e))
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
