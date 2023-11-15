import { useState } from 'react'
import './App.css'
import { Searchbar } from './components/Searchbar'

function App() {
  return (
      <div className='App'>
        <div className='search-bar-container'> 
            <Searchbar />
            <div>SearchResults</div>
        </div>
      </div>
  )
}

export default App
