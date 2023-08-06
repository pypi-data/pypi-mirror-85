Changelog for Curi Bio Software Development Kit
===============================================

0.8.0 (2020-11-11)
------------------

- Added excel sheet for full length charts.
- Fixed issue with pure noise files causing errors.


0.7.3 (2020-11-05)
------------------

- Fixed issue with twitches point up field for optical data. Also fixed
  case sensitivity issue ('y' and 'Y' both work now).
- Fixed issue causing change of chart bounds to be tedious.
- Fixed Y axis label for optical data (now 'Post Displacement (microns)').
- Fixed many of the issues causing two consecutive relaxations to be
  detected incorrectly.
- Fixed interpolation bugs.
- Changed Sampling / Frame Rate from period in seconds to a rate in Hz.
- Fixed documentation issues.


0.7.1 (2020-10-20)
------------------

- Fixed issue with markers in optical data charts.


0.7.0 (2020-10-15)
------------------

- Added ability to analyze optical data entered in an excel template.
- Added firmware version to excel metadata sheet.


0.6.0 (2020-10-07)
------------------

- Added numbered steps to getting started documentation.
- Added ``contiuous-waveform-plots`` sheet to excel file generation.
  Currently, the only format for chart creation is a <= 10 second "snapshot" of
  the middle data points. It shows waveforms as well as Contraction and
  Relaxation markers on twitches.
- Added access to reference sensor data.
- Added performance improvements for accessing raw data.
- Added ability to upload zip files to Jupyter and updated ``Getting Started``
  documentation to show how to do so.
- Changed all interpolation to 100 Hz.
- Changed default filter for 1600 µs sampling period from Bessel Lowpass 30Hz
  to Butterworth Lowpass 30Hz.
- Fixed peak detection algorithm so it is less likely to report two
  contractions/relaxations of a twitch in a row.


0.5.0 (2020-09-21)
------------------

- Added logging to ``write_xlsx``.
- Added backwards compatibility with H5 file versions >= ``0.1.1``.


0.4.1 (2020-09-16)
------------------

- Added Jupyter getting started documentation.


0.4.0 (2020-09-16)
------------------

- Added support for MyBinder.
- Added Peak Detection Error handling.
- Added function to create stacked plot.


0.3.0 (2020-09-09)
------------------

- Added generation of Excel file with continuous waveform and aggregate metrics.
- Added SDK version number to metadata sheet in Excel file.
