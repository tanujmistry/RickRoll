import cv2
import vlc

# Your video path
VIDEO_PATH = r"path.mp4"

# Load VLC
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(VIDEO_PATH)
player.set_media(media)

# Face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
                                    "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not found")
    exit()

print("Tracking attention... Press Q to quit")

last_state = None
player_started = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5)

    face_present = len(faces) > 0

    # Restart video if it ended (loop forever)
    if player_started and player.get_state() == vlc.State.Ended:
        player.stop()
        player.play()

    # Face detected → PAUSE
    if face_present:
        if last_state != "PAUSE" and player_started:
            print("👀 Focus detected → Pausing Rickroll")
            player.pause()
            last_state = "PAUSE"

    # No face → PLAY
    else:
        if last_state != "PLAY":
            print("😈 Distracted → Playing Rickroll")
            if not player_started:
                player.play()
                player_started = True
            else:
                player.set_pause(0)
            last_state = "PLAY"

    cv2.imshow("Attention Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
player.stop()
