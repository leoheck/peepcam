#!/bin/bash

# Script to make space removing old motion files (pictures/videos)

disk_usage_threshold="88"
motion_lib_path="/var/lib/motion/"

get_current_percentual_disk_usage()
{
	df -h / | egrep -o "[0-9]+%" | sed "s/%//g"
}

get_the_oldest_recording_folder()
{
	# Format
	# /var/lib/motion/[YEAR]/[MONTH]/[DAY]
	find "${motion_lib_path}" -mindepth 3 -type d | sort | head -1
}

# Compress data
compress_folder()
{
	folder_to_compress="${1}"
	echo "Compressing recordings ${folder_to_compress}"
}

# Backup data on monster
backup_data()
{
	folder_to_bkp="${1}"
	echo "Creating a bkp for ${folder_to_bkp}"
}

datetime=$(date +"%Y.%m.%d %Hh%M'%S")

echo -e "\n================================="
echo "${datetime}"
disk_usage=$(get_current_percentual_disk_usage)

while true;
do
	disk_usage=$(get_current_percentual_disk_usage)
	echo "Current disk usage is ${disk_usage}%"

	if [[ ${disk_usage} -ge ${disk_usage_threshold} ]]
	then
		oldest_recordings_day=$(get_the_oldest_recording_folder)

		#backup_data ${oldest_recordings_day}

		echo "Removing recordings from day ${oldest_recordings_day}"
		rm -rf ${oldest_recordings_day}

	else
		echo "Current disk usage under the threshold (${disk_usage_threshold}%)"
		break
	fi

	sleep 1
done

# echo "Cleanup routine done!"
