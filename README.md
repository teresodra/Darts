

In optimisation problems, it is rarely realistic to assume that everything is deterministic.  
This repository presents a simple example of how uncertainty can be handled in optimisation: **a darts game**.

# Darts Strategy Optimiser

Playing darts with your friends and want to maximise your chances of winning? This repo is for you [see Disclaimer](#disclaimer).

### Finding your skill

Depending on how often you can hit the bullseye (together with double bullseye), you can choose a skill level:
- **Top-10 professional** → **~70%** of the time → skill in the game: 10 
- **Professional player** → **~42%** of the time → skill in the game: 15 
- **Amateur league player** → **~25%** of the time → skill in the game: 20 
- **Amateur / casual player** → **~10%** of the time → skill in the game: 35

### How to run

Given your score, number of turns you want to finish in, and your skill, the program computes the best aiming position.  
<p align="center">
  <a href="#how-to-run">
    <img src="https://img.shields.io/badge/Run-dartboard.py-green?style=for-the-badge" alt="Run dartboard.py">
  </a>
</p>

### Heatmap
First it displays a heatmap showing the probability of winning when aiming at each point on the dartboard,
![Heatmap of probabilities](images/heatmap.png)


### Interactive application
After closing the heatmap, an interactive application will pop up to guide you through your throws.
![Interactive dartboard](images/application.png)


## How to run

```bash
python dartboard.py


```

Playing darts with your friends and want to maximise your chances of winning? This repo is for you ([see Disclaimer](#disclaimer)).

...

#### Disclaimer

This repository is used only to illustrate the technology used to optimise under uncertanty. If you want a program for a more realistic scenario (i.e. having an oponent), please contact the owner of the repository.