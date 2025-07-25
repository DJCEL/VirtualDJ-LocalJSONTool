import os
import json
import pandas as pd

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_readFile_method_json(strFilepath_In):

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
def LocalJSON_readFile_method_pandas(strFilepath_In):

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
def LocalJSON_list_duplicates(strFilepath_In):
    
     df_Songs = pd.read_json(strFilepath_In)

     # Find duplicates based on 'uniqueId'
     duplicates = df_Songs[df_Songs.duplicated(subset=['uniqueId'], keep=False)]

     if duplicates.empty:
        print("No duplicates found in the JSON file.\n")
     else:
        print("### Duplicates found in the JSON file:\n")
        print(duplicates)

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_sortSongs(strFilepath_In, strFilepath_Out):
    
     df_Songs = pd.read_json(strFilepath_In)

     df_Songs_sorted = df_Songs.sort_values(by='uniqueId', ascending=False)

     df_Songs_sorted['uniqueId'] = df_Songs_sorted['uniqueId'].astype(str)

     json_str = df_Songs_sorted.to_json(strFilepath_Out, orient='records')

#----------------------------------------------------------------------------------------------------------------------------------
def LocalJSON_remove_duplicates(strFilepath_In, strFilepath_Out):
     
     df_Songs = pd.read_json(strFilepath_In)

     # Remove duplicates based on 'uniqueId'. We keep the first occurrence.
     df_Songs.drop_duplicates(subset=['uniqueId'],keep='first',inplace=True)

     df_Songs['uniqueId'] = df_Songs['uniqueId'].astype(str)

     json_str = df_Songs.to_json(strFilepath_Out, orient='records')
#----------------------------------------------------------------------------------------------------------------------------------
def main():
    # VirtualDJ folder
    strAppDatalocal = os.getenv('LOCALAPPDATA')
    strFolder_prod =  strAppDatalocal + "\\VirtualDJ\\Plugins64\\OnlineSources\\"
    
    # Project folder
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    strFolder_test = parent_directory + "\\files\\"
    
    # Files
    strFilepath_In = strFolder_prod + "LocalJSON.json"
    #strFilepath_In = strFolder_test + "LocalJSON.json"
    strFilepath_Out = strFolder_test + "LocalJSON_fixed.json"

    if(os.path.isfile(strFilepath_In) == False):
         print("The following file does not exist:")
         print(strFilepath_In)
         print("\nPlease check 'strFilepath_In' and try again.\n")
         return
    
    #LocalJSON_readFile_method_json(strFilepath_In)
    LocalJSON_readFile_method_pandas(strFilepath_In)
    #LocalJSON_list_duplicates(strFilepath_In)
    #LocalJSON_sortSongs(strFilepath_In, strFilepath_Out)
    #LocalJSON_remove_duplicates(strFilepath_In, strFilepath_Out)

#----------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
