To create tensorboard in google colab:

- %load_ext tensorboard
- %tensorboard --logdir ./PPO2_logs/

PPO2 model was trained with Stable Baselines 2.10.0: 
- Policy = 'MlpPolicy'
- Steps = 200k
- Learning Rate = 1e-4
- Gamma = 0.9
- All other parameters default
