PassMark OSFMount V3.1
Copyright (C) 2010-2023 PassMark Software
All Rights Reserved
http://www.passmark.com 

Overview
========
OSFMount allows the analysis of disk images with PassMark OSForensics. OSFMount 
can be used to mount image files that were created using a disk cloning 
application (such as OSFClone). The image file is mounted as a virtual drive on 
Windows, which can then be analyzed using OSForensics.

OSFMount can also be used to create RAM disks and mount CD/DVD-ROMs as RAM disks.


Requirements
============
- Operating System: 64-bit Windows 7 SP1, 8, 10, 11, Server 2008 & 2012 (32-bit Windows is not supported)
- Users must have administrator privileges.
- RAM: 128MB. When mounting large disk images in memory, the more RAM the better.
- Disk space: 10 MB of free hard disk space for the installation files.


Windows Vista, XP, ME, 98, 95, NT and Server 2000 & 2003
=========================
Windows Vista, XP, ME, 98, 95, NT and Server 2000 & 2003 are not supported.

Windows Server 2016
=========================
Windows Server 2016 is not supported.

Installation
============
1) Uninstall any previous version of OSFMount. Restart your PC to ensure all 
   system files are fully uninstalled.
2) Double click (or Open) the downloaded installation ".exe" file
3) Follow the prompts


Un-install
==============
Use the Apps & Features from System Settings (Win 10), or Uninstall a program from the Control Panel (Win 7/8)


Version History
===============
Here is a summary of all changes that have been made in each version of 
OSFMount.

Release v3.1 build 1002
15 Sep 2023
- Fixed mounting of image files located on a network share using physical emulation

Release v3.1 build 1001
06 Jun 2022
- Added more verbose progress text when mounting image in CLI
- Fixed bug in mounting all partitions using the "-v all" option in CLI
- Display error when mounting physical disk with invalid MBR disk signature

Release v3.1 build 1000
05 Mar 2021
- Updated drivers built with latest WDK and disk image libraries
- Fixed OSFMount CLI usage text 
- Updated Command Line Interface section in help file with new examples

Release v3.0 build 1006
06 May 2020
- Added support for specifying 'all' to '-v' option in CLI to mount all detected partitions in image file
- Fixed error when saving a mounted logical drive greater than 4GB to an image file due to 32-bit truncation errors
- Fixed logical drives not being recognized by Windows Explorer for older O/S (eg. Win 7) when mounting via CLI

Release v3.0 build 1005
29 Jul 2019
- Added 'physical' and 'logical' command line option to force physical or logical emulation respectively
- Fixed image files being opened without share permissions

Release v3.0 build 1004
24 May 2019
- Fixed driver not being properly uninstalled when an older version is detected
- Error message now displayed when system reboot is required after driver installation

Release v3.0 build 1003
10 May 2019
- Fixed extremely slow disk performance of single part EnCase disk images inadvertently introduced by the previous fix

Release v3.0 build 1002
8 May 2019
- Fixed extremely slow disk performance of split EnCase disk images
- Fixed unable to query or dismount drive via CLI when disk is in use
- Fixed UI draw issues on Win7 Basic Theme

Release v3.0 build 1001
17 Apr 2019
- Fixed bug with error message displayed when mounting an image in read/write mode using logical emulation
- Fixed bug with ImageUSB images being mounted as CD

Release v3.0 build 1000
5 Apr 2019
- Mount a virtual disk using Physical Disk emulation, allowing the disk to be recognized by Windows Disk Management
- Added Write Cache mode to allow mounting a virtual disk as read-write while preserving the data of the original image file
- New step-by-step wizard for mounting virtual disks with simplicity
- NTFS, exFAT and FAT32 now supported when formatting a drive
- Revised columns in main window with support for physical disk emulation
- Added support in the OSFMount CLI for mounting using Physical Disk emulation

Release 2.0 build 1002
2018/06/26 <km>
- Added more robust handling of forced removing of mounted devices. This is to fix the problem of OSFMount.sys driver file still being locked.

Release 2.0 build 1001
2018/03/21 <rn>
- Updated/added warning and error messages when using format option on command line when
  specifying a ram drive that is smaller than 260MB.
- Fixed issue with detecting partitions for ImageUSB images.
- Microsoft signed OSFMount.sys driver for Windows 10 64-bit systems.

Release 2.0 build 1000
2018/03/08 <rn>
- Compiled with VS2017 and Driver Built using WinDDK 10. No longer supporting 
  older operating systems. Minimum OS required is Windows 7 SP1.
- Speed improvements for Blank RAM disks if enough physical free space is available on initial
  mounting. RAM disk will be reside in physical memory to allow faster access.
- Updated EWF library to libewf-20160424

Release 1.5 build 1018
2018/01/18 <rn>
- Fixed issue with not recognizing partitions from large E01 images after mounting.
- OSFMount cannot format empty ram drives that are smaller than 260 MB. They may be
    possible to be formatted using Windows.

Release 1.5 build 1017
2017/12/08 <rn>
- Added option to specify Volume Label when formatting. For
  Command Line, specify format:"Vol Label" under the options (-o). Example Syntax:
    osfmount -a -t vm -m "F:" -o format:"RamDisk" -s 1G
- OSFMount GUI will new auto refresh drive list when images are mounted/unmounted using
  Command Line Interface.
- When mounting a new image using the command line and the mount point specified
  already exists, OSFMount will fail.

Release 1.5 build 1016
2017/11/27 <rn>
- Added "Format as FAT32" as a mount option to newly created Empty RAM drives. For
  Command Line, specify "format" under the options (-o). Example Syntax:
    osfmount -a -t vm -m "F:" -o format -s 1G

Release 1.5 build 1015
2014/02/07 <km>
- Added VHD image file support via libvhdi
- Updated EWF library to libewf-20131230

Release 1.5 build 1014
2013/10/18 <km>
- Fixed issue with detecting partitions for ImageUSB images.
- Windows dynamic disks are now supported
- Fixed issue with mounting via OSFMount command line with "-o rw" option
- Fixed issue with mounting multiple partitions in an image file as writable due to file sharing permissions
- Fixed issue with mounting multiple partitions in an image file from command line
- Drive letters 'A' and 'B' can now be used
- Propagated changes from Imdisk v1.7.5 including some key fixes:
      - Disks with "lost" drive letters can now be removed
      - Notifications hanging on drive creation and removal

Release 1.5 build 1013
2013/03/07 <km>
- Columns and main window are now resizable
- Added "DEBUGMODE" command line parameter to OSFMount (GUI) for debug logging
- Added "File system (detected)" column in the mounted drive list (for file systems unsupported by OS)
- APM partition scheme is now supported, along with more robust partition detection

Release 1.5 build 1012
2012/12/27 <km>
- Fixed an issue with logical (extended) partitions not being displayed in the list when selecting a partition

Release 1.5 build 1011
2012/05/09 <km>
- Fixed OSFMount driver load error in Win2k3 64-bit
- OSFMount command line now supports setting drive type (eg. CD, HD, FD) via the -o option

Release 1.5 build 1010
2012/04/03 <km>
- Fixed error when mounting multiple drives backed by the same image file.
  This includes attempting to mount all partitions from an image file as individual drives.

Release 1.5 build 1009
2012/03/13 <km>
- Browsing for an image file automatically prompts the user to select a partition
- Changed 'Select Partition' button to a hyperlink

Release 1.5 build 1008
2011/11/22 <km>
- Added option to mount all partitions as a separate drive

Release 1.5 build 1007
2011/06/27 <km>
- Added option to dismount all drives upon exit of the application
- Fixed OSFMount logo containing incorrect version number

Release 1.5 build 1006
2011/06/16 <km>
- Added command line support via OSFMount.com console application
- Fixed 'Browse' file dialog to show all file extensions

Release 1.5 build 1005
2011/06/01 <km>
- Fixed crash when mounting incomplete split files

Release 1.5 build 1004
2011/04/25 <km>
- Added support for mounting EnCase/SMART images as read/write
- Added support for saving disks as EnCase/SMART images
- Fixed issue with mounting larger VMWare images
- Fixed crash when mounting a large image into RAM

Release 1.5 build 1003
2011/04/20 <km>
- Fixed issue with mounting images split into a large number of files (eg. AFD, E01)

Release 1.5 build 1002
2011/04/19 <km>
- Added Encase/SMART image read support

Release 1.5 build 1001
2011/04/14 <km>
- Fixed offset/size calculation for images with one partition, which was preventing the mounting of some image files. 

Release 1.5 build 1000
2011/03/16 <km>
- Fixed issue with virtual disks > 4GB
- Fixed issue with memory not deallocating properly when dismounted
- Added support for GPT-based disks
- Fixed issue with extended partitions

Release 1.4 build 1005
2011/1/27 <ir>
- Bug corrected from 1.4.1004 where the mounted drive letter may not appear 
  in Windows Explorer.

Release 1.4 build 1004
2011/1/20 <ir>
- Minor improvements.

Release 1.4 build 1003
2010/12/17 <km>
- Added support for ImageUSB image files
- Fixed issue with mounting on a drive letter that is already being used as 
  a network drive
- Fixed issue with improperly loading/unloading OSFMount driver
- Fixed issue with drive icon remaining in Windows Explorer even after 
  dismounting

Release 1.4 build 1002
2010/12/15 <km>
- Fixed issue with large physical memory usage for non-raw images
- Fixed issue with incorrectly detecting MBR
- Added status window for analyzing images before mounting
- Optimized loading of AFF images
- Synced with afflib-3.6.4

Release 1.4 build 1001
2010/12/08 <km>
- Error checking for NTFS partition size/image size mismatch
- Error checking for encrypted AFF images
- Support for AFF directories (AFD)
- Updated OSFMount logo

Release 1.4 build 1000
2010/12/06 <km>
- Support for split raw, AFF, VMWare images
- Various minor bug fixes

Release 1.3 build 1000 rev 0
WIN32 release 25 October 2010
WIN64 release 25 October 2010
- First version.  

Documentation
=============
All the documentation is included in the help file. It can be accessed 
from the OSFMount software. 


Status
======
This is a free program. 

The initial version was based on "ImDisk Virtual Disk Driver" with 
permission, by Olof Lagerkvist (http://www.ltr-data.se). 

Copyright (C) 2010-2013 PassMark Software
All Rights Reserved
http://www.passmark.com 
Copyright (c) 2005-2009 Olof Lagerkvist
http://www.ltr-data.se      olof@ltr-data.se

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation  files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.


Support
=======
For technical support, questions, suggestions, please visit our web page 
at http://www.passmark.com

Enjoy..
The PassMark Development team
