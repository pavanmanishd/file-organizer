# bash script to check for file changes in downloads folder

#!/bin/bash

sudo apt install inotify-tools jq

json_file="./directories.json"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq not found. Please install jq to continue."
    exit 1
fi

# Check if the JSON file exists
if [ ! -f "$json_file" ]; then
    echo "JSON file not found: $json_file"
    exit 1
fi

# Read and parse JSON data
json_data=$(jq '.' "$json_file")

WATCH_FOLDER=$(echo "$json_data" | jq -r '.watch_dir')

# Run the python script once before starting the inotifywait loop to organize any existing files
python3 "${PWD}/fileOrganizer.py"

# Monitor the Downloads folder for create and modify events
inotifywait -m -r -e create -e modify "$WATCH_FOLDER" |
while read path action file; do
    # .org.chromium.Chromium.* files are created when downloading files in Chrome
    # If the file is a .org.chromium.Chromium.* file, wait for 2 seconds and then check again
    if [[ $file == *.org.chromium.Chromium.* ]]; then
        echo "chromium file"
        sleep 2
    elif [[ $file == *.crdownload ]]; then
        # if it is a .crdownload file, wait for 2 seconds and then check again
        echo "crdownload file"
        sleep 2
    else
        echo "normal file"
        python3 "${PWD}/fileOrganizer.py"
    fi

    # This loop will execute whenever a file is created or modified in the Downloads folder
    # You can add your custom actions here, such as copying or processing the file
    echo "Detected event: $action on file: $file"
done
