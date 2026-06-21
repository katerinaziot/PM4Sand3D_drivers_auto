#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: kziot, mpkippen

- File opens Template with header line info, writes parametrically varying 
  parameters underneath, writes complete contents of DSSmono.fis file
  sets savefile information (for *.sav in running FLAC3D) and closes it
- Each produced *.f3fis file is named according to the varied parameters
- a batch_DSS_mono.f3fis is produced populated by call commands for each file
  generated for later being called in FLAC3D
- As of now, placeholders for relative density (can be provided with 1 or more array values)
  and the drainage conditions have been used
- all other variables are defined inside DSSmono.f3fis and can be either
  changed within (if constant across all drivers) or brought herein to be added as
  other array to be iterated over following the same philosophy
- only batch_DSS_mono.fis file needs to be called by FLAC3D
- original file in Matlab by kziot, then modified for python by kziot
"""
import os
# Get absolute path to the directory where this script is located
script_dir  = os.path.dirname(os.path.abspath(__file__))

# Define the directory where results will be produced and run (to keep separate from script)
produce_dir = os.path.join(script_dir, r"results")

# Input Parameters - CHANGE HERE BETWEEN PSC and DSS
Soil     = ""
#TestName       = "PS"           
#batch_FileName = "batch_PSC_mono.f3fis"     # 'batch_DSS_mono.fis'
#TestName       = "TXC"           
#batch_FileName = "batch_TXC_mono.f3fis"
TestName       = "DSS"
batch_FileName = "batch_DSS_mono.f3fis"    # 'batch_DSS_mono.fis'

Test_File      = os.path.join(script_dir, "DSS_monotonic.f3fis")
Template_File  = os.path.join(script_dir, "templ_DSSmono.f3fis")

# Create arrays of values to be varied across all Drivers
# Produced files will be named accordingly
Dr        = [0.35, 0.55, 0.75]    # Relative Density
drainage  = [0, 1]                # 0 for undrained, 1 for drained
CompExt   = [1,-1]                # 1 for compression, -1 for Extension

drain_dict  = {0:"u",1:"d"}
PS_dict     = {1:"C",-1:"E"}
TX_dict     = {1:"C", -1:"E"}

# Initialize lines for final batch file
call_line   = 'program call \'#\'\n'
batch_lines = []

if TestName == "PS":
  for CompExt_i in CompExt:
    for drainage_i in drainage:
      for Dr_i in Dr:
        BaseFile = str(drain_dict[drainage_i]) + TestName +str(PS_dict[CompExt_i]) + "_mono" + Soil + "_Dr" + str(int(Dr_i*100))
        FileName = os.path.join(produce_dir, BaseFile + ".f3fis")
        FileName_in_BatchFile = BaseFile + ".f3fis"

        fileID = open(FileName,"w+")
        Template_fileId = open(Template_File,"r")
        Test_fileId = open(Test_File,"r")

        fileID.write(Template_fileId.read())
        fileID.write("\n\n")

        fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
        fileID.write("fish def _var_inputs\n")
        fileID.write("\t_Dr          = " + str(Dr_i) + " \n")
        fileID.write("\t_drained     = " + str(drainage_i) + " \n")
        fileID.write("\t_Compr_Ext   = " + str(CompExt_i) + " \n")
        fileID.write("\t_basefile    = \'" + BaseFile +"_" +"\' \n")

        fileID.write("end \n")
        fileID.write("[_var_inputs]\n\n")

        fileID.write(Test_fileId.read())

        fileID.write(";-------------Footer-------------------\n")
        fileID.write(";save @_savefile\n")
        fileID.write(";--------------------------------------\n")

        Test_fileId.close()
        Template_fileId.close()
        fileID.close()
        batch_lines.append(call_line.replace("#", FileName_in_BatchFile)+"\n")
else:
  for drainage_i in drainage:
    for Dr_i in Dr:
      BaseFile = str(drain_dict[drainage_i]) + TestName + "_mono" + Soil + "_Dr" + str(int(Dr_i*100))
      FileName = os.path.join(produce_dir, BaseFile + ".f3fis")
      FileName_in_BatchFile = BaseFile + ".f3fis"

      fileID = open(FileName,"w+")
      Template_fileId = open(Template_File,"r")
      Test_fileId = open(Test_File,"r")

      fileID.write(Template_fileId.read())
      fileID.write("\n\n")

      fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
      fileID.write("fish def _var_inputs\n")
      fileID.write("\t_Dr          = " + str(Dr_i) + " \n")
      fileID.write("\t_drained     = " + str(drainage_i) + " \n")
      fileID.write("\t_basefile    = \'" + BaseFile +"_" +"\' \n")

      fileID.write("end \n")
      fileID.write("[_var_inputs]\n\n")

      fileID.write(Test_fileId.read())

      fileID.write(";-------------Footer-------------------\n")
      fileID.write(";save @_savefile\n")
      fileID.write(";--------------------------------------\n")

      Test_fileId.close()
      Template_fileId.close()
      fileID.close()
      batch_lines.append(call_line.replace("#", FileName_in_BatchFile)+"\n")

batch_file_path = os.path.join(produce_dir,batch_FileName)
batch_file = open(batch_file_path, "w")

batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write(";                     FLAC batch calling of input files                 \n")
batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write("\n")
batch_file.writelines(batch_lines)
batch_file.close()
''' EoF'''