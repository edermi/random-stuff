#!/usr/bin/env python3

import sqlite3
import pathlib

def get_db(db_type):
    home = pathlib.Path.home()
    tool = ""
    if pathlib.Path.exists(home.joinpath('.nxc', 'workspaces', 'default')):
        tool = "nxc"
    elif pathlib.Path.exists(home.joinpath('.cme', 'workspaces', 'default')):
        tool = "cme"
    else:
        raise Error("Neither nxc, nor cme found")
    if db_type == "smb":
        return sqlite3.connect(home.joinpath(f'.{tool}', 'workspaces', 'default', 'smb.db'))

'''
  CREATE TABLE "hosts" (\n'
              "id" integer PRIMARY KEY,\n'
              "ip" text,\n'
              "hostname" text,\n'
              "domain" text,\n'
              "os" text,\n'
              "dc" boolean,\n'
              "smbv1" boolean,\n'
              "signing" boolean,\n'
              "spooler" boolean,\n'
              "zerologon" boolean,\n'
              "petitpotam" boolean\n'
              )'),
'''
def extract_smb1(conn):
    cur = conn.cursor() 
    res = cur.execute("""SELECT ip, 
       COALESCE(NULLIF(hostname, ''), MAX(hostname)) AS hostname, 
       COALESCE(NULLIF(domain, ''), MAX(domain)) AS domain
FROM hosts 
WHERE smbv1 = True
GROUP BY ip
HAVING MAX(CASE WHEN hostname != '' OR domain != '' THEN 1 ELSE 0 END) = 1;
""")
    print("###SMBv1###")
    print("IP,Hostname,Domain")
    for row in res:
        print(",".join(replace_string_from_tuple(row, "\x00", ""))) # remove awkward nulls
    cur.close()

def extract_signing(conn):
    cur = conn.cursor() 
    res = cur.execute("""SELECT ip, 
       COALESCE(NULLIF(hostname, ''), MAX(hostname)) AS hostname, 
       COALESCE(NULLIF(domain, ''), MAX(domain)) AS domain
FROM hosts 
WHERE signing = False
GROUP BY ip
HAVING MAX(CASE WHEN hostname != '' OR domain != '' THEN 1 ELSE 0 END) = 1;
""")
    print("###SMB Signing###")
    print("IP,Hostname,Domain")
    for row in res:
        print(",".join(replace_string_from_tuple(row, "\x00", ""))) # remove awkward nulls
    cur.close()

def replace_string_from_tuple(tuple_to_check, old_str, new_str):
    if old_str in tuple_to_check: # check if we need to fix a null value, otherwise just move on
        working_copy = list(tuple_to_check) # tuples are immutable
        for pos,_ in enumerate(working_copy): # need to index as using iterator would return a copy
            if working_copy[pos] == old_str:
                working_copy[pos] = new_str
        return tuple(working_copy)
    return tuple_to_check
    

if __name__ == '__main__':
    with get_db("smb") as conn:
        extract_smb1(conn)
        extract_signing(conn)

