#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
# Step 1) Open Chrome
browser = webdriver.Chrome()
# Step 2) Navigate to Facebook
#reads the GD tracker and thaeles tracker to find which sites need to have forms automatically
#generated. It finds the FA number of the sites on the Thaeles tracker 
# that are New Site 7/1/21 in the subbed for review column, and then finds the corresponding
#Charge Code for those sites
thaeles = "thaeles_tracker.csv"
df = pd.read_csv(thaeles, usecols = ['FA #','SITE NAME','Subbed for Review'])

sites_ok_submit_weekly = "july23rd_sites.csv"
sites_list_july23 = pd.read_csv(sites_ok_submit_weekly, usecols = ['FA #'])

gd = "gd_tracker.csv"
df1 = pd.read_csv(gd, usecols = ['P:Project Key (Charge Code or PACE ID)','S:FA Number','S:Site Name','S:Address Line 1','S:City','S:State','S:ZIP'])
    #goes through the thaeles tracker to find the sites that need to have forms generated. 
    #It does this by looking in the subbed for view column and finding new sites
FA_Sites_That_Need_Forms= []
for i in range (1,207):
    if (df['Subbed for Review'][i] == 'New Site 7/1/21'):
        FA_Sites_That_Need_Forms.append(df['FA #'][i])
    #goes through the GD one tracker to find the corresponding charge code number to the sites
    #found using FA Sites that need forms function. The contents of this array eventually are
    #going to be plugged into the FormGenerator file#
ChargeCodeFinderforForms= []
for j in range (0,264):
    for i in range (0,len(FA_Sites_That_Need_Forms)):
        if (FA_Sites_That_Need_Forms[i] == df1['S:FA Number'][j]):
            ChargeCodeFinderforForms.append(df1['P:Project Key (Charge Code or PACE ID)'][j])
#find the charge code, and site name given an FA number
window_origional = browser.window_handles[0]
browser.switch_to_window(window_origional)
#find the charge code, and site name given an FA number
array_FA_Site_name_Charge_Code=[]                                              


# In[2]:


def ListofChargeCode_SiteName_andFA (chargecode):
    array_FA_Site_name_Charge_Code.clear()
    for j in range (0,len(df1)):
        if (df1['P:Project Key (Charge Code or PACE ID)'][j]== chargecode):
            array_FA_Site_name_Charge_Code.append((df1['P:Project Key (Charge Code or PACE ID)'][j],
                                                   df1['S:FA Number'][j], df1['S:Site Name'][j],df1['S:Address Line 1'][j],
                                                 df1['S:City'][j],df1['S:State'][j],df1['S:ZIP'][j]))
def login():
    browser.get("https://gd.onevizion.com/Login.do")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    submit   = browser.find_element_by_id("btn")
    username.send_keys("henry@thaelesinc.com")
    password.send_keys("Gravity981*")
    # Step 4) Click Login
    submit.click()
    time.sleep(15)
    # Step 5) get it to the list of projects
    firststep = browser.find_element_by_id("mainLogo")
    time.sleep(7)
    firststep.click()
    openprojectlist = browser.find_element_by_id("itemMenu_10017715_10020705")
    openprojectlist.click()
    
def searchByChargeCode(chargecode):
#searches the project page for the charge code. Selects the charge code search term and
#then searches for the charge code in the search box. We did this to bypass having to scroll
#and click through multiple pages to find elements
    searchByChargeCode = browser.find_element_by_id('qsField0')
    searchByChargeCode.click()
    clickonSearch = browser.find_element_by_id("qsValue0")
    clickonSearch.send_keys(Keys.ENTER)
    clickonSearch.send_keys(Keys.CONTROL, 'a')
    length = len(clickonSearch.get_attribute('value'))
    clickonSearch.send_keys(length*Keys.BACKSPACE)
    clickonSearch.send_keys(chargecode)
    

def CreateInFormTab(chargecode):
    #Creates a form given a charge code and inputs the basic values needed to instantiate a form
    chargeCode=browser.find_element_by_link_text( chargecode )
    chargeCode.click()
    window_after = browser.window_handles[1]
    browser.switch_to_window(window_after)
    clickonform = browser.find_element_by_id("tab10")
    clickonform.click()
    time.sleep(7)
    addform = browser.find_element_by_id("btnAdd10")
    addform.click()
            #creating a form
    window_after1 = browser.window_handles[2]
    browser.switch_to_window(window_after1)
    #fills in the bare bones of a form to generate a form
    vendor= browser.find_element_by_id("idx6_disp")
    gen12 = browser.find_element_by_id("idx12")
    formsubmitedby   = browser.find_element_by_id("idx14_disp")
    primaryrev   = browser.find_element_by_id("idx19_disp")
    secondaryrev   = browser.find_element_by_id("idx20_disp")
    vendor.send_keys("1282 (BRIUS TELECOM SOLUTIONS LLC)")
    vendor.send_keys(Keys.ENTER)
    formsubmitedby.send_keys("henry@thaelesinc.com")
    formsubmitedby.send_keys(Keys.ENTER)
    primaryrev.send_keys("Brian.Gullen@gdit.com")
    primaryrev.send_keys(Keys.ENTER)
    secondaryrev.send_keys("Melissa.Martins@gdit.com")
    secondaryrev.send_keys(Keys.ENTER)
    gen12.click()
    select = Select(browser.find_element_by_id('idx12'))
    select.select_by_value('10012143')
    #clicking on the OK button to close out the form
    submitbuttonform= browser.find_element_by_id("btnOK")
    submitbuttonform.click()
    browser.switch_to_window(window_after)
    #closes back to origional project
    submitbuttonform1= browser.find_element_by_id("btnOK")
    submitbuttonform1.click()
def projectpage():
    first_window =browser.window_handles[0]
    browser.switch_to_window(first_window)
    firststep = browser.find_element_by_id("mainLogo")
    time.sleep(7)
    firststep.click()
    openprojectlist = browser.find_element_by_id("itemMenu_10017715_10020705")
    openprojectlist.click()
    
def fillinvalues(chargecode):
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx56')).perform()
    filerev   = browser.find_element_by_id("idx56")
    
    filerev.send_keys(Keys.CONTROL, 'a')
    length = len(filerev.get_attribute('value'))
    filerev.send_keys(length*Keys.BACKSPACE)
    
    filerev.send_keys("Henry French")
    filerev.send_keys(Keys.ENTER)
    #input Natural Gas Provider 
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx69')).perform()
    natgas2   = browser.find_element_by_id("idx69")
    
    natgas2.send_keys(Keys.CONTROL, 'a')
    length1 = len(natgas2.get_attribute('value'))
    natgas2.send_keys(length1*Keys.BACKSPACE)
    
    natgas2.send_keys("N/A")
    natgas2.send_keys(Keys.ENTER)
    #input Proposed Generator lease spease 
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx71')).perform()
    propleasespace   = browser.find_element_by_id("idx71")
    
    propleasespace.send_keys(Keys.CONTROL, 'a')
    length2 = len(propleasespace.get_attribute('value'))
    propleasespace.send_keys(length2*Keys.BACKSPACE)
    
    propleasespace.send_keys("4'x10'+ concrete pad")
    propleasespace.send_keys(Keys.ENTER)
    #input MLA/SLA available
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx89')).perform()
    mlasla = browser.find_element_by_id("idx89")
    mlasla.click()
    select2 = Select(browser.find_element_by_id('idx89'))
    select2.select_by_value('10019358')
    mlasla.send_keys(Keys.ENTER)
    #input Lease Doc. Available
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx91')).perform()
    docavail = browser.find_element_by_id("idx91")
    docavail.click()
    select3 = Select(browser.find_element_by_id('idx91'))
    select3.select_by_value('10019358')
    docavail.send_keys(Keys.ENTER)
    #input Proposed Generator lease spease 
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx108')).perform()
    leasefees   = browser.find_element_by_id("idx108")
    
    leasefees.send_keys(Keys.CONTROL, 'a')
    length3 = len(leasefees.get_attribute('value'))
    leasefees.send_keys(length3*Keys.BACKSPACE)
    
    leasefees.send_keys("TBD")
    leasefees.send_keys(Keys.ENTER)
    #Leade Doc Comments
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx92')).perform()
    leasedoccom   = browser.find_element_by_id("idx92")
    
    leasedoccom.send_keys(Keys.CONTROL, 'a')
    length4 = len(leasedoccom.get_attribute('value'))
    leasedoccom.send_keys(length4*Keys.BACKSPACE)
    
    leasedoccom.send_keys("SLA + LDS")
    leasedoccom.send_keys(Keys.ENTER)
    #lease Sketch, N/A
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx97')).perform()
    leasesketch   = browser.find_element_by_id("idx97")
    
    leasesketch.send_keys(Keys.CONTROL, 'a')
    length5 = len(leasesketch.get_attribute('value'))
    leasesketch.send_keys(length5*Keys.BACKSPACE)
    
    leasesketch.send_keys("N/A")
    leasesketch.send_keys(Keys.ENTER)
    #title comments, no survey available
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx101')).perform()
    titleCom   = browser.find_element_by_id("idx101")
    
    titleCom.send_keys(Keys.CONTROL, 'a')
    length6 = len(titleCom.get_attribute('value'))
    titleCom.send_keys(length6*Keys.BACKSPACE)
    
    titleCom.send_keys("no survey available")
    titleCom.send_keys(Keys.ENTER)
    ListofChargeCode_SiteName_andFA(chargecode)
    #inputFAnumber
    favar=str(array_FA_Site_name_Charge_Code[0][1])
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx48')).perform()
    fanumber   = browser.find_element_by_id("idx48")
    
    fanumber.send_keys(Keys.CONTROL, 'a')
    length7 = len(fanumber.get_attribute('value'))
    fanumber.send_keys(length7*Keys.BACKSPACE)
    
    fanumber.send_keys(favar)
    fanumber.send_keys(Keys.ENTER)
    sitevar=str(array_FA_Site_name_Charge_Code[0][2])
    #inputsitenumber
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx50')).perform()
    sitenumber   = browser.find_element_by_id("idx50")
    
    sitenumber.send_keys(Keys.CONTROL, 'a')
    length8 = len(sitenumber.get_attribute('value'))
    sitenumber.send_keys(length8*Keys.BACKSPACE)
    
    sitenumber.send_keys(sitevar)
    sitenumber.send_keys(Keys.ENTER)
    #input address line one
    addyvar= str(array_FA_Site_name_Charge_Code[0][3])
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx52')).perform()
    addy1   = browser.find_element_by_id("idx52")
    
    addy1.send_keys(Keys.CONTROL, 'a')
    length9 = len(addy1.get_attribute('value'))
    addy1.send_keys(length9*Keys.BACKSPACE)
    
    addy1.send_keys(addyvar)
    addy1.send_keys(Keys.ENTER)
    #input address line 2
    addyvar2= str(array_FA_Site_name_Charge_Code[0][4]), str( array_FA_Site_name_Charge_Code[0][5]), str( array_FA_Site_name_Charge_Code[0][6])
    addyvar2final= addyvar2[0]+" , "+ addyvar2[1]+" "+ addyvar2[2]
    ActionChains(browser).move_to_element(browser.find_element_by_id('idx54')).perform()
    addy2   = browser.find_element_by_id("idx54")
    
    addy2.send_keys(Keys.CONTROL, 'a')
    length10 = len(addy2.get_attribute('value'))
    addy2.send_keys(length10*Keys.BACKSPACE)
    
    addy2.send_keys(addyvar2final)
    addy2.send_keys(Keys.ENTER)

    clickok_onform = browser.find_element_by_id("btnOK")
    clickok_onform.click()
    clickok_onform.click()
    browser.switch_to_window(browser.window_handles[1])
    clickok_onform = browser.find_element_by_id("btnOK")
    clickok_onform.click()
    browser.switch_to_window(window_origional)

def ChargeCodeEnter():
#searches the project page for the charge code. Selects the charge code search term and
#then searches for the charge code in the search box. We did this to bypass having to scroll
#and click through multiple pages to find elements
    searchcode = browser.find_element_by_id("qsValue0")
    searchcode.send_keys(Keys.ENTER)
def fillInTopofFormTab(chargecode):
    #Creates a form given a charge code and inputs the basic values needed to instantiate a form
    chargeCode=browser.find_element_by_link_text(array_chargecode_excel[0] )
    chargeCode.click()
    window_after = browser.window_handles[1]
    browser.switch_to_window(window_after)
    clickonform = browser.find_element_by_id("tab10")
    clickonform.click()
    time.sleep(7)
    editform = browser.find_element_by_id("btnEdit10")
    editform.click()
            #opening the form to edit
    window_after1 = browser.window_handles[2]
    browser.switch_to_window(window_after1)
    clickontopbutton = browser.find_element_by_id("search_formTabsSearch")
    clickontopbutton.click()
    clickontopbutton.send_keys(Keys.ARROW_DOWN,Keys.ENTER)
    #fills in the bare bones of a form to generate a form
    #input File reviewer
    time.sleep(5)
    fillinvalues(chargecode)
#function to look through uploaded cvs file, and find the corresponding FA number for those sites

array_chargecode_excel=[]
def getChargeCodeGivenFA (fa):
    array_chargecode_excel.clear()
    for j in range (0,len(df1)):
        if (df1['S:FA Number'][j]== fa):
            array_chargecode_excel.append((df1['P:Project Key (Charge Code or PACE ID)'][j]))                                               


# In[3]:


login()


# In[5]:


for i in range (7,len(sites_list_july23['FA #'])):
    getChargeCodeGivenFA(sites_list_july23['FA #'][i])
    x=array_chargecode_excel[0]
    searchByChargeCode(x)
    time.sleep(7)
    ChargeCodeEnter()
    time.sleep(7)
    fillInTopofFormTab(x)


# In[18]:


getChargeCodeGivenFA(sites_list_july23['FA #'][7])
x=array_chargecode_excel[0]
searchByChargeCode(x)


# In[21]:


ChargeCodeEnter()


# In[22]:


CreateInFormTab(x)


# In[27]:





# In[83]:





# In[40]:





# In[41]:





# In[42]:





# In[93]:





# In[85]:





# In[88]:





# In[89]:





# In[ ]:




