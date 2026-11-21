# Filtros parecidos com os do CapCut (aproximações, testados 21/11)

Sempre partir do bruto 4K (scale=1080:1920:flags=lanczos).

- **Aprimorar**: `hqdn3d=1.5:1.5:4:4,unsharp=5:5:0.7:5:5:0.0,eq=contrast=1.05:saturation=1.10:gamma=1.03,colorbalance=rs=0.03:bs=-0.03`
- **4K**: `unsharp=7:7:1.1:5:5:0.0,cas=strength=0.6,eq=contrast=1.10:saturation=1.18:gamma=1.02`
- **Nostalgia**: `eq=saturation=0.82:contrast=0.95,curves=r='0/0.06 0.5/0.55 1/0.96':g='0/0.05 0.5/0.50 1/0.93':b='0/0.10 0.5/0.44 1/0.85',noise=alls=9:allf=t,vignette=PI/4.5`
- **Bokeh**: `scripts/bokeh.py entrada inicio duracao saida 34 0.72` (desfoque 34, fundo escurecido 0.72).
  Precisa: `pip install mediapipe`, `apt-get install -y libegl1 libgles2`, modelo
  storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
  Funciona melhor com fundo com detalhe (closet/vestiário); em parede lisa quase não muda.
