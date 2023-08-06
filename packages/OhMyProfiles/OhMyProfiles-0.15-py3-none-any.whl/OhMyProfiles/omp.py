#!/usr/bin/python
import hashlib
import os
import sys
import json
import uuid
import zipfile
import getpass

VERSION = "0.15"


def show_help():
    print("""
   *******     ****     ****   *******
  **/////**   /**/**   **/**  /**////**
 **     //**  /**//** ** /**  /**   /**
/**      /**  /** //***  /**  /*******
/**      /**  /**  //*   /**  /**////
//**     **   /**   /    /**  /**
 //*******    /**        /**  /**
  ///////     //         //   //

    """)
    print("Oh My Profiles v{}\n".format(VERSION))
    print("-h\t\thelp\t\t\tShow help message")
    print("-a\t\tadd [filename]\t\tManage my profile")
    print("-l\t\tlist\t\t\tList file to manager")
    print("\t\texport\t\t\tExport to zip")
    print("\t\timport [filename]\tImport profile")
    print("-r\t\trm [UUID]\t\tDelete a config")


def importf(filename):
    i = getpass.getpass('Password:')
    h = hashlib.sha512()
    h.update(i.encode())
    Hash = h.hexdigest().encode()
    buff = []
    with open(filename, "rb") as f:
        fc = f.read()
        flen = len(fc)
        for i in range(flen):
            c = i % len(Hash)
            o = fc[i] ^ Hash[c]
            buff.append(o)
        with open(filename.replace(".zip", "")+".out.zip", "wb") as fo:
            fo.write(bytes(buff))
    try:
        with zipfile.ZipFile(filename.replace(".zip", "")+".out.zip", "r") as f:
            for names in f.namelist():
                if names != "data.json":
                    f.extract(
                        names, os.environ['HOME']+"/.config/oh-my-profiles/data/")
                else:
                    f.extract(
                        names, os.environ['HOME']+"/.config/oh-my-profiles/")
    except zipfile.BadZipFile:
        print("Decryption failed, maybe the password is wrong")
    os.remove(filename.replace(".zip", "")+".out.zip")


def export_config():
    i = getpass.getpass('Password:')
    re_i = getpass.getpass('Retype password:')
    if i != re_i:
        print("Sorry, passwords do not match.")
        return
    h = hashlib.sha512()
    h.update(i.encode())
    Hash = h.hexdigest().encode()
    with zipfile.ZipFile(os.getcwd()+"/.export.zip", 'w') as z:
        z.write(os.environ['HOME'] +
                "/.config/oh-my-profiles/data.json", "data.json")
        for dirpath, dirnames, filenames in os.walk(os.environ['HOME']+"/.config/oh-my-profiles/data"):
            fpath = dirpath.replace(
                os.environ['HOME']+"/.config/oh-my-profiles/data", '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath+filename)
    buff = []
    with open(os.getcwd()+"/.export.zip", 'rb') as f:
        fc = f.read()
        flen = len(fc)
        for i in range(flen):
            c = i % len(Hash)
            o = fc[i] ^ Hash[c]
            buff.append(o)
        with open(os.getcwd()+"/export.zip", 'wb') as fo:
            fo.write(bytes(buff))
    os.remove(os.getcwd()+"/.export.zip")


def init():
    if not os.path.exists(os.environ['HOME']+"/.config/oh-my-profiles"):
        os.mkdir(os.environ['HOME']+"/.config/oh-my-profiles")
    if not os.path.exists(os.environ['HOME']+"/.config/oh-my-profiles/data"):
        os.mkdir(os.environ['HOME']+"/.config/oh-my-profiles/data")
    if not os.path.exists(os.environ['HOME']+"/.config/oh-my-profiles/data.json"):
        data = {"items": []}
        with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "w") as f:
            json.dump(data, f)
    return


def add_config(filename):
    if not os.path.exists(filename):
        print("file does not exist")
        return
    UUID = str(uuid.uuid4())
    if os.path.islink(os.getcwd()+"/"+filename):
        print("Centralized management of soft links is temporarily not supported")
        return
    with open(os.getcwd()+"/"+filename, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
    file_meta = {
        "UUID": UUID,
        "Target": os.getcwd()+"/"+filename,
        "Hash": hash,
        "Remarks": ""
    }
    with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "r") as f:
        data = json.load(f)
        for i in data["items"]:
            if i["Target"] == (os.getcwd()+"/"+filename):
                print(
                    "There are duplicate records in the metadata database, please check")
                return
        os.system("mv "+os.getcwd()+"/"+filename+" " +
                  os.environ['HOME']+"/.config/oh-my-profiles/data/"+UUID)
        os.system("ln -s "+os.environ['HOME'] +
                  "/.config/oh-my-profiles/data/"+UUID+" "+os.getcwd()+"/"+filename)
        data["items"].append(file_meta)
    with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "w") as f:
        json.dump(data, f)


def del_config(UUID):
    newdata = []
    status = 0
    with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "r") as f:
        data = json.load(f)
        for i in data["items"]:
            if UUID == i["UUID"]:
                status = 1
                print(i["Target"], " - ", i["UUID"], " # ", i["Hash"])
                print("Are you sure you want to delete this document?")
                a = input(
                    "(d confirm deletion | n cancel | r Restore files) >> ")
                if a == "d":
                    os.remove(os.environ['HOME'] +
                              "/.config/oh-my-profiles/data/"+i["UUID"])
                elif a == "n":
                    pass
                elif a == "r":
                    os.system("mv "+os.environ['HOME'] +
                              "/.config/oh-my-profiles/data/"+i["UUID"]+" "+i["Target"])
                else:
                    print("The input is not as expected, cancel the action")
            else:
                newdata.append(i)
    with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "w") as f:
        json.dump({"items": newdata}, f)
    if status == 0:
        print("No such file")


def list_config():
    with open(os.environ['HOME']+"/.config/oh-my-profiles/data.json", "r") as f:
        data = json.load(f)
        fix = ""
        for i in data["items"]:
            status = "\033[31m[-/-]\033[0m"
            if os.path.islink(i["Target"]) and os.readlink(i["Target"]) == (os.environ['HOME']+"/.config/oh-my-profiles/data/"+i["UUID"]):
                status = "\033[32m[---]\033[0m"
            else:
                fix += "rm "+i["Target"]+" && ln -s " + \
                    os.environ['HOME'] + "/.config/oh-my-profiles/data/" + \
                    i["UUID"]+" "+i["Target"]+"\n"
            print(status, i["UUID"], "\t", i["Target"])
        if fix != "":
            print("")
            print("You can use the following commands to repair. Note that the repair process may cause your original data to be lost. Please operate with caution")
            print(fix)


def sync():
    pass


def entry():
    init()
    if len(sys.argv) > 1:
        if sys.argv[1] == "help" or sys.argv[1] == "-h":
            show_help()
        elif sys.argv[1] == "add" or sys.argv[1] == "-a" and len(sys.argv) == 3:
            add_config(sys.argv[2])
        elif sys.argv[1] == "rm" or sys.argv[1] == "-r" and len(sys.argv) == 3:
            del_config(sys.argv[2])
        elif sys.argv[1] == "list" or sys.argv[1] == "-l":
            list_config()
        elif sys.argv[1] == "export":
            export_config()
        elif sys.argv[1] == "import" and len(sys.argv) == 3:
            importf(sys.argv[2])
        elif sys.argv[1] == "sync":
            sync()
        else:
            show_help()
    else:
        print("Try 'omp help' for more information.")


if __name__ == "__main__":
    entry()
