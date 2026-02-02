# NoGAN Video Colorization — Technical Notes (Cluster)

This README documents the exact technical workflow used to:
1) prepare short video clips, and  
2) colorize them locally/on a cluster GPU using **DeOldify**, saving outputs to a fixed folder.

---



Create + activate:

```bash
conda create -n deoldify python=3.8 -y
conda activate deoldify



ffmpeg # clip extraction, f.e. ffmpeg -ss 00:10:00 -i input.mp4 -t 20 -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 128k clip_001.mp4



# after:

git clone -q https://github.com/jantic/DeOldify.git
cd /content/DeOldify
pip -q install -r requirements.txt


curl -L -o models/ColorizeVideo_gen.pth https://data.deepai.org/deoldify/ColorizeVideo_gen.pth # load model

# by having problems, run:
conda install -c conda-forge *missing modul* -y



