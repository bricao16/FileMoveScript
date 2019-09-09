#This script automatically transfers files from the M drives of St. Paul, Duluth, Furgus Falls, and Minneapolis to a new folder,
#and copies all of the files onto the server

import paramiko as pk
import os
import shutil
import argparse
import datetime
import smtplib
from email.mime.text import MIMEText
import ssl


#method to send email message if error occurs
def sendemail(error):
    smtp_server_name = 'smtp.gmail.com'
    port = '465' # for secure messages
    #port = '587'  # for normal messages
    sender = 'errormessages1@gmail.com'
    receiver = 'brian_cao@mnb.uscourts.gov'
    password = 'errors123'

    content = error
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Errors Have Been Found'
    if port == '465':
        server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
    else:
        server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
        server.starttls() # this is for secure reason

    server.login(sender, password)
    server.send_message(msg)
    server.quit()


numberOfSourceFiles = 0
numberOfDestinationFiles = 0

#current time variable
currentTime = datetime.datetime.now()
printTime = currentTime.replace(microsecond=0)

#source directories to collect files from
source = 'C:/Users/bricao/PycharmProjects/Test'
source1 = 'C:/Users/bricao/PycharmProjects/Test1'
source2 = 'C:/Users/bricao/PycharmProjects/Test2'

#destination folder to put all files in and copy to server
destination = "C:/Users/bricao/PycharmProjects/Test3"


#method to move all files from source directory to destination directory
def filemove(source, destination):
    for file in os.listdir(source):
        if os.listdir(source):
            try:
                src_file = os.path.join(source, file)
                dst_file = os.path.join(destination, file)
                shutil.move(src_file, dst_file)
                with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                    myFile.write(str(printTime) + str(": ") + str("Successfully moved: ")
                                 + file + str(" to directory: ") + destination + "\n")

                print("Successfully moved: ", file + " to directory: " + destination)
            except IOError:
                with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                    myFile.write(str(printTime) + ":" + " ERROR: Unable to move file: " + file + "\n")
                print("Unable to copy file: ", file)
                emailerror = str(printTime) + ": Error: Unable to copy file: ", file
                sendemail(str(emailerror))


#method that creates destination directory if it doesn't already exist
def dircheck():
    # if files exist, create a new directory
    if not os.path.exists(destination):
        try:
            os.mkdir(destination)
            with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                myFile.write(str(printTime) + ": Successfully created directory " + str(destination) + "\n")
            print("Successfully created directory: ", destination)

        except OSError:
            with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                myFile.write(str(printTime) + ": Creation of directory " + str(destination) + " failed" + "\n")
            print("Creation of directory ", destination, "failed" + "\n")
            emailerror = str(printTime) + ": Error: Creation of directory ", destination, "failed"
            sendemail(str(emailerror))

    else:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ": " + "Successfully moved files into directory: " + str(destination)
                         + "\n")

        print("Successfully created directory: ", destination)


#moving the files into destination directory and catching if directories did not have files in them
def completefilemove(source):
    #checking if files exist in the directory
    if os.listdir(source):
        #move all files from source directory into new directory
        filemove(source, destination)
    else:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ": "
              + 'No files were uploaded in directory: ' + str(source) + '\n')
        print(str(printTime) + ": "
              + 'No files were uploaded in directory: ' + str(source) + '\n')


#calling directory check method to create directory
dircheck()
#calling complete file move method for each source directory
completefilemove(source)
completefilemove(source1)
completefilemove(source2)


filesInDestination = []
newSourceFilesNumber = 0
#print('Files in Destination: ')

#storing all files in new destination directory into an array
# for file in os.listdir(destination):
#     if os.listdir(destination):
#         filesInDestination = file
#         numberOfDestinationFiles += 1
#     if os.listdir(source):
#         newSourceFilesNumber += 1
#print(filesInDestination)


#print('Total number of files in destination directory: ' + str(numberOfDestinationFiles))
#print('Total number of source files after move:', str(newSourceFilesNumber))


# #argparse to manually enter in username, password, and ipaddress
# parser = argparse.ArgumentParser(description='Login Information')
# parser.add_argument('-u', '--username', type=str, metavar='', help='Username')
# parser.add_argument('-p', '--password', type=str, metavar='', help='Password')
# parser.add_argument('-i', '--ipaddress', type=str, metavar='', help='IPaddress')
# args = parser.parse_args()


#method to connect to server and copy files to
def serverconnect():
    #user information


    # ip = args.ipaddress
    # userName = args.username
    # pwd = args.password
    fin = open('C:/Users/bricao/PycharmProjects/FileLog.txt', "r")
    data2 = fin.read()
    #print(data2)
    fin.close()


    #connecting to server
    try:
        client = pk.SSHClient()
        client.set_missing_host_key_policy(pk.AutoAddPolicy())
        client.connect(hostname=ip, port=22, username=userName, password=pwd)
    # This exception takes care of Authentication error& exceptions
    except pk.AuthenticationException:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ': ERROR : Authentication failed because of irrelevant details!' + "\n")
        print('ERROR : Authentication failed because of incorrect username or password')
        emailerror = str(printTime) + ': ERROR : Authentication failed because of incorrect username or password'
        print(emailerror)
        sendemail(str(emailerror))
        exit()

    # This exception will take care of the rest of the error& exceptions
    except ConnectionError:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ': ERROR : Could not connect to IP address' + "\n")
        print('ERROR : Could not connect to ip address')
        emailerror = str(printTime) + ': ERROR : Could not connect to IP address'
        sendemail(str(emailerror))
        exit()

    except TimeoutError:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ': ERROR : Could not connect to IP address' + "\n")
        print('ERROR : Could not connect to ip address')
        emailerror = str(printTime) + ': ERROR : Could not connect to IP address'
        sendemail(str(emailerror))
        exit()
    except:
        with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
            myFile.write(str(printTime) + ': ERROR : Could not connect to IP address' + "\n")
        print('ERROR : Could not connect to ip address')
        emailerror = str(printTime) + ': ERROR : Could not connect to IP address'
        sendemail(str(emailerror))
        exit()


    #path to copy and remote path to copy to
    local_path = 'C:/Users/bricao/PycharmProjects/Test3/'
    remote_path = '/home/autodkt/FTP/Test/'

    ftp_client1 = client.open_sftp()

    # creating new directory in remote server if the directory does not already exist
    try:
        ftp_client1.chdir(remote_path)  # Test if remote path exists
        print('Remote Path exists')
    except IOError:
        ftp_client1.mkdir(remote_path)  # Create remote path
        ftp_client1.chdir(remote_path)
        print('Creating Remote Path:', remote_path)

    log_file_path = 'C:/Users/bricao/PycharmProjects/'
    ftp_client = client.open_sftp()
    # creating new directory in remote server if the directory does not already exist
    try:
        ftp_client.chdir(remote_path)  # Test if remote path exists
    except IOError:
        ftp_client.mkdir(remote_path)  # Create remote path
        ftp_client.chdir(remote_path)
        print('Creating Remote Path:', remote_path)

    #path of FileLog.txt
    file_log_path = 'C:/Users/bricao/PycharmProjects/FileLog.txt'
    #source directory of FileLog.txt
    file_log_source = 'C:/Users/bricao/PycharmProjects/'
    #master file log path on local machine
    local_master_file_log_path = 'C:/Users/bricao/PycharmProjects/masterFileLog.txt'
    #master file log path on server
    server_master_file_log_path = '/home/autodkt/FTP/Test/masterFileLog.txt'

    #creating file log and storing master log on server
    try:
        os.chdir(file_log_source)
        ftp_client.get(server_master_file_log_path, local_master_file_log_path)
        print('Successfully got file: ', file_log_path)
        ftp_client.close()
        with open(local_master_file_log_path, 'a+') as outfile:
            with open(file_log_path) as infile:
                for line in infile:
                    outfile.write(line)
        ftp_client = client.open_sftp()
        new_log_file_path = os.path.join(log_file_path, 'masterFileLog.txt')
        ftp_client.put(new_log_file_path, remote_path + '/' + 'masterFileLog.txt')
        os.remove(local_master_file_log_path)

    except IOError:
        print('Failed to find masterFileLog in remote directory. Creating masterFileLog')
        new_log_file_path = os.path.join(log_file_path, 'FileLog.txt')
        ftp_client.put(new_log_file_path, remote_path + '/' + 'masterFileLog.txt')
        ftp_client.close()
        os.chdir(file_log_source)
        os.remove(local_master_file_log_path)


    #copying every file from local path into remote path
    def transfer_files():
        for file1 in os.listdir(local_path):
            new_local_path = os.path.join(local_path, file1)
            #copying files into remote directory
            try:
                ftp_client1.put(new_local_path, remote_path + '/' + file1)
               # with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                    #myFile.write(str(printTime) + "File being copied to server: ", file1 + "\n")
                print("File being copied to server: ", file1)
            except ConnectionError:
                #with open("C:/Users/bricao/PycharmProjects/FileLog.txt", "a+") as myFile:
                   # myFile.write(str(printTime) + "File being copied to server: " + file1 + str("failed\n"))
                print("File failed to copy to server")
                emailerror = str(printTime) + ': ERROR : File failed to copy to server'
                sendemail(str(emailerror))
        print('Finished copying files to server')

    transfer_files()
    ftp_client1.close()
    client.close()


serverconnect()

