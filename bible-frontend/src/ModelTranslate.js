import axios from 'axios';

//const API_URL = 'http://localhost:8000/translate/';
const API_URL = 'https://b63bfdks-8000.usw3.devtunnels.ms/translate/';

const translateTextM = async (text, source_lang_code, target_lang_code) => {
    console.log(text + " " + source_lang_code + " " + target_lang_code);
  const response = await axios.post(
    API_URL,
    {
      text: text,
      source_lang_code: source_lang_code,
      target_lang_code: target_lang_code,
    }
  );

  return response.data.translated_text;
};

export default translateTextM;
