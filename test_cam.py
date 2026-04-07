import cv2

print("Attempting to connect to webcam...")
# Trying the default Windows driver first
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

if not cap.isOpened():
    print("❌ ERROR: Windows physically blocked access to the camera.")
else:
    print("✅ Camera connection opened! Attempting to pull a frame...")
    success, frame = cap.read()
    
    if success:
        print("🎉 SUCCESS! The camera works. Showing frame for 3 seconds...")
        cv2.imshow('Test', frame)
        cv2.waitKey(3000)
    else:
        print("❌ ERROR: Connected to camera, but the lens is returning pure black/empty frames.")

cap.release()
cv2.destroyAllWindows()