# Rivas Bible

## Dev Docs
- ## Getting started

To make it easy for you to get started with this project, here is some starting documentation!

1. **Clone the Repository**
    -  **Download Necessities** *(if not already on machine)*
        - Install Git : [Download Site](https://github.com/git-guides/install-git) 
        - Install Python : [Download Site](https://www.python.org/downloads/) 
        - Install Pycharm (Community Edition) : [Download Site](https://www.jetbrains.com/pycharm/download/)  
        
    -  **Cloning using Pycharm**
        - Open Pycharm and click "Get from VCS"

          ![Screenshot](../DocumentationImages/GetFromVCS.png)

        - Open your browser and navigate to the project repository. Copy the repository's cloning link 
          ![Screenshot](../DocumentationImages/CloneLink.png)

        - Paste the url into the "Get From Version Control popup and click "Clone". 
          ![Screenshot](../DocumentationImages/PycharmCloneRepo.png)

        - Wait for the project to finish cloning and clieck "Trust Project" when the popup appears.
  
2. **Environment Setup**
    - Once you have the project opened, create a virtual environment using Pycharm's terminal
#### Windows
```bash
python -m venv < venv name >
```

#### Linux
```bash
python3 -m venv < venv name >
```


  - Now we can activate our virtual environment by running these commands in Pycharm's terminal:
#### Windows
```bash
.\< venv name >\Scripts\activate
```
#### Linux
```bash
source < venv name >/bin/activate
```


  - After activating the virtual environment, we can install our python dependencies by running this command in Pycharm's termminal: 
  
```bash
pip install -r requirements.txt
``` 
3. **bible-frontend: Frontend Setup**
    - Install Node.js: https://nodejs.org/en/download/
	- In Pycharm's terminal, navigate to the bible-frontend directory and run the following commands:
```bash
npm start
```
	
  - Navigate to http://localhost:3000 - you should see the translation application


## User Docs
- ## Usage
