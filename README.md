# TopoLines: Topological Smoothing for Line Charts
## EuroVis 2020 Short Papers Submission #1026

This software admittedly could be difficult to get running. We have tested it on Mac and Linux distributions. 

If you are on Windows or would like a live demo without running the software, visit **http://131.247.3.215:5050** or **http://131.247.3.213:5050**


### [required] Install python3, python3-virtualenv, and git

    On Debian linux, such as Ubuntu
    > sudo apt install python3 python3-virtualenv git

    On Mac, you can download from python.org, macports, or homebrew. You will need python3, python3-virtualenv, pip, git, ... maybe others 


### [optional] If you want topolgical distances to work: 

    Clone and build Hera (https://bitbucket.org/grey_narn/hera)
    > git clone https://bitbucket.org/grey_narn/hera.git

    See included build instruction for building both geom_bottleneck and geom_matching

    Update path used in our software:
        Open setup.sh
        Update the path to Hera bottleneck_dist and wasserstein_dist to absolute path you compiled to


### [required] Run setup process

    This process will setup a virtual environment and install all prerequisites.
    > ./setup.sh
    
    In during this process you should see information, but hopefully no errors.
    
    
### [required] Start the webserver
    
    Assuming everything has run correctly thus far, we need to run the code.
    
    > ./run.sh
    
    If everythin goes as planned, a webserver will be started and a webbrowser will pop open to the correct url. If no browser appears, continue to url http://localhost:5050
    
    

