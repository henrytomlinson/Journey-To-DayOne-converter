# -*- coding: utf-8 -*-
# developed by aref993
import uuid
from time import strftime
from datetime import datetime
import json
import os
import glob
from yattag import Doc, indent
import shutil
from sys import stdout


def getuuid():
    uu = str(uuid.uuid4())
    return uu.replace("-", "").upper()


def read_specific_files(pathtodir, filetype):
    all_jrnls_in_array = []
    os.chdir(pathtodir)
    for anyfile in glob.glob("*." + filetype):
        with open(anyfile, 'r', encoding='utf-8') as tmpfile:
            all_jrnls_in_array.append(tmpfile.read())
    return all_jrnls_in_array


def convert_unixtime(unixtime):
    return datetime.fromtimestamp(int(unixtime) / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')


def check_dirs(path):
    os.chdir(path)
    if not os.path.exists('./journal.dayone/'):
        os.makedirs('journal.dayone')
    if not os.path.exists('./journal.dayone/entries/'):
        os.makedirs('./journal.dayone/entries/')
    if not os.path.exists('./journal.dayone/photos/'):
        os.makedirs('./journal.dayone/photos/')
    print('directory creation done.')


def deserialize_json(allentries):
    loaded = json.loads(allentries)
    return loaded


def convert_to_xml(entry):
    new_uuid = getuuid()
    alluuids.append(new_uuid)
    new_date = convert_unixtime(entry["date_journal"])
    doc, tag, text = Doc().tagtext()
    with tag('plist', Version="1.0"):
        with tag('dict'):
            with tag('key'):
                text('UUID')
            with tag('string'):
                text(new_uuid)
            with tag('key'):
                text('Creation Date')
            with tag('date'):
                text(new_date)
            # ... (rest of your XML generation code goes here)

    result = indent(doc.getvalue(), indentation=' ' * 4, newline='\r\n')
    return result


def convert_main():
    real_path = os.path.dirname(os.path.realpath(__file__))
    alljsons = []
    alljsons = read_specific_files("./journey/", "json")
    os.chdir(real_path)
    print('we found %d entries to export' % (len(alljsons)))
    check_dirs(real_path)
    i = 0
    for anyjson in alljsons:
        dj = deserialize_json(anyjson)
        xmltmp = ""
        xmltmp += (r'<?xml version="1.0" encoding="UTF-8"?>')
        xmltmp += (r'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">')
        xmltmp += (convert_to_xml(dj))
        suuid = alluuids[i]
        i = i + 1
        os.chdir(real_path + "/journal.dayone/entries/")
        with open(str(suuid) + ".doentry", "w", encoding='utf-8') as myfile:
            myfile.write(xmltmp)
        if len(dj['photos']) > 0:
            source = real_path + "/journey/" + str(dj['photos'][0])
            target = real_path + "/journal.dayone/photos/" + \
                str(suuid) + ".jpg"
            shutil.copyfile(source, target)
        stdout.write("\r%d entry imported successfully" % i)
        stdout.flush()


alluuids = []
convert_main()
