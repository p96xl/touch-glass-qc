@echo off
rem Opens Touch Glass QC as its own window (no browser bars). Needs Edge or Chrome.
set "P=%~dp0touch-qc.html"
set "P=%P:\=/%"
start "" msedge --app="file:///%P%"
