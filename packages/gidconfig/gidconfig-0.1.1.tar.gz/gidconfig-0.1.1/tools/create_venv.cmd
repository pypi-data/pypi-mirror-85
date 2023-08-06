@echo off
setlocal enableextensions
set OLDHOME_FOLDER=%~dp0
set INPATH=%~dp1
set INFILE=%~nx1
set INFILEBASE=%~n1

rem ---------------------------------------------------
set _date=%DATE:/=-%
set _time=%TIME::=%
set _time=%_time: =0%
rem ---------------------------------------------------
rem ---------------------------------------------------
set _decades=%_date:~-2%
set _years=%_date:~-4%
set _months=%_date:~3,2%
set _days=%_date:~0,2%
rem ---------------------------------------------------
set _hours=%_time:~0,2%
set _minutes=%_time:~2,2%
set _seconds=%_time:~4,2%
rem ---------------------------------------------------
set TIMEBLOCK=%_years%-%_months%-%_days%_%_hours%-%_minutes%-%_seconds%
Echo ################# Current time is %TIMEBLOCK%
Echo.
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64
Echo.
Echo.
Echo -------------------------------------------- BASIC VENV SETUP --------------------------------------------
Echo.
Echo.
Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
Echo.
echo ################# suspending Dropbox
call pssuspend64 Dropbox
echo.
Echo ################# removing old venv folder
RD /S /Q ..\.venv
echo.

Echo ################# creating new venv folder
mkdir ..\.venv
echo.
Echo ################# calling venv module to initialize new venv
python -m venv ..\.venv
echo.

Echo ################# changing directory to ..\.venv
cd ..\.venv
echo.
Echo ################# activating venv for package installation
call .\Scripts\activate.bat
echo.

Echo ################# upgrading pip to get rid of stupid warning
call %OLDHOME_FOLDER%get-pip.py
echo.
echo.
echo.
Echo -------------------------------------------- INSTALLING PACKAGES --------------------------------------------
echo.
echo.
Echo +++++++++++++++++++++++++++++ Standard Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing Setuptools
call pip install --upgrade --pre setuptools
echo.
rem Echo ################# Installing pywin32
rem call pip install --upgrade --pre pywin32
rem echo.
Echo ################# Installing python-dotenv
call pip install --upgrade --pre python-dotenv
echo.
echo.
rem Echo +++++++++++++++++++++++++++++ Qt Packages +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing PyQt5
rem call pip install --upgrade --pre PyQt5
rem echo.
rem Echo ################# Installing pyopengl
rem call pip install --upgrade --pre pyopengl
rem echo.
rem Echo ################# Installing PyQt3D
rem call pip install --upgrade --pre PyQt3D
rem echo.
rem Echo ################# Installing PyQtChart
rem call pip install --upgrade --pre PyQtChart
rem echo.
rem Echo ################# Installing PyQtDataVisualization
rem call pip install --upgrade --pre PyQtDataVisualization
rem echo.
rem Echo ################# Installing PyQtWebEngine
rem call pip install --upgrade --pre PyQtWebEngine
rem echo.
rem Echo ################# Installing pyqtgraph
rem call pip install --upgrade --pre pyqtgraph
rem echo.
rem Echo ################# Installing QScintilla
rem call pip install --upgrade --pre QScintilla
rem echo.

echo.

rem Echo +++++++++++++++++++++++++++++ Packages From Github +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing git+https://github.com/overfl0/Armaclass.git
rem call pip install --upgrade --pre git+https://github.com/overfl0/Armaclass.git
rem echo.
echo.

rem Echo +++++++++++++++++++++++++++++ Misc Packages +++++++++++++++++++++++++++++
rem echo.
rem Echo ################# Installing pyperclip
rem call pip install --upgrade --pre pyperclip
rem echo.
Echo ################# Installing jinja2
call pip install --upgrade --pre jinja2
echo.
rem Echo ################# Installing bs4
rem call pip install --upgrade --pre bs4
rem echo.
rem Echo ################# Installing requests
rem call pip install --upgrade --pre requests
rem echo.
rem Echo ################# Installing PyGithub
rem call pip install --upgrade --pre PyGithub
rem echo.
Echo ################# Installing fuzzywuzzy
call pip install --upgrade --pre fuzzywuzzy
echo.
rem Echo ################# Installing fuzzysearch
rem call pip install --upgrade --pre fuzzysearch
rem echo.
Echo ################# Installing python-Levenshtein
call pip install --upgrade --pre python-Levenshtein
echo.
Echo ################# Installing jsonpickle
call pip install --upgrade --pre jsonpickle
echo.
Echo ################# Installing parse
call pip install --upgrade --pre parse
echo.
rem Echo ################# Installing parce
rem call pip install --upgrade --pre parce
rem echo.
rem Echo ################# Installing parceqt
rem call pip install --upgrade --pre parceqt
rem echo.
rem Echo ################# Installing discord.py
rem call pip install --upgrade --pre discord.py
rem echo.
Echo ################# Installing regex
call pip install --upgrade --pre regex
echo.
Echo ################# Installing marshmallow
call pip install --upgrade --pre marshmallow
echo.
rem Echo ################# Installing click
rem call pip install --upgrade --pre click
rem echo.
rem Echo ################# Installing checksumdir
rem call pip install --upgrade --pre checksumdir
rem echo.
rem Echo ################# Installing pdfkit
rem call pip install --upgrade --pre pdfkit
rem echo.
rem Echo ################# Installing sip
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall sip
rem echo.
rem Echo ################# Installing PyQt-builder
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall PyQt-builder
rem echo.
rem Echo ################# Installing python-poppler-qt5
rem call pip install --upgrade --pre --no-cache-dir --force-reinstall git+https://github.com/mitya57/python-poppler-qt5.git@sip5
rem echo.
echo.
Echo +++++++++++++++++++++++++++++ Gid Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing flit
call pip install --force-reinstall --no-cache-dir --upgrade --pre flit
echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
rem pushd D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidtools_utils
rem call flit install -s
rem popd
rem echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidqtutils
rem echo.
Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\gidlogger_rep
echo.

call pip install --force-reinstall --no-cache-dir --upgrade --pre gidlogger

rem echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_Vscode_Wrapper
rem echo.
rem Echo ################# Installing D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
rem call pip install -e D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Gid_View_models
rem echo.
rem echo.

Echo ################# changing directory to %OLDHOME_FOLDER%
cd %OLDHOME_FOLDER%
echo.
rem Echo ################# writing ..\requirements_dev.txt
rem echo ########################################################## created at --^> %TIMEBLOCK% ##########################################################> ..\requirements_dev.txt
rem call pip freeze>>..\requirements_dev.txt
echo.
echo.
echo.
Echo +++++++++++++++++++++++++++++ Test Packages +++++++++++++++++++++++++++++
echo.

rem Echo ################# Installing pytest-qt
rem call pip install --upgrade --pre pytest-qt
rem echo.
Echo ################# Installing pytest
call pip install --upgrade --pre pytest
echo.

echo.
Echo +++++++++++++++++++++++++++++ Dev Packages +++++++++++++++++++++++++++++
echo.
Echo ################# Installing wheel
call pip install --no-cache-dir --upgrade --pre wheel
echo.
rem Echo ################# Installing https://github.com/pyinstaller/pyinstaller/tarball/develop
rem call pip install --force-reinstall --no-cache-dir --upgrade --pre https://github.com/pyinstaller/pyinstaller/tarball/develop
rem echo.
Echo ################# Installing pep517
call pip install  --no-cache-dir --upgrade --pre pep517
echo.

rem Echo ################# Installing pyqt5-tools==5.15.1.1.7.5
rem call pip install --pre --upgrade --pre pyqt5-tools==5.15.1.1.7.5
rem echo.
rem Echo ################# Installing PyQt5-stubs
rem call pip install --upgrade --pre PyQt5-stubs
rem echo.


rem Echo ################# Installing pyqtdeploy
rem call pip install --upgrade --pre pyqtdeploy
rem echo.
rem Echo ################# Installing nuitka
rem call pip install --upgrade --pre nuitka
rem echo.
Echo ################# Installing memory-profiler
call pip install --upgrade --pre memory-profiler
echo.
Echo ################# Installing matplotlib
call pip install --upgrade --pre matplotlib
echo.
Echo ################# Installing import-profiler
call pip install --upgrade --pre import-profiler
echo.
Echo ################# Installing objectgraph
call pip install --upgrade --pre objectgraph
echo.
Echo ################# Installing pipreqs
call pip install --upgrade --pre pipreqs
echo.
Echo ################# Installing pydeps
call pip install --upgrade --pre pydeps
echo.
rem Echo ################# Installing bootstrap-discord-bot
rem call pip install --upgrade --pre bootstrap-discord-bot
rem echo.
rem echo.
Echo ################# Installing numpy
call pip install --no-cache-dir --force-reinstall numpy==1.19.3
echo.
rem Echo ################# Installing PyQtdoc
rem call pip install --no-cache-dir --force-reinstall PyQtdoc
rem echo.
rem echo -------------------calling pyqt5toolsinstalluic.exe-----------------------------
rem call ..\.venv\Scripts\pyqt5toolsinstalluic.exe
rem echo.
echo.
rem call ..\.venv\Scripts\pyqtdoc.py register
echo.
rem Echo ################# converting ..\requirements_dev.txt to ..\requirements.txt by calling %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
rem call %OLDHOME_FOLDER%convert_requirements_dev_to_normal.py
echo.
Echo INSTALL THE PACKAGE ITSELF AS -dev PACKAGE SO I DONT HAVE TO DEAL WITH RELATIVE PATHS
cd ..\
rem call pip install -e --upgrade --pre .
call flit --debug install -s
echo.
echo.
echo.
Echo setting modified env vars!!
call %OLDHOME_FOLDER%create_venv_extra_envvars.py %OLDHOME_FOLDER% gidconfig
echo.
rem Echo ################# restarting Dropbox
rem call pssuspend64 Dropbox -r
rem echo.

echo ###############################################################################################################
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ---------------------------------------------------------------------------------------------------------------
echo                                                     FINISHED
echo ---------------------------------------------------------------------------------------------------------------
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ###############################################################################################################
