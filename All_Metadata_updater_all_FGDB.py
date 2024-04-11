import os
import arcpy

from arcpy import metadata as md

#
#
# ENTER Location of Source Metadata in XML File
#
src_csdgm_file = "/EsriTraining/INDR/geodatabase_metadata.xml"

import os

#
#
# ENTER Root Folder Location to start search for Geodatabases
#
rootDir = r"C:\EsriTraining\INDR"

gdbList = []

#
#
# Search root Location for File Geodatabases
#
for dirPath, dirNames, fileNames in os.walk(rootDir, topdown=True):
   if dirPath.endswith(".gdb") or ".gdb." in dirPath:
      file_gdb = dirPath

      print (" ")
      print ("------- Next File Geodatabase ------------------- ")
      print (" ")
      print ("File geodatabase --> ",file_gdb)
      print (" ")
      gdbList.append(dirPath)

      arcpy.env.workspace = file_gdb

#
#
# Get List of All Feature Datasets in the Geodatabase
#
      datasets = arcpy.ListDatasets("", "Feature")

      print (" ")
      print (" ")
      print ("All Feature Datasets in the Geodatabase ",datasets)
      print (" ")

      fd_path_list = [ ]
      fd_name_dict = { }

#
#
# For Each Feature Datasets Get List of Feature Classes within
#
      for feature_dataset in datasets:
          fd_path = os.path.join(file_gdb, feature_dataset)

          fd_path_list.append(fd_path)
          fd_name_dict[fd_path] = str(feature_dataset)

          print (" ")
          print (" ")
          print (fd_path, " <--- Feature Dataset ")
          print (" ")

#
#
# For Each Feature Datasets Update the Metadata
#
          tgt_item_md = md.Metadata(fd_path)
          tgt_item_md.importMetadata(src_csdgm_file,"ARCGIS_METADATA")

#
#
# Change the Title for the Metadata to the Feature Dataset name
#
          tgt_item_md.title = feature_dataset

          tgt_item_md.save()
   
          for fd in fd_path_list:
              fc_path_list_WD = [ ]
              fc_path_list_WED = [ ]
              arcpy.env.workspace = fd
              featureclasses = arcpy.ListFeatureClasses()
 
#
#
# For Each Feature Class in the Feature Datasets Update the Metadata
#
          for fc in featureclasses:
        
              fc_path = os.path.join(fd_path, fc)
              print (fc_path)
              tgt_item_md = md.Metadata(fc_path)

              tgt_item_md.importMetadata(src_csdgm_file,"ARCGIS_METADATA") 

#
#
# Change the Title for the Metadata to the Feature Classes name
#
              tgt_item_md.title = fc
	
              tgt_item_md.save()

      arcpy.env.workspace = file_gdb

      feature_classes = arcpy.ListFeatureClasses()

#
#
# For Each Feature Class not in a Feature Datasets Get List of Feature Classes
#
      print (" ")
      print (" ")
      print ("  --- Feature Classes not in a Feature Dataset --- ")
      print (" ")

      for feature_class in feature_classes:
    
          print (feature_class)
          tgt_item_md = md.Metadata(feature_class)

          tgt_item_md.importMetadata(src_csdgm_file,"ARCGIS_METADATA") 
#
#
# Change the Title for the Metadata to the Feature Classes name
#
          tgt_item_md.title = feature_class
	
          tgt_item_md.save()


      arcpy.env.workspace = file_gdb

#
#
# Get a List of tables in the Geodatabase
#
      print (" ")
      print (" ")
      print ("  --- Tables --- ")
      print (" ")
      tables = arcpy.ListTables()

      for table in tables:

          print(table)
          tgt_item_md = md.Metadata(table)
          tgt_item_md.importMetadata(src_csdgm_file,"ARCGIS_METADATA") 

#
#
# Change the Title for the Metadata to the Table name
#
          tgt_item_md.title = table

          tgt_item_md.save()

print (" ")
print (" ")
print ("all done")