import { useEffect, useState } from 'react'
import './App.css'
import { Searchbar } from './components/Searchbar'
import { SearchResultsList } from './components/SearchresultsList'
import {DataFetcher} from './components/DataFetcher';

function App() {
  const [results, setResults] = useState([])
  const [groceryList, setGroceryList] = useState([])

  const clickAction = (id) => {
    setGroceryList((oldlist) => {
      oldlist.push(id)
      return oldlist
    })
  }


  return (
      <div className='App'>
        <div className='search-bar-container'> 
            <Searchbar setResults ={setResults}/>
            <SearchResultsList results={results} clickAction={clickAction} />
        </div>
        <ul>
        {groceryList.map((item, i) => <li key={item + i}> 
          {item}
        </li>)}
        </ul>
      </div>
  )
}

export default App
