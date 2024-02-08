# Instroduction
This is the re-implement of The project called Video2Music
Source: https://github.com/AMAAI-Lab/Video2Music

# Installation
```php
apt-get update
git clone https://github.com/Phan-Trung-Thuan/Video2Music-testing
cd Video2Music-testing
pip install -r requirements.txt
```
# Execution
You can run separately python files for several purposes. Note that some files require GPU for better performance.
```php
cd Video2Music-testing
python <running-file>.py
```
Files that need GPU to execute:
* emotion_extraction.py
* semantic_extraction.py
The rest of python files do not require GPU