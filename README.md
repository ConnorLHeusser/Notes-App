# Notes-App
This program serves as an application where one can write passwords and other reminders in the form of Notes. The reason behind this choice of program was because it will have relativley less time consuming UI to implement so that we will have more time to make the program work. The program uses exclusivly Python for its code as we felt it was within our abilities to use it for both the main program and the backend code.

Currently the program contains this README, The folder for Ui and the main application. The main.py is where all logic and routing is located and the backbone of the project. Ui contains any html and css used to make landing pages

The functionallity to allow the user to create multiple files to store their notes in, edit any existing notes and also delete notes.

To run app, go to latest release and download the "Note-App" zip file and run the "main.py" file

v2.0.1 

Rebuilt the codebase adding in much needed frameworks and api's. There are still major bugs that need to be tackled but for now the code base is stabalized and going in the right direction.

Docker file
for much simpler means of running the app, download the docker file and build it with

"docker build -t noteapp_docker_file .\"

And run it using:

"docker run -p 8000:8000 noteapp_docker_file"

Everything will build automatically for you with those steps. 

v3.0.0 Professional Release

Program is in a polished enough state to show off basic uses and functionality. 

Final Release Reflections:

Throughout the development of this app, we had to learn many different things very quickly because the starting of the app was quite shaky, but after seeing frameworks that could be used and learning how to use and implement them the pace started to pick up and also working with different technologies other than pure coding, such as working with dockerfiles and using profiling tools to optimize our code. It was a very eye opening experience and we gained alot of useful knowledge and know how from it 

Plans for the future:

There are still a few features that didn't quite make it into the final release due to time constraints that we would have liked to have implemented, such as the star and archieve feature, but those can still be worked on in the future.  




