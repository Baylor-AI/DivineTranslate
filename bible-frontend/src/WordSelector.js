import  { useEffect } from 'react';
import React, { useState } from 'react';
const API_URL = 'http://localhost:8001/';
const WordSelector = ({ data }) => {
  const [selectedWord, setSelectedWord] = useState('');
  const [relatedWords, setRelatedWords] = useState([]);

  useEffect(() => {
    if (selectedWord) {
      // Find the corresponding word in data.inputText based on the index
      const index = data.translatedText.split(' ').indexOf(selectedWord);
      setRelatedWords(data.wordnetResults[index]);

    }
  }, [selectedWord, data.inputText, data.translatedText]);

  const handleWordSelect = (word) => {
    setSelectedWord(word);
  };

  return (
   <div>
  <p></p>
  {data.translatedText && (
    <div>
      {selectedWord && (
        <p>Selected Word: {selectedWord}</p>
      )}
      {relatedWords && relatedWords.length > 0 && (
        <div>
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
    </div>
  )}



      {data.translatedText &&
        data.translatedText.split(' ').map((word, index) => (
          <React.Fragment key={index}>
            {data.wordnetResults[index] && data.wordnetResults[index][1] > 3 ? (
              <button onClick={() => handleWordSelect(word)}>
                {word}
              </button>
            ) : (
              <span> {word} </span>
            )}
          </React.Fragment>
        ))}
    </div>
  );
};

export default WordSelector;

