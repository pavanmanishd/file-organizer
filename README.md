# File Organizer
## Description
- This is a simple python script that organizes files in a directory into folders based on their file extension.
- bash script to run the python script is also included.
- bash script will run when it detects a file change in the directory.

## Requirements
- Python 3
- Bash
- Work on Linux (Not tested on Windows or Mac)

## Usage
- Clone the repository
- Change the directory to your desired directory in the directories.json file
- Run the bash script
- To run once
```bash
./test.sh
```
- To run in the background
```bash
./test.sh &
```
The script will run in the background and will organize the files in the directory when there is a file change.
