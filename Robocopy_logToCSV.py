from datetime import datetime
from subprocess import call
import shutil
import os
import socket
import sys
import time

# DONE: Bring robocopy into python script
# DONE: Add timing for copying file/directories
# DONE: Add timing for deleting file/directories
# DONE: Create new logs directory if it does not exist
# DONE: Create new csv file if it does not exist
# DONE: Ensure script can run using python 2.x


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


def transfer_log_info(log_file_name, in_copy_type, in_cleanup_time):
    hostname = socket.gethostname()
    print("Transferring logs for {}".format(log_file_name))
    print("Hostname: {}".format(hostname))

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
                print("  Source directory: {}".format(src_dir))
            elif "Dest :" in log_row:
                dst_dir = log_row.replace("Dest :", "").strip()
                print("  Target directory: {}".format(dst_dir))
            elif "Files :" in log_row:
                if file_text_count == 0:
                    files_copied_ = list(filter(None, log_row.replace("Files :", "").split(" ")))
                    if len(files_copied_) == 0:
                        files_copied = "All files in folder"
                    else:
                        files_copied = files_copied_[0]
                    file_text_count += 1
                    print("  Files copied: {}".format(files_copied))
                elif file_text_count == 1:
                    no_of_files = list(filter(None, log_row.replace("Files :", "").split(" ")))[0]
                    file_text_count += 1
                    print("  No. of files: {}".format(no_of_files))
            elif "Dirs :" in log_row:
                no_of_dirs = int(list(filter(None, log_row.replace("Dirs :", "").split(" ")))[0])-1
                print("  No. of directories: {}".format(no_of_dirs))
            elif "Bytes :" in log_row:
                copy_size = list(filter(None, log_row.replace("Bytes :", "").split(" ")))[0]
                copy_units_ = list(filter(None, log_row.replace("Bytes :", "").split(" ")))[1]
                if copy_units_.lower() == "m":
                    copy_units = "MB"
                elif copy_units_.lower() == "g":
                    copy_units = "GB"
                else:
                    copy_units = "Unknown"
                print("  File size: {}".format(copy_size))
                print("  File size units: {}".format(copy_units))
            elif "Times :" in log_row:
                times = list(filter(None, log_row.replace("Times :", "").split(" ")))[0]
                hours = int(times.split(":")[0])
                mins = int(times.split(":")[1])
                secs = int(times.split(":")[2])
                hours_in_secs = hours * 60 * 60
                mins_in_secs = mins * 60
                total_secs = hours_in_secs + mins_in_secs + secs
                total_time_format = hms_string(total_secs).strip()
                print("  Total Elapsed time = {}".format(total_time_format))
            elif "MegaBytes/min" in log_row:
                mb_per_sec = float(log_row.replace("Speed :", "").replace("MegaBytes/min.", ""))
                print("  {} MegaBytes/min".format(mb_per_sec))
    with open(csv_log_file, "a") as csv_file:
        csv_file.write("\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\","
                       "\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\"\n".format(
                            hostname, in_copy_type, log_file_name, date_time_obj,
                            date_obj, time_obj, src_dir, dst_dir, files_copied,
                            no_of_dirs, no_of_files, copy_size, copy_units, total_secs,
                            total_time_format, mb_per_sec, in_cleanup_time, hms_string(in_cleanup_time)))


def run_robocopy():
    print("Running Robocopy speed test...")
    for config in config_list:
        from_dir = config[0]
        from_file = config[1]
        print("\n##########################################\nCopying {}".format(from_dir))
        if from_file == "":
            logfile = r"{}\{}_{}_log_{}.log".format(log_file_path, script_name, "multiple", time_now)
            copy_type = "Multiple Files"
            call(
                ["robocopy", from_dir, copy_to_dir, "/S", "/E", "/IS", "/IT", "/NP", "/NFL", "/LOG:{}".format(logfile)])
        else:
            logfile = r"{}\{}_{}_log_{}.log".format(log_file_path, script_name, "single", time_now)
            copy_type = "Single File"
            call(["robocopy", from_dir, copy_to_dir, from_file, "/IS", "/IT", "/NP", "/NFL", "/LOG:{}".format(logfile)])
        cleanup_time = cleanup(from_dir, from_file)
        transfer_log_info(logfile, copy_type, cleanup_time)


def cleanup(in_from_dir, in_from_file):
    print("Cleaning up copied files...")
    start_time_cleanup = time.time()
    # if in_from_file != "":
    #     file_path = os.path.join(to_dir, in_from_file)
    #     print("Removing {}".format(file_path))
    #     if os.path.isfile(file_path):
    #         print("Deleting {} file".format(file_path))
    #         os.remove(file_path)
    # else:
    #     src_file_list = []
    #     for dirname, dirnames, filenames in os.walk(in_from_dir):
    #         if dirname != in_from_dir:
    #             src_file_list.append(dirname)
    #         for filename in filenames:
    #             src_file_list.append(os.path.join(dirname, filename))
    #     new_file_list = [a.replace(in_from_dir, to_dir) for a in src_file_list]
    #     for new_file in new_file_list:
    #         # print("Checking {} file".format(new_file))
    #         if os.path.isdir(new_file):
    #             print("  Deleting {} directory".format(new_file))
    #             shutil.rmtree(new_file)
    #         elif os.path.isfile(new_file):
    #             print("  Deleting {} file".format(new_file))
    #             os.remove(new_file)
    #
    #     print()

    if os.path.isdir(copy_to_dir):
        print("  Deleting {} directory".format(copy_to_dir))
        shutil.rmtree(copy_to_dir)

    end_time_cleanup = time.time()
    cleanup_duration = int(end_time_cleanup - start_time_cleanup)
    if end_time_cleanup - start_time_cleanup < 1:
        cleanup_duration = round(end_time_cleanup - start_time_cleanup, 2)
    return cleanup_duration


def create_csv_logfile():
    out_log_file_path = os.path.dirname(csv_log_file)
    if not os.path.isdir(out_log_file_path):
        print("Creating log file path \"{}\"".format(out_log_file_path))
        os.makedirs(out_log_file_path)
    if not os.path.isfile(csv_log_file):
        print("Creating CSV log file: {}".format(csv_log_file))
        with open(csv_log_file, "w") as csv_file:
            csv_file.write(
                "\"Hostname\",\"Copy Type\",\"Log file\",\"Datetime\",\"Date\",\"Time\",\"Source directory\",\"Target directory\",\"Files copied\",\"No. of directories\",\"No. of files\",\"File size\",\"File units\",\"Total seconds\",\"Time taken\",\"MB per minute\",\"Delete time seconds\",\"Delete time\"\n")
    return out_log_file_path


if __name__ == "__main__":
    """
      Variables:
        - to_dir: Directory to which the single and multiple files are copied.
                  A new directory called 'CopyTo' (to_dir_name) is created and the file(s) 
                  are copied here. This new directory is then deleted and time
                  taken to delete is recorded in the csv log file.
    """

    to_dir = r"\\2108-jxi\c$\GISData\Scripts\RobocopySpeedTest"

    # #######################################################################################
    script_name = os.path.basename(sys.argv[0]).split(".")[0]
    home_dir = os.path.dirname(sys.argv[0]).replace("/", "\\")
    config_list = [[r"{}\CopyFrom".format(home_dir), "new-zealand-latest-free.shp_20200722.zip"],
                   [r"{}\CopyFromMulti".format(home_dir), ""]]
    csv_log_file = r"{}\logs2\RobocopySpeedTest.csv".format(home_dir)
    to_dir_name = "CopyTo"
    copy_to_dir = os.path.join(to_dir, to_dir_name)

    log_file_path = create_csv_logfile()

    now = datetime.now()
    time_now = now.strftime("%Y%m%d_%H%M%S")
    run_robocopy()
    # # transfer_log_info(sys.argv)

    sleep_time = 10
    print("Waiting for {} seconds before closing...".format(sleep_time))
    time.sleep(sleep_time)
