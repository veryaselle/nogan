# NoGAN Video Colorization — Technical Notes (Cluster)

This README documents the exact technical workflow used to:
1) prepare short video clips, and  
2) colorize them locally/on a cluster GPU using **DeOldify**, saving outputs to a fixed folder.

---



Create + activate:

```bash
conda create -n deoldify python=3.8 -y
conda activate deoldify



# nogan
