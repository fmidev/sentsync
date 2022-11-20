#!/usr/bin/python3

import argparse
import datetime
import os,sys
import json
import tempfile
from copy import deepcopy
from uuid import uuid4
from sentinelsat import SentinelAPI


now = datetime.datetime.utcnow()
today = datetime.datetime(now.year,now.month,now.day)

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getScriptName():
    return os.path.splitext(os.path.realpath(sys.argv[0]))[0]

def write2log(fpath,severity="INFO", description=""):
    with open(fpath,'a') as fp:
        ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S UTC')
        fp.write("["+ts+"]")
        fp.write(" ["+severity+"]")
        fp.write(" ["+description+"]")
        fp.write('\n')
    # Debug
    # print(description)

basedir = getScriptPath()
tmpdir = tempfile.gettempdir()
parent_log_path = os.path.join(basedir,getScriptName() + '.log')

def terminate_cli():
    write2log(parent_log_path,"INFO",'Terminating. Use --help for usage.')
    exit()

def terminate_cfg(config_file,scene):
    write2log(parent_log_path,"INFO",'Terminating. Check scene %s in config file %s.' % (scene,config_file))
    exit()

parser = argparse.ArgumentParser(description = "Reproject and resample 1km IMS to target grid.")
parser.add_argument('--config-file', help = "Path to the (json) config file. See readme or the example. Cannot be used with other arguments.")

parser.add_argument('--day-offset', action = "append", help = "Offset in days (int) from today (e.g. -1 is yesterday). Can be used multiple times. Cannot be used with -d or -r.")
parser.add_argument('--day', action = "append", help = "Daystring YYYYMMDD. Can be used multiple times. Cannot be used with -r or -o.")
parser.add_argument('--day-range', help = "range of daystrings YYYYMMDD-YYYYMMDD. Cannot be used with -d or -o.")

parser.add_argument('--wkt', help = "Area in WKT format. Use in quotes.")
# TODO fix product eg name
parser.add_argument('--product', help = "Product to download (e.g. S1GRD)")

parser.add_argument('--target-dir', help = "Path to target directory to stored in.")
parser.add_argument('--log-file', help = "Path to log file.")

parser.add_argument('--hub-url', help = "URL of the Sentinel hub.")
parser.add_argument('--username', help = "Username for the Sentinel hub.")
parser.add_argument('--password', help = "Password for the Sentinel hub.")
parser.add_argument('--credentials-file', help = "Credentils file for the Sentinel hub. Do not use url, username and password with this. See readme for format.")

args = parser.parse_args()
arg_list = [arg.replace('_','-') for arg in list(args.__dict__.keys())]
value_list = list(args.__dict__.values())

if args.config_file is not None:
    args.config_file = os.path.realpath(args.config_file)
    # Check if other arguments supplied
    if value_list.count(None) != len(value_list)-1:
        write2log(parent_log_path,"ERROR","Cannot use other arguments with config-file.")
        write2log(parent_log_path,"INFO",'Terminating. Use --help for usage.')
        exit()

    # Check and parse config file
    cfg_path = args.config_file
    try:
        cfg = json.load(open(cfg_path,'r'))
    except Exception:
        write2log(parent_log_path,"ERROR","Problem in config file JSON format, check config file.")
        write2log(parent_log_path,"ERROR",'Terminating')
        exit()

    # read scenes and merge with shared options, fill missing as None
    scenes = {}
    for scene_label in cfg["scenes"]:
        for product in cfg["scenes"][scene_label]["products"]:
            scene_label_product = scene_label+"|"+product
            scenes.update(
                deepcopy(
                    {scene_label_product: cfg["scenes"][scene_label]}
                )
            )
            scenes[scene_label_product].pop("products")
            scenes[scene_label_product].update(
                deepcopy(cfg["scenes"][scene_label]["products"][product])
            )
            scenes[scene_label_product].update({"config-file":args.config_file})
            scenes[scene_label_product].update({"product":product})
            for arg in arg_list:
                if arg not in scenes[scene_label_product]:
                    if arg in cfg["shared"]:
                        scenes[scene_label_product].update({arg:deepcopy(cfg["shared"][arg])})
                    else:
                        scenes[scene_label_product].update({arg:None})

else:
    # set cli options as scene
    scenes = {
        "cli" : {}
    }
    for a,arg in enumerate(arg_list):
        scenes["cli"].update({arg:value_list[a]})

# parse, complete, check options
for scene_label in scenes:
    # Check required and combinations
    if (scenes[scene_label]["day"], scenes[scene_label]["day-offset"], scenes[scene_label]["day-range"]).count(None) != 2:
        write2log(parent_log_path,"ERROR","Use minimum and only one of the temporal arguments.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    # TODO add other type of extent (what?)
    if scenes[scene_label]["wkt"] is None:
        write2log(parent_log_path,"ERROR","Spatial extent is required.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if scenes[scene_label]["product"] is None:
        write2log(parent_log_path,"ERROR","Product type is required.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if scenes[scene_label]["target-dir"] is None:
        write2log(parent_log_path,"ERROR","Target directory is required.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if scenes[scene_label]["log-file"] is None:
        write2log(parent_log_path,"ERROR","Path to log file is required.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if scenes[scene_label]["credentials-file"] is None and (scenes[scene_label]["hub-url"], scenes[scene_label]["username"], scenes[scene_label]["password"]).count(None) != 0:
        write2log(parent_log_path,"ERROR","Arguments for credentials are missing.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if scenes[scene_label]["credentials-file"] is not None and (scenes[scene_label]["hub-url"], scenes[scene_label]["username"], scenes[scene_label]["password"]).count(None) != 3:
        write2log(parent_log_path,"ERROR","Credential files and other credentials arguments cannot be used together.")
        if scene_label == "cli":
            terminate_cli()
        else:
            terminate_cfg(scenes[scene_label]["config-file"],scene_label)

    # use realpaths
    for arg in scenes[scene_label]:
        if arg in ["target-dir","log-file","credentials-file"]:
            if scenes[scene_label][arg] is not None:
                scenes[scene_label][arg] = os.path.realpath(scenes[scene_label][arg])

    # check existence-permissions
    if os.path.exists(scenes[scene_label]["log-file"]):
        write2log(parent_log_path,"WARNING","Log file in the config exists. Log will be appended.")
        if not os.access(scenes[scene_label]["log-file"], os.W_OK):
            write2log(parent_log_path,"ERROR","Log file in config is not writable.")
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    else:
        try:
            os.makedirs(os.path.split(scenes[scene_label]["log-file"])[0],exist_ok = True)
        except:
            write2log(parent_log_path,"ERROR","Log file in config is not writable.")
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    if os.path.exists(scenes[scene_label]["target-dir"]):
        write2log(parent_log_path,"WARNING","Target directory in the config exists.")
        if not os.access(scenes[scene_label]["target-dir"], os.W_OK):
            write2log(parent_log_path,"ERROR","Target directory in config is not writable.")
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)
    else:
        try:
            os.makedirs(scenes[scene_label]["target-dir"],exist_ok = True)
        except:
            write2log(parent_log_path,"ERROR","Log file in config is not writable.")
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)
        
    # temporals
    if scenes[scene_label]["day-range"] is not None:
        try:
            scenes[scene_label]["day-range"] = scenes[scene_label]["day-range"].split("-")
            scenes[scene_label]["day-range"][0] = datetime.datetime.strptime(scenes[scene_label]["day-range"][0],"%Y%m%d")
            scenes[scene_label]["day-range"][1] = datetime.datetime.strptime(scenes[scene_label]["day-range"][1],"%Y%m%d")
            scenes[scene_label]["day-range"] = tuple(scenes[scene_label]["day-range"])
            if len(scenes[scene_label]["day-range"]) != 2:
                raise
        except:
            write2log(parent_log_path,"ERROR","Day string %s not in correct format." % scenes[scene_label]["day-range"])
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)

    if scenes[scene_label]["day"] is not None:
        daylist = []
        if isinstance(scenes[scene_label]["day"],str):
            scenes[scene_label]["day"] = [scenes[scene_label]["day"]]
        for day in scenes[scene_label]["day"]:
            try:
                day = datetime.datetime.strptime(day,"%Y%m%d")
            except:
                write2log(parent_log_path,"ERROR","Day list or day string in day list %s not in correct format." % scenes[scene_label]["day"])
                if scene_label == "cli":
                    terminate_cli()
                else:
                    terminate_cfg(scenes[scene_label]["config-file"],scene_label)
            daylist.append(day)
        scenes[scene_label]["day"] = deepcopy(daylist)

    if scenes[scene_label]["day-offset"] is not None:
        daylist = []
        for day_offset in scenes[scene_label]["day-offset"]:
            try:
                day = today + datetime.timedelta(days=int(day_offset))
            except:
                write2log(parent_log_path,severity="ERROR",description="Day offset %s in argument not in correct format." % day_offset)
                if scene_label == "cli":
                    terminate_cli()
                else:
                    terminate_cfg(scenes[scene_label]["config-file"],scene_label)
            if day > today:
                write2log(parent_log_path,severity="ERROR",description="Day offset %s means a future day. No foretelling." % day_offset)
                if scene_label == "cli":
                    terminate_cli()
                else:
                    terminate_cfg(scenes[scene_label]["config-file"],scene_label)
            daylist.append(day)
        # convert to daylist
        scenes[scene_label]["day"] = deepcopy(daylist)
        scenes[scene_label]["day-offset"] = None

    # TODO check extent (if poly or bb is valid)
    if "+" in scenes[scene_label]["wkt"]:
        write2log(parent_log_path,severity="WARNING",description=" + Sign found in WKT in scene %s. Replacing with spaces." % scene_label)
        scenes[scene_label]["wkt"] = scenes[scene_label]["wkt"].replace("+"," ")

    # credentials
    if scenes[scene_label]["credentials-file"] is not None:
        try:
            with open(scenes[scene_label]["credentials-file"],"r") as f:
                for line in f:
                    for arg in ["hub-url","username","password"]:
                        key = arg + ":"
                        if line[:len(key)] == key:
                            line = line[len(key):]
                            if line[-1:] == "\n":
                                line = line[:-1]
                            scenes[scene_label][arg] = line
            if [scenes[scene_label][arg] for arg in ["hub-url","username","password"]].count(None) != 0:
                raise
        except:
            write2log(parent_log_path,severity="ERROR",description="Credentials file in incorrect format or has missing fields. See readme.")
            if scene_label == "cli":
                terminate_cli()
            else:
                terminate_cfg(scenes[scene_label]["config-file"],scene_label)

write2log(parent_log_path,severity="INFO",description="Config file and/or arguments are valid. Processing to download.")
for scene_label in scenes:
    date_extents = []
    if scenes[scene_label]["day-range"] is not None:
        date_extents = [list(scenes[scene_label]["day-range"])]
        date_extents[0][1] += datetime.timedelta(days=1,seconds=-1)
        date_extents[0] = tuple(date_extents[0])

    if scenes[scene_label]["day"] is not None:  #offset already converted to daylist
        for day in scenes[scene_label]["day"]:
            date_extents.append((day, day + datetime.timedelta(days=1,seconds=-1)))
            
    write2log(parent_log_path,severity="INFO",description="Processing download of %s products for the scene \"%s\". Scene options:" % (scenes[scene_label]["product"],scene_label.replace("|"+scenes[scene_label]["product"],"")))
    write2log(parent_log_path,severity="INFO",description="- Area: %s" % scenes[scene_label]["wkt"])
    for date_extent in date_extents:
        write2log(parent_log_path,severity="INFO",description="- Date range: %s - %s" % (date_extent[0].strftime("%Y%m%dT%H%M%S"), date_extent[1].strftime("%Y%m%dT%H%M%S")))
    write2log(parent_log_path,severity="INFO",description="- Hub: %s" % scenes[scene_label]["hub-url"])
    write2log(parent_log_path,severity="INFO",description="- Target directory: %s" % scenes[scene_label]["target-dir"])
    write2log(parent_log_path,severity="INFO",description="- Log file: %s" % scenes[scene_label]["log-file"])

    write2log(scenes[scene_label]["log-file"],severity="INFO",description="Logging into the hub %s" % scenes[scene_label]["hub-url"])
    try:
        api = SentinelAPI(scenes[scene_label]["username"], scenes[scene_label]["password"], scenes[scene_label]["hub-url"])
    except:
        # TODO include API error to log
        write2log(scenes[scene_label]["log-file"],severity="ERROR",description="Error in logging in. Skipping scene.")
        write2log(parent_log_path,severity="ERROR",description="Error in logging in. See log file at %s. Skipping scene." % scenes[scene_label]["log-file"])
        continue

    for date_extent in date_extents:
        write2log(scenes[scene_label]["log-file"],severity="INFO",description="Requesting %s products from %s to %s in given WKT." % (
            scenes[scene_label]["product"], date_extent[0].strftime("%Y%m%dT%H%M%S"), date_extent[1].strftime("%Y%m%dT%H%M%S")
        ))
        
        products = api.query(
            area = scenes[scene_label]["wkt"],
            producttype = scenes[scene_label]["product"], 
            date = date_extent
        )

        write2log(scenes[scene_label]["log-file"],severity="INFO",description="%s products found." % len(products))

        try:
            write2log(scenes[scene_label]["log-file"],severity="INFO",description="Starting the download of %s products" % len(products))
            api.download_all(products, scenes[scene_label]["target-dir"], max_attempts=2,checksum=True)
            write2log(scenes[scene_label]["log-file"],severity="INFO",description="Download is complete.")
        except:
            # TODO include download log/error to log
            write2log(scenes[scene_label]["log-file"],severity="ERROR",description="Error in downloading. Skipping download.")
            write2log(parent_log_path,severity="ERROR",description="Error in downloading. See log file at %s. Skipping download." % scenes[scene_label]["log-file"])
            continue
