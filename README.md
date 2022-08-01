# 🔥📈🔥 Scrape Data From 同花顺 🔥📈🔥


## Installation Guide 🏗️

Create the environment using
```bash
  conda env create -f environment.yml
```
Activate the environment 
```bash
  conda activate environmental
```

Or:
```bash
pip3 install requirements
```

## Usage/Examples 🧙
In terminal, we type   **crontab -e**   and copy code below in it (don't forget to replace **absolute_path** in the code below and in **业绩公告.py**):

```bash
* * * * * python3 /absolute_path/业绩公告.py
```
In my computer, these are:
```bash
* * * * * python3 /Users/jiahaozhang/Desktop/Scrape-Data-From-同花顺/业绩公告.py
```
Here, we scrap data every minute. 


Run code below in terminal to stop this task:
```bash
crontab -r
```
PS:
```
1:
If we download the data for the first time, we would like to change **download_first_time=True** in each .py file to download historical data.
If we just want to update data, we would like to change **download_first_time=False** in each .py file to just update data.

2:
To speed the code while updating data, just comment the parts we don't need.

```

## Authors
```bash
Yi-Yu Lin
Jiahao Zhang
```
