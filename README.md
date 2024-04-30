# Rivas Bible
## Dev Docs
- ## Getting started

To make it easy for you to get started with this project, here is some starting documentation!

1. **Clone the Repository**
    -  **Download Necessities** *(if not already on machine)*
        - [Git](https://github.com/git-guides/install-git) 
        - [Python](https://www.python.org/downloads/) 
        - [Pycharm](https://www.jetbrains.com/pycharm/download/)  
        
    -  **Cloning using Pycharm**
        - Open Pycharm and click "Get from VCS"  

          ![Screenshot](/DocumentationImages/GetFromVCS.png)

        - Open your browser and navigate to the project repository. Copy the repository's cloning link.  
            
            ![Screenshot](/DocumentationImages/CloneLink.png)

        - Paste the url into the "Get From Version Control popup and click "Clone". 

          ![Screenshot](/DocumentationImages/PycharmCloneRepo.png)

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


3. **Frontend Setup**
    - Install Node.js: https://nodejs.org/en/download/
	- In Pycharm's terminal, navigate to the bible-frontend directory and run the following commands:


```bash
npm start
```
	
  - Open your browser and navigate to http://localhost:3000 - the translation application should appear


    ![Screenshot](/DocumentationImages/FrontendOpen.png)


## User Docs
- ## Usage
1. **Input Text** into the textbox on the left side of the screen.  

  ![Screenshot](/DocumentationImages/FrontendTextInput.png)

2. **Select Your Preferred Language** and click the "Translate" button.  

  ![Screenshot](/DocumentationImages/FrontendInputChooseTranslation_1.png) ![Screenshot](/DocumentationImages/FrontendInputChooseTranslation_2.png)

3. **Check the Translation**  

  ![Screenshot](/DocumentationImages/FrontendTranslationOutput.png)

- ## Main Elements
  - **Translation Page**
    - This is the primary page for interacting with our translation mechanism.

  - **Input Textbox**
    - This textbox is situated on the left half of the screen, right below the name of our Language Model. Users can interact with it by  
      clicking on it, and typing words into it.

  - **Language Dropdown**
    - This dropdown is situated right underneath the input textbox. Users can interact with it by clicking on it once to reveal the possible language options. They can select the language to translate the input text into by clicking on the desired language. 

  - **Translate Button**
    - This button can be seen below the Input textbox and to the right of the Language Dropdown Menu. Once clicked, it will detect the text input in the Input Textbox, and send it to a backend system that will return the translated verson of the input text, to be displayed in the Output Textbox.

  - **Output Textbox**
    - This textbox is located to the right of the Input Textbox, and is not user interactible. Once the translation is complete, the results will be displayed in this textbox.  



# Contributions

# License

- # TODO:
  - Add Dev documentation for account token generation for cloning the repository
  - Add additional Dev documentation for the frontend dependencies and python backend requirements
  - Add additional Dev documentation for python backend setup
