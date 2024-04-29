#region imports
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", '-r', package])
package = 'requirements.txt'
install(package)

import tkinter
import os
import platform
import json
from Dropbox_Token_Despenser import DropboxTokenDespenserGUI
from Dropbox_Token_Despenser import DropboxTokenAuthorizationGUI
import customtkinter
#endregion

# ~~~~~~~~~~~~~~~~ Window Setup
#region window setup
#Set basic appearance settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
#root.geometry("720x480")
root.minsize(width=720, height=540)
root.title("Content MGMT")

headerFrame = customtkinter.CTkFrame(master=root)
headerFrame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "NEW")

frame = customtkinter.CTkFrame(master=root)
frame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "NSEW")

execFrame = customtkinter.CTkFrame(master=root)
execFrame.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "NSEW")

footerFrame = customtkinter.CTkFrame(master=root)
footerFrame.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "SEW")
#endregion

# ~~~~~~~~~~~~~~~~ Variables Setup
#region initial setup, variables, and structure
#Define user variables
cont_dir = tkinter.StringVar()
thumbnail_dir = tkinter.StringVar()
db_thumb_dir = tkinter.StringVar()
airtable_token = tkinter.StringVar()
airtable_base_key = tkinter.StringVar()
airtable_table_key = tkinter.StringVar()
db_app_key = tkinter.StringVar()
db_secret = tkinter.StringVar()
db_refresh_key = tkinter.StringVar()

#Define JSON API default structure for dropbox refresh token
defaultsSettings = data = '''
{
  "DROPBOX_SECRET": null,
  "DROPBOX_KEY": null,
  "DROPBOX_ACCESS_TOKEN": null,
  "DROPBOX_REFRESH_TOKEN": null,
  "AIRTABLE_API_KEY": null,
  "AIRTABLE_BASE_KEY": null,
  "AIRTABLE_TABLE_NAME": null,
  "AIRTABLE_URL":  null,
  "CONTENT_SOURCE": null,
  "THUMB_DEPOT": null,
  "THUMB_DB_PATH": null,
  "REFRESH_KEY": null
}
'''
defaults =json.loads(defaultsSettings)
settingsPath = 'secrets.json'
#endregion

# ~~~~~~~~~~~~~~~~ Define All Functions
#region functions

def saveConf():
    defaults['CONTENT_SOURCE'] = cont_dir.get().strip()
    defaults['THUMB_DEPOT'] = thumbnail_dir.get().strip()
    defaults['THUMB_DB_PATH'] = db_thumb_dir.get().strip()
    defaults['DROPBOX_SECRET'] = db_secret.get().strip()
    defaults['DROPBOX_KEY'] = db_app_key.get().strip()
    defaults['AIRTABLE_API_KEY'] = airtable_token.get().strip()
    defaults['AIRTABLE_BASE_KEY'] = airtable_base_key.get().strip()
    defaults['AIRTABLE_TABLE_NAME'] = airtable_table_key.get().strip()
    defaults['AIRTABLE_URL'] = f'https://api.airtable.com/v0/{defaults['AIRTABLE_BASE_KEY']}/{defaults['AIRTABLE_TABLE_NAME']}'
    #dbRefreshButton.configure()

    final = open(settingsPath,'w')
    final.write(json.dumps(defaults))
    final.close()
    print("Configuration saved")
    return defaults

def runApp():
    if platform.system() == 'Darwin':
        subprocess.run(['python3', '_MGMT_OSX.py'])
    else:
        subprocess.run(['python', '_MGMT.py'])
    print("Running Application")

def dbGetToken():
    print("okay")
    try:
        DropboxTokenDespenserGUI(defaults['DROPBOX_KEY'],defaults['DROPBOX_SECRET'])
    except Exception as e :
        print("Token Generation Failed!", e)

def storeRefreshToken():
    defaults['CONTENT_SOURCE'] = cont_dir.get().strip()
    defaults['THUMB_DEPOT'] = thumbnail_dir.get().strip()
    defaults['THUMB_DB_PATH'] = db_thumb_dir.get().strip()
    defaults['DROPBOX_SECRET'] = db_secret.get().strip()
    defaults['DROPBOX_KEY'] = db_app_key.get().strip()
    defaults['AIRTABLE_API_KEY'] = airtable_token.get().strip()
    defaults['AIRTABLE_BASE_KEY'] = airtable_base_key.get().strip()
    defaults['AIRTABLE_TABLE_NAME'] = airtable_table_key.get().strip()
    defaults['AIRTABLE_URL'] = f'https://api.airtable.com/v0/{defaults['AIRTABLE_BASE_KEY']}/{defaults['AIRTABLE_TABLE_NAME']}'
    defaults['REFRESH_KEY'] = db_refresh_key.get().strip()
    final = open(settingsPath,'w')
    final.write(json.dumps(defaults))
    final.close()
    access_token, refresh_token = DropboxTokenAuthorizationGUI(defaults['DROPBOX_KEY'],defaults['DROPBOX_SECRET'],defaults['REFRESH_KEY'])
    defaults['DROPBOX_ACCESS_TOKEN']=access_token
    defaults['DROPBOX_REFRESH_TOKEN']=refresh_token
    f = open(settingsPath,'w')
    f.write(json.dumps(defaults))
    f.close()
    print("Access Token: ", access_token)
    print("Refresh Token: ", refresh_token)
    print("Refresh Token Saved!")

def loadExistingJson():
    f = open(settingsPath)
    existingData = json.load(f)
    f.close()
    try:
        cont_dir.set(existingData['CONTENT_SOURCE'])
        thumbnail_dir.set(existingData['THUMB_DEPOT'])
        db_thumb_dir.set(existingData['THUMB_DB_PATH'])
        airtable_token.set(existingData['AIRTABLE_API_KEY'])
        airtable_base_key.set(existingData['AIRTABLE_BASE_KEY'])
        airtable_table_key.set(existingData['AIRTABLE_TABLE_NAME'])
        db_app_key.set(existingData['DROPBOX_KEY'])
        db_secret.set(existingData['DROPBOX_SECRET'])
        db_refresh_key.set(existingData['REFRESH_KEY'])
    except Exception as e :
        print("Cannot Load Existing Settings.", e)

# ~~~~~~~~~~~~~~~~ Folder Dialog Buttons for Directory Picking
def cont_browse_button():
    foldername = customtkinter.filedialog.askdirectory()
    cont_dir.set(foldername)
    return foldername

def thumb_browse_button():
    foldername = customtkinter.filedialog.askdirectory()
    thumbnail_dir.set(foldername)
    return foldername

#endregion

# ~~~~~~~~~~~~~~~~ Establish all Labels with CTkinter
#region Labels
# Create Labels
headerLabel = customtkinter.CTkLabel(master=headerFrame, text="Content MGMT", font=("Roboto", 24))
contentLabel = customtkinter.CTkLabel(master=frame, text="Content Directory: ", font=("Roboto", 16))
thumbnalLabel = customtkinter.CTkLabel(master=frame, text="Thumbnail Output Directory: ", font=("Roboto", 16))
dbPathLabel = customtkinter.CTkLabel(master=frame, text="Dropbox Relative Thumbnail Path: ", font=("Roboto", 16))
airtableTokenLabel = customtkinter.CTkLabel(master=frame, text="Airtable Token: ", font=("Roboto", 16))
airtableBaseLabel = customtkinter.CTkLabel(master=frame, text="Airtable Base Key (in URL starting with app): ", font=("Roboto", 16))
airtableTblLabel = customtkinter.CTkLabel(master=frame, text="Airtable Table Key (in URL starting with tbl): ", font=("Roboto", 16))
dbAppKeyLabel = customtkinter.CTkLabel(master=frame, text="Dropbox App Key: ", font=("Roboto", 16))
dbSecretLabel = customtkinter.CTkLabel(master=frame, text="Dropbox App Secret: ", font=("Roboto", 16))
dbRefreshLabel = customtkinter.CTkLabel(master=frame, text="Dropbox Refresh Token: ", font=("Roboto", 16))
footerLabel = customtkinter.CTkLabel(master=footerFrame, text="Andy Philpo, Josh Spodick, Grant McDonald, Drew Winston", font=("Roboto", 10, "italic"))

# Set labels on screen
headerLabel.pack(padx = 20, pady = 10, anchor="n")
contentLabel.grid(row = 1, column = 0, sticky = "e")
thumbnalLabel.grid(row = 2, column = 0, sticky = "e")
dbPathLabel.grid(row = 3, column= 0, sticky = "e")
airtableTokenLabel.grid(row = 4, column= 0, sticky = "e")
airtableBaseLabel.grid(row= 5, column= 0, sticky= "e")
airtableTblLabel.grid(row= 6, column= 0, sticky= "e")
dbAppKeyLabel.grid(row= 7, column= 0, sticky = "e")
dbSecretLabel.grid(row= 8, column= 0, sticky = "e")
dbRefreshLabel.grid(row= 12, column= 0, sticky = "e")
footerLabel.pack(padx = 0, pady = 10, anchor = "s")

#endregion

# ~~~~~~~~~~~~~~~~ Establish all user interactive text fields with CTkinter
#region Entries
#Create text fields
contentEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Content Directory", width = 300, textvariable = cont_dir)
thumbnailEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Thumbnail Directory", width = 300, textvariable = thumbnail_dir)
dbPathEntry = customtkinter.CTkEntry(master=frame, placeholder_text="path relative to DB folder, remove last slash", width = 300, textvariable = db_thumb_dir)
airtableTokenEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Airtable Token", width = 300, textvariable = airtable_token)
airtableBaseEntry = customtkinter.CTkEntry(master=frame, placeholder_text="app...", width= 300, textvariable = airtable_base_key)
airtableTblEntry = customtkinter.CTkEntry(master=frame, placeholder_text="tbl...", width= 300, textvariable= airtable_table_key)
dbAppKeyEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Dropbox App Key", width = 300, textvariable = db_app_key)
dbSecretEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Dropbox Secret", width = 300, textvariable = db_secret)
dbRefreshEntry = customtkinter.CTkEntry(master=frame, placeholder_text="Dropbox Refresh Token", width=300, textvariable= db_refresh_key)

#Folder Browser for content and thumbnail directories
dirButton1 = customtkinter.CTkButton(master=frame, text="Browse", command= cont_browse_button, width=40)
dirButton1.grid(row = 1, column = 2)

dirButton2 = customtkinter.CTkButton(master=frame, text="Browse", command= thumb_browse_button, width=40)
dirButton2.grid(row=2, column=2)

#Set entries on screen
contentEntry.grid(row = 1, column = 1, sticky = "w", columnspan = 1)
thumbnailEntry.grid(row = 2, column = 1, sticky = "w", columnspan = 1)
dbPathEntry.grid(row = 3, column = 1, sticky = "w", columnspan = 2)
airtableTokenEntry.grid(row = 4, column = 1, sticky = "w", columnspan = 2)
airtableBaseEntry.grid(row = 5, column = 1, sticky = "w", columnspan = 2)
airtableTblEntry.grid(row = 6, column = 1, sticky = "w", columnspan = 2)
dbAppKeyEntry.grid(row = 7, column = 1, sticky = "w", columnspan = 2)
dbSecretEntry.grid(row = 8, column = 1, sticky = "w", columnspan = 2)
dbRefreshEntry.grid(row = 12, column = 1, sticky = "w", pady = 10, columnspan = 2)

#endregion

# ~~~~~~~~~~~~~~~~ Establish all Buttons to trigger functions and other sub processes
#region Buttons
#Create Butons
#customtkinter.CTkLabel(master=frame, text="   ").grid(row=9, column=1)

saveConfButton = customtkinter.CTkButton(master=frame, text='Save Configuration', width=140, height=28, command=saveConf)
saveConfButton.grid(row = 10, column = 1, pady = 10)

dbRefreshButton = customtkinter.CTkButton(master=frame, text="Retrieve Dropbox Refresh Token", width=200, height=28, command=dbGetToken)
dbRefreshButton.grid(row = 11, column = 1)

dbStoreRefreshButton = customtkinter.CTkButton(master=frame, text="Store Refresh Token", width=200, height=28, command=storeRefreshToken)
dbStoreRefreshButton.grid(row = 13, column = 1)

loadExistingButton = customtkinter.CTkButton(master=execFrame, text="Load Existing Data", width=200, height=28, command=loadExistingJson)
loadExistingButton.grid(row = 0, column = 0, padx = 30, pady = 10, sticky = "E")

runAppButton = customtkinter.CTkButton(master=execFrame, text="Run App", width=200, height=28, command=runApp)
runAppButton.grid(row = 0, column = 1, padx = 30, pady = 10, sticky = "W")

#endregion

#Run App
root.mainloop()