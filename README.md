# PM4Sand3D_drivers_auto
## Scripts that produce multiple PM4Sand3D drivers for different loading paths, batch files for running them in FLAC 3D/9.X, and post-processing codes for plotting
### Original versions of processing and plotting files created by M-P Kippen in the framework of the PM4Sand3D development, May 2021

### v1.0 June 2026

### Structure

- Three folder structure (for now)
- PM4Sand3D* folders contain drivers and processing* folder contains post-processing and plotting files
- Each PM4Sand* folder provides the ability to create multiple FLAC *.f3fis drivers that cover various parameters and are named accordingly. A batch*.f3fis file is also produced that can be directly called in FLAC3D that will run them all and produce csv files with results in the same folder.
- Each plotting*.py file in the "processing_plotting" folder will process different drivers and produce Figures. Decode python file contains useful functions for all and ucdavis.mplstyle is used for figure styling.

### Driver details
#### PM4Sand3D_Cyclic_DSS_MRD_batch
Produces strain controlled drained Direct Simple Shear drivers. Each driver features five elements, each at a different overburden. User can select relative densities. Options for exercising at a range of strains for a certain number of cycles at each one (will produce Modulus Reduction and Damping curves) or applying uniform cycles at the same shear strains for multiple cycles (will produce volumetric response). This can be controlled by the "volumetric" parameter.

#### PM4Sand3D_Cyclic_DSS_undrained_batch
Produces stress controlled undrained Direct Simple Shear drivers. Each driver features five elements, each at a different CSR. Middle element is exercised under the CRR of the relative density (set internally in DSS_cyclic_undrained.fis). User can select relative densities, overburdens, static shear stress bias values, and Ko values.

#### PM4Sand3D_Cyclic_TXC_undrained_batch
Produces undrained cyclic triaxial compression (TXC) drivers. Similar philosophy to DSS ones.

#### PM4Sand3D_mono_DSS_PSC_TXC_batch
Produces monotonic, drained and undrained, direct simple shear (DSS), plane-strain compression (PSC), and triaxial compression (TXC drivers)

---
Please send your comments, bugs, issues and features to add to [Katerina Ziotopoulou] at katerinaziot@gmail.com.
