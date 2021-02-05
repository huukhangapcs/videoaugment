from fastapi import FastAPI, UploadFile, File, requests
from fastapi.responses import FileResponse, RedirectResponse
import cv2
app = FastAPI()


@app.get("/")
async def main():
    return {"Hello": "World!"}

def process_video(filename):
    cap = cv2.VideoCapture(filename)
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # write the flipped frame
            out.write(frame)
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()

@app.post("/video_upload")
async def upload_video(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("mp4", "wav")
    if not extension:
        return "Video must in mp4 or wav format!"
#     process_video(file.filename)
    return FileResponse(file.filename, media_type="video/mp4")

    
