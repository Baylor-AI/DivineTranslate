import React, { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000/';

const WordSelector = ({ data }) => {
  const [selectedWord, setSelectedWord] = useState('');
  const [relatedWords, setRelatedWords] = useState([]);

  useEffect(() => {
    if (selectedWord) {
      // Find the corresponding word in data.inputText based on the index
      const compareWord = data.inputText.split(' ')[data.translatedText.split(' ').indexOf(selectedWord)];

      const apiUrl = `http://localhost:8000/word_similarity/?initial=${compareWord}&compare=${selectedWord}&lang1=eng&lang2=${data.targetLang}&limit=5`;

      fetch(apiUrl)
        .then(response => response.json())
        .then(data => setRelatedWords(data))
        .catch(error => console.error('Error fetching related words:', error));
    }
  }, [selectedWord, data.inputText, data.translatedText]);

  const handleWordSelect = (word) => {
    setSelectedWord(word);
  };

  return (
    <div>
      <p>Sentence: {data.inputText}</p>
      <p>Translated Text: {data.translatedText}</p>

      {data.translatedText && (
        <div>
          <p>Selected Word: {selectedWord}</p>
          <p>Related Words:</p>
          {relatedWords.map((item, index) => (
            <div key={index}>
              {typeof item === 'number' && relatedWords[index + 1] ? (
                <span>
                  {relatedWords[index + (relatedWords.length / 2)]} {item}%
                </span>
              ) : null}
            </div>
          ))}
        </div>
      )}

      {data.translatedText &&
        data.translatedText.split(' ').map((word, index) => (
          <button key={index} onClick={() => handleWordSelect(word)}>
            {word}
          </button>
        ))}
    </div>
  );
};

export default WordSelector;

