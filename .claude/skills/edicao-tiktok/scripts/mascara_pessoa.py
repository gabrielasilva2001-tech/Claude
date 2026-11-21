import sys, subprocess, numpy as np, mediapipe as mp, cv2
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
src, a, b, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
W,H=1080,1920
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=mpt.BaseOptions(model_asset_path=sys.argv[5]), output_confidence_masks=True))
rd = subprocess.Popen(["ffmpeg","-v","error","-ss",str(a),"-to",str(b),"-i",src,"-vf","fps=30","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","gray","-s",f"{W}x{H}","-r","30","-i","-","-c:v","ffv1",out],stdin=subprocess.PIPE)
n=0; prev=None
while True:
    buf = rd.stdout.read(W*H*3)
    if len(buf) < W*H*3: break
    fr = np.frombuffer(buf,np.uint8).reshape(H,W,3)
    r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(fr)))
    bg = r.confidence_masks[0].numpy_view()
    m = np.clip(1.0-bg,0,1)
    m = cv2.resize(m,(W,H),interpolation=cv2.INTER_LINEAR)
    m = cv2.GaussianBlur(m,(0,0),2.5)
    if prev is not None: m = 0.6*m+0.4*prev
    prev=m
    wr.stdin.write((m*255).astype(np.uint8).tobytes()); n+=1
wr.stdin.close(); wr.wait(); print("frames",n)
