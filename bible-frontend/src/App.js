import React, { useState } from 'react';
import translateText from './GoogleTranslate';
import CompareWord from './WordnetFrontendpoint';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import WordSelector from "./WordSelector";
import translateTextM from "./ModelTranslate";
import  { useEffect } from 'react';

const API_URL = 'http://localhost:8001';

function App() {
    const [inputText, setInputText] = useState('');
    const [inputLanguage, setInputLanguage] = useState('eng');
    const [targetLanguage, setTargetLanguage] = useState('fra');
    const [translatedText, setTranslatedText] = useState('');
    const [wordnetResults, setWordNetResults] = useState([]);
    const [showWordSelector, setShowWordSelector] = useState(false);

    const wordSelectorData = {
        inputText: inputText,
        translatedText: translatedText,
        targetLang: targetLanguage,
        wordnetResults: wordnetResults,
    };

    const handleTranslate = async () => {
        wordSelectorData.wordnetResults = [];
        setTranslatedText("");
        if (inputText && inputLanguage !== targetLanguage) {
            const text = await translateTextM(stripPunctuation(inputText), inputLanguage, targetLanguage);
            setTranslatedText(text);
            console.log(text);
        } else {
            // Input and target languages are the same, or input text is empty.
            // Handle this case as needed.
        }
    };

    const fillHasResults = async () => {
        if (translatedText) {
            const inputWords = stripPunctuation(inputText).split(' ');
            const translatedWords = stripPunctuation(translatedText).split(' ');

            const wordPairs = translatedWords.map((word, index) => ({
                initial: word,
                compare: inputWords[index] || '',
                lang1: inputLanguage,
                lang2: targetLanguage,
                limit: 5
            }));
            console.log(wordPairs.toString());
            const apiCalls = wordPairs.map(pair =>
                fetch(`http://localhost:8001/word_similarity/?initial=${pair.compare}&compare=${pair.initial}&lang1=${pair.lang1}&lang2=${pair.lang2}&limit=${pair.limit}`)
                    .then(response => response.json())
            );

            Promise.all(apiCalls)
                .then(results => {
                    setWordNetResults(results);
                    console.log('WordNet results:', results);
                })
                .catch(error => console.error('Error fetching WordNet results:', error));
        }
    };

     const languageOptions = {
    eng: 'English',
    fra: 'French',
    deu: 'German',
    hai: 'Haida',
    jpn: 'Japanese',
    cmn: 'Mandarin Chinese',
    mar: 'Marathi',
    nse: 'Nsenga',
    rus: 'Russian',
    spa: 'Spanish'
};

    const languageOptionsFiltered = Object.entries(languageOptions)
        .filter(([code]) => code !== inputLanguage); // Filtering out the selected input language

    const stripPunctuation = (str) => {
        return str.replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ");
    };

    const handleInputChange = (e) => {
        setInputText(e.target.value);
    };

    const handleTargetChange = (e) => {
        setTargetLanguage(e.target.value);
    };

    const handleClose = (e) => {

    };

    const toggleWordSelector = () => {
        fillHasResults();
        setShowWordSelector(!showWordSelector);
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
                                onChange={handleInputChange}
                            ></textarea>
                        </div>
                        <p>Input language:</p>
                        <div className="input-group">
                            <select
                                className="form-select"
                                aria-label="Default select example"
                                value={inputLanguage}
                                onChange={(e) => setInputLanguage(e.target.value)}
                            >
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
                                {languageOptionsFiltered.map(([code, language]) => (
                                    <option key={code} value={code}>
                                        {language}
                                    </option>
                                ))}
                            </select>
                            <button
                                className="btn btn-primary"
                                onClick={handleTranslate}
                            >
                                Translate
                            </button>
                        </div>
                        <p></p>
                        <h4>Translation Tools:</h4>
                        <button
                            type="button"
                            className="btn btn-primary"
                            data-bs-toggle="modal"
                            data-bs-target="#exampleModal"
                            onClick={toggleWordSelector}
                            disabled={targetLanguage !== 'eng'}
                        >
                            WordNet
                        </button>
                        <p>If any of the words selected by the model are unsatisfactory, wordnet generates similar words and the degrees of similarity to original word. This is limited to English translations. </p>
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
                </div>
            </div>
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">WordNet</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <WordSelector data={wordSelectorData}></WordSelector>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onClick={handleClose} data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;

