import React, { useState } from 'react';
import translateText from './GoogleTranslate';
import CompareWord from './WordnetFrontendpoint';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import wordSelector from "./WordSelector";
import WordSelector from "./WordSelector";

function App() {
  const [inputText, setInputText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('es'); // Default: Spanish
     const [translatedText, setTranslatedText] = useState('');

  const handleTranslate = async () => {
    if (inputText) {
      const text = await translateText(inputText, targetLanguage);
        setTranslatedText(text);
        console.log(text);
    }
  };

   return (
        <div className="App">
            <h1 className="text-success">  SIC'EM NLP </h1>
            <div class="container">
                <div className="row">
                    <div className="col s12 m6">
                        <div className="form-group">
                            <textarea className="form-control" id="exampleFormControlTextarea1" rows="5" value={inputText}
        onChange={(e) => setInputText(e.target.value)}></textarea>
                        </div>
                        <div className="input-group">

                        <select className="form-select" aria-label="Default select example" value={targetLanguage} onChange={(e) => setTargetLanguage(e.target.value)}>
                            <option selected>Select translation language</option>
                            <option value="es">Spanish</option>
                            <option value="fr">French</option>
                            <option value="en">English</option>
                        </select>
                            <a
                            className="btn btn-primary"
                            data-bs-toggle="collapse"
                            href="#collapseExample"
                            role="button"
                            aria-expanded="false"
                            aria-controls="collapseExample"
                            onClick={handleTranslate}
                        >
                            Translate
                        </a>
                            </div>
                    </div>
                    <div className="col s12 m6">

                        <div className="form-group">
                            <textarea className="form-control" id="exampleFormControlTextarea1" rows="5" value={translatedText}></textarea>
                        </div>
                    </div>
                    <WordSelector sentence={translatedText}/>
                </div>

            </div>
        </div>
    );
}

export default App;





