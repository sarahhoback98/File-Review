#!/usr/bin/env python
# coding: utf-8

# In[1]:


#login to CEmobility


# In[2]:


#search for function in CE mobility with an FA number - $50


# In[3]:


#Find the Title document-$100
#step one sort from assending date lowest to highest
#auto scroll until the word Title is contained in the the name of one of the files
#download the copy as an origional


# In[4]:


#Find the Leasing Review document-$100
#step one sort from assending date highest to lowest
#auto scroll until the word lease review, or lease advice is contained in the the name of one of the files, 
#and is an excel
#download the copy as an origional


# In[5]:


#$200
#Document search through a folder to identify which document has the word lease data sheet
#step one, make the pdf readable
#step 2, parse through the readable pdf to find the 
#lease expiration date, lease term, lessor legal name, current lesse legal name. 
#store as a list
#if the Payable to line is different than the current lessor legal name then an additional
#element to the list , 'DBA' and put the different name here


#identify which have the name Lease Data Sheet


# In[ ]:


#$1000
#Document search through a the rest of the documents in a folder that are not the lease data sheet
#step one, make them readable
#step 2, parse through the readable pdf to find the 
#amount paid per month, increase by what percent annually,
# and square feet of the premises
#note you may have to be tricky about which key words can be used here
#perhaps you can also loop in searching through the Lease Review document
#to get a base of these elements before you parse through the documents
#as you go through the documents to find this imformation yeild to the largest number 
#found. if the information is not available then show nothing

