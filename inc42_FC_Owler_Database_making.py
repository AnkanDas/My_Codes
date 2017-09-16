import numpy as np
import pandas as pd
import requests
import re
import sys
import urllib3
import csv
import codecs
import ast


'''
Reading the data sheet into dataframe
'''
df_inc = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Company_Basic_H1_2017_WithM&A.xlsx',
                           sheetname = 'Final')
df_fc = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'company basic')
df_ow = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Owler/company_basic_details.xlsx',
                           sheetname = 'company_basic_details')

'''
Function for cleaning the url to get just the domain name
'''
def get_domain(url):
    """Return top two domain levels from URI"""
    re_3986_enhanced = re.compile(r"""
        # Parse and capture RFC-3986 Generic URI components.
        ^                                    # anchor to beginning of string
        (?:  (?P<scheme>    [^:/?#\s]+): )?  # capture optional scheme
        (?://(?P<authority>  [^/?#\s]*)  )?  # capture optional authority
             (?P<path>        [^?#\s]*)      # capture required path
        (?:\?(?P<query>        [^#\s]*)  )?  # capture optional query
        (?:\#(?P<fragment>      [^\s]*)  )?  # capture optional fragment
        $                                    # anchor to end of string
        """, re.MULTILINE | re.VERBOSE)
    re_domain =  re.compile(r"""
        # Pick out top two levels of DNS domain from authority.
        (?P<domain>[^.]+\.[A-Za-z]{2,6})  # $domain: top two domain levels.
        (?::[0-9]*)?                      # Optional port number.
        $                                 # Anchor to end of string.
        """,
        re.MULTILINE | re.VERBOSE)
    result = ""
    m_uri = re_3986_enhanced.match(url)
    if m_uri and m_uri.group("authority"):
        auth = m_uri.group("authority")
        m_domain = re_domain.search(auth)
        if m_domain and m_domain.group("domain"):
            result = m_domain.group("domain")
            result = result.lower()
    return result


'''
Relpacing the websites with domain
'''

for index, row in df_inc.iterrows():
    df_inc.loc[index, "Website"] = get_domain(str(row["Website"]))
print (df_inc["Website"])

for index1, row in df_fc.iterrows():
    df_fc.loc[index1, "Website"] = get_domain(str(row["Website"]))
print (df_fc["Website"])

for index2, row in df_ow.iterrows():
    df_ow.loc[index2, "Website"] = get_domain(str(row["Website"]))
print (df_ow["Website"])

'''
Merging the 3 dataframes
'''
df_fc_inc = pd.merge(df_inc,df_fc, how='outer', on="Website",suffixes=('_inc42', '_FC'))
# print(df_fc_inc.head(5))
df_fc_inc_ow = pd.merge(df_fc_inc,df_ow, how='outer', on="Website",suffixes=('_x', '_OW'))
# print (df_fc_inc_ow.head(5))

print(df_fc_inc_ow.duplicated())

df_final = df_fc_inc_ow.drop_duplicates(['Website'], keep='first')
# print (df_final.columns)
# print (df_final["Website"])

'''
---------------------------For ID Map Worksheet------------------------------------------------------------------
'''

'''
Writing it to excel - ID_MAP
'''

to_write = df_final[["ID_inc42","ID_FC","ID","Website","Startup Name","organization name","Name"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/ID_MAP.xlsx')
to_write.to_excel(writer,'ID_MAP')
writer.save()

'''
---------------------------For Company Basic Worksheet-----------------------------------------------------------
'''


'''
Writing it to excel - Company_basic
'''
to_write = df_final[["ID_inc42","ID_FC","ID","Website","Startup Name","organization name","Name","Logo_x","Logo_OW",
                     "Launched Date","founded_on","Launch Year","Range Employee Count","Absolute Employee Count",
                     "employee_count","Employee Count_OW","Industries","Tags","keyword","Sector","CEO","CEO logo",
                     "Founders","Status Detail","Status","Description","short_description","Sort Description",
                     "Long Description","Revenue"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_Basic.xlsx')
to_write.to_excel(writer,'Basic_info')
writer.save()

'''
---------------------------For Social links and Images Basic Worksheet-----------------------------------------------
'''
df_fc_images = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'images')
df_fc_social = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'social_info')


# Defining index to extract website links from the dataframe
df_fc_1 = df_fc.set_index("ID")


social_links_fc = []

for index, row in df_fc_images.iterrows():
    temp = []
    temp.append(row["ID"])
    temp.append(row["url"])
    x = str(row["label"])
    x = x + "_images"
    temp.append(x)
    temp.append("Full Contact")
    temp.append(df_fc_1.loc[row["ID"],"Website"])
    social_links_fc.append(temp)


for index, row in df_fc_social.iterrows():
    temp = []
    temp.append(row["ID"])
    temp.append(row["url"])
    temp.append(row["type_name"])
    temp.append("Full Contact")
    temp.append(df_fc_1.loc[row["ID"], "Website"])
    social_links_fc.append(temp)

df_social_link_image_fc = pd.DataFrame(social_links_fc)
print (df_social_link_image_fc.head(5))

social_logo_array_list = []

for index, row in df_final.iterrows():
    if ((not str(row["ID_inc42"])== "nan") and (not str(row["LinkedIn"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append(row["LinkedIn"])
        temp.append("LinkedIn")
        temp.append("inc42")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID_inc42"])== "nan") and (not str(row["Facebook_x"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append(row["Facebook_x"])
        temp.append("Facebook")
        temp.append("inc42")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID_inc42"])== "nan") and (not str(row["Twitter_x"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append(row["Twitter_x"])
        temp.append("Twitter")
        temp.append("inc42")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID_FC"])== "nan") and (not str(row["Logo_x"]) == "nan")):
        temp = []
        temp.append(row["ID_FC"])
        temp.append(row["Logo_x"])
        temp.append("Logo")
        temp.append("Full Contact")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Linkedin"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append(row["Linkedin"])
        temp.append("LinkedIn")
        temp.append("Owler")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Facebook_OW"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append(row["Facebook_OW"])
        temp.append("Facebook")
        temp.append("Owler")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Twitter_OW"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append(row["Twitter_OW"])
        temp.append("Twitter")
        temp.append("Owler")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Youtube"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append(row["Youtube"])
        temp.append("Youtube")
        temp.append("Owler")
        temp.append(row["Website"])
        social_logo_array_list.append(temp)
        # print (temp)


df_social_link_image = pd.DataFrame(social_logo_array_list)
print (df_social_link_image.head(10))

df_social_links = df_social_link_image.append(df_social_link_image_fc, verify_integrity= False)
df_social_links.columns = ["ID","url","Portal Name","Source","domain"]

print(df_social_links.head(5))

'''
Writing it to excel - Company_Social
'''
to_write = df_social_links[["ID","url","Portal Name","Source","domain"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_Social.xlsx')
to_write.to_excel(writer,'Social_links_logo')
writer.save()

'''
---------------------------For Contact Worksheet-----------------------------------------------
'''

df_fc_contact = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'email_phone')

contact_fc = []

for index, row in df_fc_contact.iterrows():
    temp = []
    temp.append(row["ID"])
    temp.append(row["type"])
    temp.append(row["value"])
    temp.append(row["label"])
    temp.append("Full Contact")
    temp.append(df_fc_1.loc[row["ID"],"Website"])
    contact_fc.append(temp)


df_contact_fc = pd.DataFrame(contact_fc)
print (df_contact_fc.head(5))

contact_array_list = []
#
for index, row in df_final.iterrows():
    if ((not str(row["ID_inc42"])== "nan") and (not str(row["Contact Email"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append("email")
        temp.append(row["Contact Email"])
        temp.append("general")
        temp.append("inc42")
        temp.append(row["Website"])
        contact_array_list.append(temp)
        print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Ph no"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append("Ph no")
        temp.append(row["Ph no"])
        temp.append("general")
        temp.append("Owler")
        temp.append(row["Website"])
        contact_array_list.append(temp)
        # print (temp)

df_contact_inc = pd.DataFrame(contact_array_list)
# print (df_contact_inc.tail(10))

df_contact = df_contact_inc.append(df_contact_fc, verify_integrity= False)
df_contact.columns = ["ID","type","email/phone","Label","Source","domain"]
print(df_contact.head(5))

'''
Writing it to excel - Company_Social
'''
to_write = df_contact[["ID","type","email/phone","Label","Source","domain"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_Contact.xlsx')
to_write.to_excel(writer,'email_phone')
writer.save()



'''
---------------------------For Description Worksheet-----------------------------------------------
'''

df_fc_bio = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'social_info')

bio_fc = []

for index, row in df_fc_bio.iterrows():
    temp = []
    temp.append(row["ID"])
    temp.append(row["type_name"])
    temp.append(row["bio"])
    temp.append("Full Contact")
    temp.append(df_fc_1.loc[row["ID"],"Website"])
    bio_fc.append(temp)

df_bio_fc = pd.DataFrame(bio_fc)
print (df_bio_fc.head(5))


bio_array_list = []

for index, row in df_final.iterrows():
    if ((not str(row["ID_inc42"])== "nan") and (not str(row["Description"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append("short description")
        temp.append(row["Description"])
        temp.append("inc42")
        temp.append(row["Website"])
        bio_array_list.append(temp)
        print (temp)
    elif ((not str(row["ID_FC"])== "nan") and (not str(row["short_description"]) == "-")):
        temp = []
        temp.append(row["ID_FC"])
        temp.append("short description")
        temp.append(row["short_description"])
        temp.append("Full Contact")
        temp.append(row["Website"])
        bio_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Sort Description"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append("Sort Description")
        temp.append(row["Sort Description"])
        temp.append("Owler")
        temp.append(row["Website"])
        bio_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Long Description"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append("Long Description")
        temp.append(row["Long Description"])
        temp.append("Owler")
        temp.append(row["Website"])
        bio_array_list.append(temp)
        # print (temp)


df_bio_inc = pd.DataFrame(bio_array_list)
# print (df_contact_inc.tail(10))

df_desc = df_bio_inc.append(df_bio_fc, verify_integrity= False)
df_desc.columns = ["ID","type","Document","Source","domain"]

print(df_desc.head(10))
print(df_desc.tail(10))

'''
Writing it to excel - Company_Social
'''
to_write = df_desc[["ID","type","Document","Source","domain"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_Description.xlsx')
to_write.to_excel(writer,'Description')
writer.save()



'''
---------------------------For Location and Addresss Worksheet-----------------------------------------------
'''

df_fc_address = pd.read_excel('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/Full Contact/fullcontact_company_Excel.xlsx',
                           sheetname = 'address')
address_fc = []

for index, row in df_fc_address.iterrows():
    temp = []
    temp.append(row["ID"])
    ad_line = str(row["address_line1"]) + " | " + str(row["address_line2"])
    temp.append(ad_line)
    temp.append(row["locality"])
    temp.append(row["region_name"])
    temp.append(row["country_name"])
    temp.append(row["postal_code"])
    temp.append("Full Contact")
    temp.append(df_fc_1.loc[row["ID"],"Website"])
    address_fc.append(temp)
    # print (len(temp))

df_address_fc = pd.DataFrame(address_fc)
# print (df_address_fc.head(5))


address_array_list = []

for index, row in df_final.iterrows():
    if ((not str(row["ID_inc42"])== "nan") and (not str(row["City"]) == "nan")):
        temp = []
        temp.append(row["ID_inc42"])
        temp.append("NA")
        temp.append(row["City"])
        temp.append("NA")
        temp.append("NA")
        temp.append("NA")
        temp.append("inc42")
        temp.append(row["Website"])
        address_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID_FC"])== "nan") and (not str(row["City"]) == "nan")):
        temp = []
        temp.append(row["ID_FC"])
        temp.append("NA")
        temp.append(row["City"])
        temp.append("NA")
        temp.append("NA")
        temp.append("NA")
        temp.append("Full Contact")
        temp.append(row["Website"])
        address_array_list.append(temp)
        # print (temp)
    elif ((not str(row["ID"])== "nan") and (not str(row["Location"]) == "-")):
        temp = []
        temp.append(row["ID"])
        temp.append(row["Address"])
        for item in str(row["Location"]).split(","):
            temp.append(item)
        # temp.append("")
        # temp.append("")
        temp.append("NA")
        temp.append("Owler")
        temp.append(row["Website"])
        address_array_list.append(temp)
        # print (len(temp))



df_address_inc = pd.DataFrame(address_array_list)
print (df_address_inc.head(5))
df_address_inc.drop(df_address_inc.columns[[8,9]], axis=1, inplace=True)
print (df_address_inc.head(5))

df_address = df_address_inc.append(df_address_fc, verify_integrity= False)
df_address.columns = ["ID","Address","City","State","Country","Postal Code", "Source","Domain"]

print(df_address.head(10))
print(df_address.tail(10))

'''
Writing it to excel - Company_Address&Location
'''
to_write = df_address[["ID","Address","City","State","Country","Postal Code", "Source","Domain"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_location.xlsx')
to_write.to_excel(writer,'Address_location')
writer.save()


'''
---------------------------For Founder Worksheet-----------------------------------------------
'''

df_founders = df_final[["ID_inc42","ID_FC","ID","Website","Founders"]]

print (df_founders.head(5))

founder_array = []
for index, row in df_founders.iterrows():
    content = str(row["Founders"])
    founder_list = content.split(",")
    id_inc = row["ID_inc42"]
    id_fc = row["ID_FC"]
    id_ow = row["ID"]
    web = row["Website"]
    for item in founder_list:
        temp = []
        founder_name = item.strip()
        temp.append(id_inc)
        temp.append(id_fc)
        temp.append(id_ow)
        temp.append(web)
        temp.append(founder_name)
        founder_array.append(temp)

print (founder_array[10])

df_founder_list = pd.DataFrame(founder_array)
df_founder_list.columns = ["ID_inc42","ID_FC","ID","Website","Founders"]

'''
Writing it to excel - Founders
'''
to_write = df_founder_list[["ID_inc42","ID_FC","ID","Website","Founders"]]
# print (to_write)
writer = pd.ExcelWriter('/Users/Ankan/Documents/Inc42_Work_Related/Inc42_data/Nucleus42/Company/Final Data Sheet/Database Making/1stAug/Airtable_Bases/Indian_Funding_DataBase/Final/all_sheets/Company_Founders.xlsx')
to_write.to_excel(writer,'Founders')
writer.save()


'''
---------------------------For Transaction Worksheet-----------------------------------------------
'''


'''
---------------------------For investor Worksheet-----------------------------------------------
'''

