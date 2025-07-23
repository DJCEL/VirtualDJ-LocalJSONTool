import json
import pandas as pd

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_readFile_method_json(username:str):
    strFilepath_In = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON.json"

    # Open the JSON file and load its content
    fp = open(strFilepath_In, "r", encoding="utf8")
    Songs = json.load(fp)
    fp.close()

    NbSongs = len(Songs)
    if(NbSongs == 0):
        print("The JSON file is empty.")
        return

    print("NbSongs =", NbSongs)
    print("\n")

    # Extract unique tags from all the songs
    Tags = []
    for no,song in enumerate(Songs):
        for tag in song:
            if tag not in Tags:
                Tags.append(tag)
    
    print("Tags =", Tags)
    print("\n")
    print("Songs[0] =",Songs[0])
    print("\n")
#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_readFile_method_pandas(username:str):
    strFilepath_In = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON.json"

    # Read the JSON file into a pandas DataFrame
    df_Songs = pd.read_json(strFilepath_In)
    if(df_Songs.empty == True):
        print("The JSON file is empty.")
        return
    
    NbSongs = len(df_Songs.index)

    print("NbSongs =", NbSongs)
    print("\n")

    pd_Tags = df_Songs.columns
    Tags = pd_Tags.tolist()
    print("Tags =", Tags)
    print("\n")

    # 'uniqueId' is the unique key to identify a song so we can use it as the index of the DataFrame
    # Otherwise use LocalJSON_list_duplicates() to find duplicates
    # df_Songs.set_index('uniqueId', inplace=True)

    print("### Preview of the five first songs:\n")
    print(df_Songs.head(5))

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_sortSongs(username:str):
     strFilepath_In = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON.json"
     strFilepath_Out = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON_fixed.json"
     
     df_Songs = pd.read_json(strFilepath_In)

     df_Songs_sorted = df_Songs.sort_values(by='uniqueId', ascending=False)

     df_Songs_sorted['uniqueId'] = df_Songs_sorted['uniqueId'].astype(str)

     json_str = df_Songs_sorted.to_json(strFilepath_Out, orient='records')

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_list_duplicates(username:str):
     strFilepath_In = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON.json"
     strFilepath_Out = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON_fixed.json"
     
     df_Songs = pd.read_json(strFilepath_In)

     # Find duplicates based on 'uniqueId'
     duplicates = df_Songs[df_Songs.duplicated(subset=['uniqueId'], keep=False)]

     if duplicates.empty:
        print("No duplicates found in the JSON file.\n")
     else:
        print("### Duplicates found in the JSON file:\n")
        print(duplicates)

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_remove_duplicates(username:str):
     strFilepath_In = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON.json"
     strFilepath_Out = "C:\\Users\\" + username + "\\AppData\\Local\\VirtualDJ\\Plugins64\\OnlineSources\\LocalJSON_fixed.json"
     
     df_Songs = pd.read_json(strFilepath_In)

     # Remove duplicates based on 'uniqueId'. We keep the first occurrence.
     df_Songs.drop_duplicates(subset=['uniqueId'],keep='first',inplace=True)

     df_Songs['uniqueId'] = df_Songs['uniqueId'].astype(str)

     json_str = df_Songs.to_json(strFilepath_Out, orient='records')
#----------------------------------------------------------------------------------------------------------------------------------
def main():
    username = "YourWindowsUsername" # Replace with your actual Windows username

    #LocalJSON_readFile_method_json(username)
    LocalJSON_readFile_method_pandas(username)
    #LocalJSON_sortSongs(username)
    #LocalJSON_list_duplicates(username)
    #LocalJSON_remove_duplicates(username)

#----------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
