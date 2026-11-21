"""Bokeh (fundo desfocado tipo modo retrato) em um trecho de vídeo.
uso: python bokeh.py entrada.mp4 inicio duracao saida.mp4 [forca_desfoque]
Recorte da pessoa com MediaPipe selfie_multiclass (fundo = classe 0), máscara suavizada no tempo
e nas bordas; fundo desfocado com blur gaussiano forte. Áudio copiado do trecho.
"""
import sys, subprocess, numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

src, ss, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
strength = float(sys.argv[5]) if len(sys.argv) > 5 else 22
MODEL = "/tmp/claude-0/-home-user-Claude/c9666f33-89ef-5d36-9a00-fdf48ae9d107/scratchpad/models/selfie_multiclass_256x256.tflite"
W, H, FPS = 1080, 1920, 30

seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODEL), running_mode=vision.RunningMode.VIDEO,
    output_confidence_masks=True, output_category_mask=False))

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", src,
                        "-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-ss", str(ss), "-t", str(dur), "-i", src, "-map", "0:v", "-map", "1:a?", "-shortest",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", out],
                       stdin=subprocess.PIPE)
prev, n = None, 0
k = int(strength) * 2 + 1
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    small = cv2.resize(fr, (540, 960), interpolation=cv2.INTER_AREA)
    res = seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small)), int(n * 1000 / FPS))
    person = 1.0 - res.confidence_masks[0].numpy_view().astype(np.float32)  # classe 0 = fundo
    person = cv2.resize(person, (W, H), interpolation=cv2.INTER_LINEAR)
    person = cv2.dilate(person, np.ones((9, 9), np.uint8))           # não comer cabelo/borda
    person = cv2.GaussianBlur(person, (31, 31), 0)                    # borda macia
    prev = person if prev is None else 0.55 * person + 0.45 * prev  # suaviza no tempo (sem tremer)
    m = np.clip(prev, 0, 1)[..., None]
    bg = cv2.GaussianBlur(fr, (k, k), 0)
    comp = (fr.astype(np.float32) * m + bg.astype(np.float32) * (1 - m)).astype(np.uint8)
    enc.stdin.write(comp.tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.wait()
print("ok", n, "quadros")
