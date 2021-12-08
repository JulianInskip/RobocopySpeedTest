from datetime import datetime
import os
import socket
import sys

# TODO: Bring robocopy into python script


def hms_string(sec_elapsed):
    """
    Formated the elapsed time based on an integer of an elapsed time
    :param sec_elapsed: Elapsed time in seconds
    :return: Formatted elapsed time string
    """
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    h_suffix = "hours"
    m_suffix = "minutes"
    s_suffix = "seconds"
    if h == 1:
        h_suffix = "hour"
    if m == 1:
        m_suffix = "minute"
    if s == 1:
        s_suffix = "second"
    if h == 0 and m == 0 and (s != 0 or s == 0):
        return "{:>2.0f} {}".format(s, s_suffix)
    elif h == 0 and m != 0 and s == 0:
        return "{:>2} {}".format(m, m_suffix)
    elif h == 0 and m != 0 and s != 0:
        return "{:>2} {}; {:>2.0f} {}".format(m, m_suffix, s, s_suffix)
    elif h != 0 and m == 0 and s == 0:
        return "{:>2} {}".format(h, h_suffix)
    elif h != 0 and m != 0 and s != 0:
        return "{:>2} {}; {:>2} {}; {:>2.0f} {}".format(h, h_suffix, m, m_suffix, s, s_suffix)


def transfer_log_info(in_argv):
    bat_file_name = in_argv[1]
    log_file_name = in_argv[2]
    csv_file_name = os.path.join(os.path.dirname(log_file_name), bat_file_name.split("_")[0] + ".csv")
    hostname = socket.gethostname()
    print(f"Transferring logs for {bat_file_name}")
    print(f"Transferring logs for {log_file_name}")
    print(f"Transferring logs for {csv_file_name}")
    print(f"Hostname: {hostname}")

    date_time_obj = datetime.strftime(datetime.strptime(log_file_name[-19:-4], "%Y%m%d_%H%M%S"), "%d/%m/%Y %H:%M:%S")
    date_obj = datetime.strftime(datetime.strptime(log_file_name[-19:-4], "%Y%m%d_%H%M%S"), "%d/%m/%Y")
    time_obj = datetime.strftime(datetime.strptime(log_file_name[-19:-4], "%Y%m%d_%H%M%S"), "%H:%M:%S")

    src_dir = ""
    dst_dir = ""
    no_of_dirs = ""
    no_of_files = ""
    files_copied = ""
    total_secs = ""
    total_time_format = ""
    mb_per_sec = ""
    file_text_count = 0
    with open(log_file_name, "r") as log_file:
        lines = log_file.readlines()
        lines = [line.rstrip() for line in lines]
        for log_row in lines:
            if "Source :" in log_row:
                src_dir = log_row.replace("Source :", "").strip()
                print(f"Source directory: {src_dir}")
            elif "Dest :" in log_row:
                dst_dir = log_row.replace("Dest :", "").strip()
                print(f"Target directory: {dst_dir}")
            elif "Files :" in log_row:
                if file_text_count == 0:
                    files_copied_ = list(filter(None, log_row.replace("Files :", "").split(" ")))
                    if len(files_copied_) == 0:
                        files_copied = "All files in folder"
                    else:
                        files_copied = files_copied_[0]
                    file_text_count += 1
                    print(f"Files copied: {files_copied}")
                elif file_text_count == 1:
                    no_of_files = list(filter(None, log_row.replace("Files :", "").split(" ")))[0]
                    file_text_count += 1
                    print(f"No. of files: {no_of_files}")
            elif "Dirs :" in log_row:
                no_of_dirs = list(filter(None, log_row.replace("Dirs :", "").split(" ")))[0]
                print(f"No. of directories: {no_of_dirs}")
            elif "Bytes :" in log_row:
                copy_size = list(filter(None, log_row.replace("Bytes :", "").split(" ")))[0]
                copy_units_ = list(filter(None, log_row.replace("Bytes :", "").split(" ")))[1]
                if copy_units_.lower() == "m":
                    copy_units = "MB"
                elif copy_units_.lower() == "g":
                    copy_units = "GB"
                else:
                    copy_units == "Unknown"
                print(f"File size: {copy_size}")
                print(f"File size units: {copy_units}")
            elif "Times :" in log_row:
                times = list(filter(None, log_row.replace("Times :", "").split(" ")))[0]
                hours = int(times.split(":")[0])
                mins = int(times.split(":")[1])
                secs = int(times.split(":")[2])
                hours_in_secs = hours * 60 * 60
                mins_in_secs = mins * 60
                total_secs = hours_in_secs + mins_in_secs + secs
                total_time_format = hms_string(total_secs).strip()
                print(f"Total Elapsed time = {total_time_format}")
            elif "MegaBytes/min" in log_row:
                mb_per_sec = float(log_row.replace("Speed :", "").replace("MegaBytes/min.", ""))
                print(f"{mb_per_sec} MegaBytes/min")
    with open(csv_file_name, "a") as csv_file:
        csv_file.write(f"\"{hostname}\",\"{bat_file_name}\",\"{log_file_name}\",\"{date_time_obj}\",\"{date_obj}\",\"{time_obj}\",\"{src_dir}\",\"{dst_dir}\",\"{files_copied}\",\"{no_of_dirs}\",\"{no_of_files}\",\"{copy_size}\",\"{copy_units}\",\"{total_secs}\",\"{total_time_format}\",\"{mb_per_sec}\"\n")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        print(sys.argv)
        transfer_log_info(sys.argv)
    else:
        print("-- Usage:")
        fmt = "python %s <log file name>"
        print(fmt % (sys.argv[0]))

        transfer_log_info(["Robocopy_logToCSV.py", r"RobocopySpeedTest_MultiFiles.bat", r"logs\RobocopySpeedTest_MultiFiles_log_20211203_141903.log"])
