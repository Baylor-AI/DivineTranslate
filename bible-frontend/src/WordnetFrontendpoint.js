import React, {useEffect, useState} from "react";
import axios from 'axios';

const API_URL = 'http://localhost:8000/';

export default async function CompareWord ({fromText = 'fruit', toText = 'produce', fromLang = 'eng', toLang = 'eng', value = 5}) {
    const [result, setResult] = useState([]);

    try{
        const response = await axios.get(
            `${API_URL}word_similarity/`,
            {
                params: {
                    initial_word: fromText,
                    compare_word: toText,
                    lang1: fromLang,
                    lang2: toLang,
                    limit: value
                }
            });
        setResult(response.data)
    }
    catch (error){
        console.error('Error fetching data: ', error)
    }

    return (
        <div>
            <div>
                <h2>Showing Replacements for {fromText}:</h2>
            </div>
            <div>
                <u1>

                </u1>
            </div>
        </div>
    );
};

// export default CompareWord;
