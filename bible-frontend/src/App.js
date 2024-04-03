import React, { useState } from 'react';
import translateText from './GoogleTranslate';
import CompareWord from './WordnetFrontendpoint';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import WordSelector from "./WordSelector";
import translateTextM from "./ModelTranslate";

function App() {
  const [inputText, setInputText] = useState('');
  const [inputLanguage, setInputLanguage] = useState('Set input language'); // Default: English
  const [targetLanguage, setTargetLanguage] = useState('Set output language'); // Default: Spanish
  const [translatedText, setTranslatedText] = useState('');

  const handleTranslate = async () => {
    if (inputText && inputLanguage !== targetLanguage) {
      if (targetLanguage === "cmn") {
        const text = await translateTextM(inputText, inputLanguage, targetLanguage);
        setTranslatedText(text);
        console.log(text);
      } else {
        const text = await translateText(inputText, targetLanguage);
        setTranslatedText(text);
        console.log(text);
      }
    } else {
      // Input and target languages are the same, or input text is empty.
      // Handle this case as needed.
    }
  };

  const languageOptions = {
    es: 'Spanish',
    en: 'English',
    fr: 'French',
    cmn: 'Mandarin Chinese',
  };

  const languageCodeMap = {
    es: 'spa',
    en: 'eng',
    fr: 'fra',
    'Mandarin Chinese': 'cmn',
  };

  const handleInputChange = (e) => {
    setInputLanguage(e.target.value);
  };

  const handleTargetChange = (e) => {
    setTargetLanguage(e.target.value);
  };

  const wordSelectorData = {
    inputText: inputText,
    translatedText: translatedText,
    targetLang: languageCodeMap[targetLanguage],
  };

  return (
    <div className="App">
      <h1 className="text-success">SIC'EM NLP</h1>
      <div className="container">
        <div className="row">
          <div className="col s12 m6">
            <div className="form-group">
              <textarea
                className="form-control"
                id="exampleFormControlTextarea1"
                rows="5"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              ></textarea>
            </div>
            <div className="input-group">
              <select
                className="form-select"
                aria-label="Default select example"
                value={inputLanguage}
                onChange={handleInputChange}
              >
                <option>Select input language</option>
                {Object.entries(languageOptions).map(([code, language]) => (
                  <option key={code} value={code}>
                    {language}
                  </option>
                ))}
              </select>
              <select
                className="form-select"
                aria-label="Default select example"
                value={targetLanguage}
                onChange={handleTargetChange}
              >
                <option>Select translation language</option>
                {Object.entries(languageOptions).map(([code, language]) => (
                  <option key={code} value={code}>
                    {language}
                  </option>
                ))}
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
              <textarea
                className="form-control"
                id="exampleFormControlTextarea1"
                rows="5"
                value={translatedText}
              ></textarea>
            </div>
          </div>
          <WordSelector data={wordSelectorData} />
        </div>
      </div>
    </div>
  );
}

export default App;




