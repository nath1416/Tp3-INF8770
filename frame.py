import cv2

def main(video_path: str):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    saved_frames = []
    fast_step = 10  # Number of frames to skip when using fast navigation
    
    print(f"Total frames: {total_frames}")
    print("Controls:")
    print("  Left Arrow  - Previous frame")
    print("  Right Arrow - Next frame")
    print("  Page Up     - Jump 10 frames back")
    print("  Page Down   - Jump 10 frames forward")
    print("  Space       - Save current frame number")
    print("  Q / ESC     - Quit")
    
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        
        if not ret:
            print("Error reading frame")
            break
        
        # Display frame number on the image
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Frame: {current_frame}/{total_frames - 1}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display_frame, f"Saved: {saved_frames}", 
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        
        cv2.imshow("Video Frame Viewer", display_frame)
        
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('q') or key == 27:  # Q or ESC
            break
        elif key == 32:  # Space bar
            if current_frame not in saved_frames:
                saved_frames.append(current_frame)
                print(f"Saved frame: {current_frame}")
            else:
                print(f"Frame {current_frame} already saved")
        elif key == 81 or key == 2:  # Left arrow
            current_frame = max(0, current_frame - 1)
        elif key == 83 or key == 3:  # Right arrow
            current_frame = min(total_frames - 1, current_frame + 1)
        elif key == 85 or key == 0:  # Page Up
            current_frame = max(0, current_frame - fast_step)
        elif key == 86 or key == 1:  # Page Down
            current_frame = min(total_frames - 1, current_frame + fast_step)
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nSaved frame numbers: {saved_frames}")
    return saved_frames


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python frame.py <video_path>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    saved = main(video_path)
    print(saved)