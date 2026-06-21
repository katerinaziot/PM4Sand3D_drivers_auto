#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday June 19 2025
@author: kziot


- File opens Template with header line info, writes parametrically varying 
  parameters underneath, writes complete contents of DSS_cyclic_drained.f3fis file
  sets savefile information (for *.sav in running FLAC3D) and closes it
- Each produced *.f3fis file is named according to the varied parameters
- a batch_drainedDSS_vol.f3fis or batch_drainedDSS_MRD.f3fis is produced populated by call commands for each file
  generated for later being called in FLAC
- As of now, placeholders for relative density (can be provided with 1 or more array values)
  number of cycles to be performed at each strain limit (degradation), and maximum strain
  to be reached by each driver
- if 'volumetric' set to 1 then files are produced that apply uniform strain controlled @1% loading for a maximum
  number of cycles / if not the file produces files for MRD curves that exercise the element for Ncyc across an 
  array of shear strains
- all other variables are defined inside DSS_cyclic_drained.f3fis and can be either
  changed within (if constant across all drivers) or brought herein to be added as 
  other array to be iterated over following the same philosophy
- only batch_drainedDSS_***.f3fis file needs to be called by FLAC3D
- CAUTION: file naming conventions intimately related to post-processing & plotting protocols
"""
import os 
# Get absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory where results will be produced and run (to keep separate from script)
produce_dir = os.path.join(script_dir, r"results")

# Input Parameters
Soil     = ""
TestName = "dDSS" # will match template Driver and built upon that

# Create arrays of values to be varied across all Drivers
# Produced files will be named accordingly
volumetric  = 1
Dr          = [0.35, 0.55, 0.75]    # Relative Density
Ncyc        = [20]                   # Number of Cycles to be performed at each strain
gamma_count = [8]                   # Stop at this value in limit array(10) [index in array]

# Dictionary that matches strain array index to actual maximum strain reached in driver
gamma_dict = {1:"0.0003p",2:"0.001p",3:"0.003p",4:"0.01p",5:"0.03p",6:"0.1p",7:"0.3p",8:"1p",9:"3p",10:"10p"}

Test_File     = os.path.join(script_dir, "DSS_cyclic_drained.f3fis")
Template_File = os.path.join(script_dir, "templ_drDSScyc.f3fis")

# Initialize lines for final batch file
call_line   = 'program call \'#\'\n'
batch_lines = []

if volumetric  != 1:
  for Dr_i in Dr:
      for Ncyc_i in Ncyc:
          for gamma_count_i in gamma_count:
                # First create a file name 
                BaseFile = TestName+Soil+ "_MRD" + "_Dr" +str(int(Dr_i*100))+"_Ncyc"+str(Ncyc_i)+"_max"+str(gamma_dict[gamma_count_i])
                FileName = os.path.join(produce_dir, BaseFile + ".f3fis")
                FileName_in_BatchFile = os.path.join(BaseFile + ".f3fis")

                # Create a new file and open template and test file
                fileID 			= open(FileName,"w+");
                Template_fileId = open(Template_File,"r");
                Test_fileId     = open(Test_File,"r")

                # Writing to a file
                fileID.write(Template_fileId.read())
                fileID.write("\n\n")

                fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
                fileID.write("fish def _var_inputs\n")
                fileID.write("\t_Dr           = " + str(Dr_i) + " \n")
                fileID.write("\t_nCycles      = " + str(Ncyc_i) + " \n")
                fileID.write("\t_strainCount  = " + str(gamma_count_i) + " \n")
                fileID.write("\t_basefile     = \'" + BaseFile + "\' \n")
                fileID.write("end \n");
                fileID.write("[_var_inputs]\n\n")

                fileID.write(Test_fileId.read())

                fileID.write(";-------------Footer-------------------\n")
                fileID.write(";save @_savefile\n")
                fileID.write(";--------------------------------------\n")

                # Closing the files
                Test_fileId.close()
                Template_fileId.close()
                fileID.close()
                batch_lines.append(call_line.replace("#", FileName_in_BatchFile)+"\n")

  batch_file_path = os.path.join(produce_dir, "batch_drainedDSS_MRD.f3fis")
  batch_file = open(batch_file_path, "w")

else:
  for Dr_i in Dr:
      for Ncyc_i in Ncyc:
                # First create a file name 
                BaseFile = TestName+ Soil +"_vol"+ "_Dr"+str(int(Dr_i*100))+"_Ncyc"+str(Ncyc_i)+"_max"+str(gamma_dict[8])
                FileName = os.path.join(produce_dir, BaseFile + ".f3fis")
                FileName_in_BatchFile = os.path.join(BaseFile + ".f3fis")

                # Create a new file and open template and test file
                fileID          = open(FileName,"w+");
                Template_fileId = open(Template_File,"r");
                Test_fileId     = open(Test_File,"r")

                # Writing to a file
                fileID.write(Template_fileId.read())
                fileID.write("\n\n")

                fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
                fileID.write("fish def _var_inputs\n")
                fileID.write("\t_Dr           = " + str(Dr_i) + " \n")
                fileID.write("\t_nCycles      = " + str(Ncyc_i) + " \n")
                fileID.write("\t_strainCount = 1                   \n")
                fileID.write("\t_basefile     = \'" + BaseFile + "\' \n")
                fileID.write("end \n");
                fileID.write("[_var_inputs]\n\n")

                fileID.write(Test_fileId.read())

                fileID.write(";-------------Footer-------------------\n")
                fileID.write(";save @_savefile\n")
                fileID.write(";--------------------------------------\n")

                # Closing the files
                Test_fileId.close()
                Template_fileId.close()
                fileID.close()
                batch_lines.append(call_line.replace("#", FileName_in_BatchFile)+"\n")

  batch_file_path = os.path.join(produce_dir, "batch_drainedDSS_vol.f3fis")
  batch_file = open(batch_file_path, "w")

batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write(";                     FLAC3D batch calling of input files               \n")
batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write("\n")
batch_file.writelines(batch_lines)
batch_file.close()
''' EoF'''
