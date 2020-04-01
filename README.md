# TopoLines: Topological Smoothing for Line Charts

__TopoLines: Topological Smoothing for Line Charts__\
__Paul Rosen, Ashley Suh, Christopher Salgado, & Mustafa Hajij__\
__EuroVis 2020 Short Papers__

We have tested this setup on Mac and Linux distributions. 


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
    
    
### [required] Generate the experiemental data
    
    Assuming everything has run correctly thus far, we need to run the code.
    
    > ./run.sh
    

### [required] Start a webserver

    Go to docs directory
    > cd docs
    
    Start webserver
    > python3 -m http.server 5050
    
    If everything goes as planned, you can open a webbrowser and open url http://localhost:5050
    
    

