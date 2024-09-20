##### Minimum #####

The bare minimum to get started would be 
- have docker installed on the base machine and ensure the current user is in the 'docker' group. If you just now added the user to the group, logout, and log back in for it to take effect, then continue with the rest below
- create an ENV file
	- This is to differentiate between production and development. 
	- The ENV file for development typically would be whatever path to your test directory and just have 1 line that looks like "export BASEDIR=/path/to/docker/files/external/to/containers" 
	- I recommend the base directory for production to be 'BASEDIR=/app/dockerfiles' unless you change the setup for some reason, you can see that this is also mapped in the CMD as is explained later.



##### Development #####

To get started with development, first complete the minimum section above:
- *recommended but not required* create a venv  to isolate your dev environment. To do this:
	- change to the top directory for the site and run 'python3 -m venv devenv'
	- enter the venv by running '. ./devenv/bin/activate'
	- if you choose to leave the venv you can just run 'deactivate'
- run 'pip install --upgrade pip'
- change to the app directory and run 'pip install -r requirements.txt' to install all required libraries to run various functions
- change to the dir where your ENV file is and run '. ./ENV' to set your environment variables
- change the dir to the app directory and run 'python backbone.py'

The dev environment runs in a verbose mode to make troubleshooting easier, eventually I hope to add a more in depth error handler so you won't need to use the terminal to read the stack trace but that may be a while.



##### Production #####

To get started with production, first complete the minimum section above
- in terminal, navigate to the /maxsessions.com/app directory and run 'build -t "desiredimagename" .'
- change the container name, -v line and final line in the CMD file to the image name you chose in the step above 
	- you need to change the path before ':' to the directory where you plan to store your docker directories for your various container files and images. 
		- After the ':' should stay the same unless you know what you are doing
- run the command 'sudo bash CMD'

This is how to get the site running in production



##### File Structure #####

Just so you understand, the docker directory I am referring to is a structure similar to this (best read in a text editor, git webpage doesn't display properly):

/dockercontainers
	/terraria
		/game files
		/etc
	/mysql
		/db files
		/etc
	/nginx
		/config
		/etc
	/etc



If you set a directory for each image you hope to use, as you use these tools you will select the directory you wish to work with and as you create a docker run command, you can save it to the desired directory to re-use later
without having to remember the config
