# NavRep

![varch](media/varch.gif)

This repository contains two main modules:
- NavRepSim, a simulator aimed at allowing anyone to easy reproduce and improve on the state-of-the-art of RL for robot navigation.
- NavRep, a suite for unsupervised-learning-assisted RL for robot navigation. It contains tools, datasets, models which allow you to easily reproduce findings from our paper.

## Pre-requisites
Python 3.6

For example, on Ubuntu 20

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.6 python3.6-dev
sudo apt-get install -y virtualenv python3-virtualenv
```

We recommend creating a virtualenv:

```
virtualenv ~/navrepvenv --python=python3.6
source ~/navrepvenv/bin/activate
```

rospy:

```
pip install --extra-index-url https://rospypi.github.io/simple/ rospy rosbag tf tf2_ros
```

## Install

Installing navrep is as simple as

```
pip install navrep
```

## NavRepSim

### NavRep training environment

![trainenv](media/trainenv.gif)

### NavRep testing environment

![testenv1](media/testenv1.gif)
![testenv2](media/testenv2.gif)
![testenv3](media/testenv3.gif)

### SOADRL

![soadrlenv](media/soadrlenv.gif)

### CrowdMove

![crowdmoveenv1](media/crowdmoveenv1.gif)

![crowdmoveenv2](media/crowdmoveenv2.png)
![crowdmoveenv3](media/crowdmoveenv3.png)
![crowdmoveenv4](media/crowdmoveenv4.png)
![crowdmoveenv5](media/crowdmoveenv5.png)
![crowdmoveenv6](media/crowdmoveenv6.png)

### Pfeiffer

![markenv1](media/markenv1.gif)
![markenv2](media/markenv2.gif)


## NavRep

### make a V dataset

```
python -m navrep.scripts.make_vae_dataset --environment navreptrain --render
```

(remove `--render` argument to speed up data generation)

### train V

```
python -m navrep.scripts.train_vae --environment navreptrain
```

### train M

```
python -m navrep.scripts.make_rnn_dataset --environment navreptrain
python -m navrep.scripts.train_rnn --environment navreptrain
```

### Play encoded environment

```
python navrep.scripts.play_navreptrainencodedenv --backend VAE_LSTM --encoding V_ONLY
```

### Play dream environment

### Train C

```
python navrep.scripts.train_gym_navreptrainencodedenv --backend VAE_LSTM --encoding V_ONLY
```

### Test C

```
python navrep.scripts.cross_test_navreptrain_in_ianenv --backend VAE_LSTM --encoding V_ONLY --render
```

![traj](media/traj_gpt.png)

### Run in ROS node

```
roslaunch launch/sim_and_navrep.launch
```

## NavRep Variants

| **Environments**            | **Modular V, M**                  | **Joint V+M**                    | **Transformer V+M**              |
| --------------------------- | --------------------------------- | --------------------------------- | --------------------------------- |
| NavRep train                | :heavy_check_mark:                | :heavy_check_mark:                | :heavy_check_mark:                |
| NavRep test                 | :heavy_check_mark:                | :heavy_check_mark:                | :heavy_check_mark:                |
| SOADRL                      | :heavy_check_mark:                | :heavy_check_mark:                | :heavy_check_mark:                |
| Pfeiffer                    | :heavy_check_mark:                | :heavy_check_mark:                | :heavy_check_mark:                |
| CrowdMove                   | :heavy_minus_sign:                | :heavy_minus_sign:                | :heavy_minus_sign:                |


## Credits

This library was written primarily by Daniel Dugas. The transformer block codes, and vae/lstm code were taken or heavily derived from world models and karpathy's mingpt. We've retained the copyright headers for the relevant files.
