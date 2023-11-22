import { useState } from 'react'
import './App.css'
import { Searchbar } from './components/Searchbar'
import { SearchResultsList } from './components/SearchresultsList'
import {DataFetcher} from './components/DataFetcher';

function App() {
  const[results, setResults] = useState([])

  return (
      <div className='App'>
        <div className='search-bar-container'> 
            <Searchbar setResults ={setResults}/>
            <SearchResultsList results={results} />
        </div>
      </div>
  )
}

export default App
