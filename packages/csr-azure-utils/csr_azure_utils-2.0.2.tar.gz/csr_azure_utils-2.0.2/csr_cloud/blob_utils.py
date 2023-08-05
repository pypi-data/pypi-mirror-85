#!/usr/bin/env python

'''
Cisco Copyright 2018
Author: Abhinav Sanakkayala <asanakka@cisco.com>




'''
from __future__ import print_function
from builtins import object
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContentSettings
import logging

log = logging.getLogger('csr_tvnet')

class BlobUtils(object):
    def __init__(self, account_name, account_key):

        self.blob_service_client = BlobServiceClient(
            account_url="http://"+account_name+".blob.core.windows.net", 
            credential=account_key)

    def create_container_if_doesnt_exist(self, containername):
        if self.does_container_exist(containername) is False:
            self.blob_service_client.create_container(containername)

    def download_file_from_container(self, containername, filename, directory="/bootflash/"):
        try:
            blob_client=self.blob_service_client.get_blob_client(
                container=containername, blob=filename)
            
            with open((directory+filename), "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
        except Exception as e:
            log.exception("Config File Download Failed.  Error: %s" % e)
            return False
        
        print("\nDownload Complete")
        return True

    def upload_file_to_container(self, containername, filename, directory="/bootflash/"):
        self.create_container_if_doesnt_exist(containername)
        try:
            blob_client=self.blob_service_client.get_blob_client(
                container=containername, blob=filename)
            
            with open((directory+filename), "rb") as data:
                blob_client.upload_blob(data)
        except Exception as e:
            print("Uploading %s Failed.  Error: %s" % (filename, e))
            return False

        print("Upload Complete to container %s" % (containername))
        return True

    def does_container_exist(self, containername):
        containers = self.blob_service_client.list_containers()

        for c in containers:
            if containername is c.name:
                return True
        return False
