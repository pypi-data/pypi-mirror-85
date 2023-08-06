# Janet

Janet is a powerful python project manager that allows python developers
to focus more on scripting and less on piping packages. janet will auto-install
pip packages when a .py file is saved and will generate a requirements.txt file
automatically, it will also monitor all your scripts for new packages and install them in the background. 

To get start with janet, you need to install the package:

```bash
pip install janet
```

once installed, cd to your project directory and run the following:

```bash
python -m janet -p <PROJECT_PATH, default="current directory"> -s <SCRIPT>
```
the -s flag specifies which script to run when the ```run``` command is issued,
this is useful if your project is a webserver. You can change the script that is run, this is discussed below in the "commands" section.

you will then be greeted with a menu of commands, that's it!

![Janet CLI](readme_assets/images/janet_cli.png)

you can now start working on your project, create new files, delete files, do whatever it is you want, janet will silently track your project and download dependecies silently once a file is saved.






## I am seeing this weird ```janetrecord.json```, WTH is that ?

When you initialize janet in your projet directory, it creates a ```janetrecord.json``` file that stores the last time a file is modified, when a file is saved the last modified date will also change and notify janet to check for new packages

![Janet record](readme_assets/images/janet_record.png)