import React, { useState, useEffect } from 'react';

const WordSelector = ({ sentence }) => {
  const [selectedWord, setSelectedWord] = useState('');
  const [relatedWords, setRelatedWords] = useState([]);

  useEffect(() => {
    // Fetch related words when the selected word changes
    if (selectedWord) {
      fetch(`YOUR_API_ENDPOINT?word=${selectedWord}`)
        .then(response => response.json())
        .then(data => setRelatedWords(data))
        .catch(error => console.error('Error fetching related words:', error));
    }
  }, [selectedWord]);

  const handleWordSelect = (word) => {
    setSelectedWord(word);
  };

  return (
    <div>
      <p>Sentence: {sentence}</p>

      {sentence && (
        <div>
          <p>Selected Word: {selectedWord}</p>
          <p>Related Words:</p>
          <ul>
            {relatedWords.map((word, index) => (
              <li key={index}>{word}</li>
            ))}
          </ul>
        </div>
      )}

      {sentence && sentence.split(' ').map((word, index) => (
        <button key={index} onClick={() => handleWordSelect(word)}>
          {word}
        </button>
      ))}
    </div>
  );
};

export default WordSelector;

