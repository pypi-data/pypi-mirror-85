import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="PySimpleGUI",
    version="4.32.1",
    author="PySimpleGUI",
    author_email="PySimpleGUI@PySimpleGUI.org",
    description="GUI SDK Launched in 2018. It's 2020 and PySimpleGUI is actively developed and supported. Super-simple to create custom GUI's. 200+ Demo programs & Cookbook for rapid start. Extensive documentation. Main doc is www.PySimpleGUI.org.  Examples using Machine Learning (GUI, OpenCV Integration,  Chatterbot), Rainmeter Style Floating Desktop Widgets, Matplotlib + Pyplot integration, add GUI to command line scripts, PDF & Image Viewer. Great for beginners as well as advanced GUI programmers",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="GUI UI tkinter wrapper simple easy beginner novice student graphics progressbar progressmeter",
    url="https://github.com/PySimpleGUI/PySimpleGUI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)