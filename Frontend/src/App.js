import { useState } from 'react';
import axios from 'axios';
import './App.css';
import Header from './Component/Header';
import Contents from './Component/Company Contents';

function App() {

  const [code, setCode] = useState('');
  const [loadError, setLoadError] = useState('');
  const [loadingCode, setLoadingCode] = useState(false);
  const [currentFilter, setCurrentFilter] = useState('Today');

  const getStockInfo = async(code, filter) => {
    if (code) {
      setLoadingCode(true);
      const {data} = await axios.get('http://127.0.0.1:5000/getStockInfo?code='+code+'&filter='+filter);
      const {status, result, msg} = data;
      console.log({status, result});
      setLoadingCode(false);
      if (status === 'ERROR') {
        setLoadError(msg);
        return;
      }
      setLoadError('');
      setCode(result);
    }
    else {
      setLoadingCode(false);
      setCode('');
      setLoadError('');
    }
  }
  
  const changeFilter = (filter) => {
    if (code)
      getStockInfo(code.name, filter);
    setCurrentFilter(filter);
  }

  return (
    <div className="App flex flex-col bg-gray-100 h-screen">
      <Header setCode={getStockInfo} currentFilter={currentFilter} changeFilter={changeFilter} />
      <Contents code={code} currentFilter={currentFilter} loadingCode={loadingCode} loadError={loadError} />
    </div>
  );
}

export default App;
