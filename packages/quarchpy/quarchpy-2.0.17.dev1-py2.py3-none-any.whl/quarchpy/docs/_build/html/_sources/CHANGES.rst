
Changelog (Quarchpy)
====================
2.0.13
-----
- Python2 bug fixes 
- UI tidy up
- New custom annotations and comments QPS API

2.0.12
-----
- Fixed issue with array module scan over UDP outside of subnet
- Bug fix for HD connection via USB in linux
- Added headless launch of QIS
- Added Shinx auto documentation
- Fixed issue with USB command response timeout in longer QCS tests
- Fixed issue where UDP locate parser was using the legacy header, not the quarch fields
- Improved qurchpy.run oarsing and help generation
- Fixed syntax warnings for string literal comparisons
- Calibration wait for specific module uptime and report file updates.

2.0.11
-----
- Improved list selection for devices
- Fixed bug when scanning for devices within an Array
- Module detection fixes for QCS and PAM/Rev-B HD
- Clean up of calibration switchbox code and user logging

2.0.10
-----
- QCS server logging cleaned up
- Additional platform tests added to debug_info test
- Cleaned up print() statements and replaced with logging calls
- Help message added to quarchpy.run command
- Module detection fixes for QCS
- Improved calibration prompts
- Added initial calibration stubs for the PAM
- QCS improvements to linux drive enumeration tests

2.0.9
-----
- Significant QCS additions including power testing
- Added remote switchbox to calibration utility
- Various minor bug fixes and improvements to calibration utility

2.0.8
-----
- Added readme.md for PyPi description
- Fixed bug in QIS when checking if QIS is running
- Various minor additions for QCS

2.0.7
-----
- Changes since 2.0.2
- Minor bug fixes
- Calibration Changes
- QIS folder gone, QIS now in QPS only
- Run package added
- Update quarchpy added
- SystemTest improvements
- UI changes, input validation, smart port select

2.0.2 
-----
- UI Package added 
- Connection over TCP for python added
- Logging on devices
- Drive test core added

2.0.0
-----
- Major folder restructure
- Added test center support
- Detected streaming devices
- Added latest qps1.09 and qis
- Minor bug fixes

1.8.0
-----

- Tab to white space convert
- Updated __init__ file to co-allign with python practices
- Updated project structure 
- Added documents for changes and Script Locations
- Disk selection update
- Compatibility with Python 3 and Linux Improved!

1.7.6
-----

- Fixes bug with usb connection

1.7.5
-----
- Fixed USB DLL Compatibility 
- Fixed potential path issues with Qis and Qps open

1.7.4
-----

- Updated to QPS 1.08

1.7.3
-----

- Additional Bug Fixes

1.7.2
-----

- Bug fixing timings for QIS (LINUX + WINDOWS)

1.7.1
-----

- Updated FIO for use with Linux and to allow arguments without values 
- Fixes path problem on Linux
- Fixes FIO on Linux

1.7.0
-----

- Improved compatability with Windows and Ubuntu 

1.6.1
------

- Updating USB Scan
- Adding functionality to specify OS bit architecture (windows)

1.6.0
-----
- custom $scan IP
- fixes QIS detection
- implements custom separator for stream files
- Bug fix - QIS Load

1.5.4
-----

- Updating README and LICENSE

1.5.2
-----

- Bug Fix - Case sensitivity issue with devices 

1.5.1
-----

- Additional Bug Fixes

1.5.0
-----

- Integration with FIO 
- Additional QPS functionality
- Added device search timeout

1.4.1
-----

- Fixed the wmi error when importing quarchpy.

1.4.0
---

- Integration with QPS
- supports Iometer testing
- Additional fixes for wait times

1.3.4
-----

- Implemented resampling and a better way to launch QIS from the script.

1.3.3
-----

- Implements isQisRunning
- Implements qisInterface
- Changes startLocalQIS to startLocalQis
- Fixes a bug in QIS interface listDevices that didn't allow it to work with Python 3

1.3.2
-----

- Bug Fix running QIS locally

1.3.1
-----

- Implements startLocalQIS
- Packs QIS v1.6 - fixes the bugs with QIS >v1.6 and multiple modules
- Updates quarchPPM (connection_specific)
- Compatible with x6 PPM QIS stream.

1.2.0
-----

- Changes to object model
