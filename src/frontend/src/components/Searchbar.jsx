import React, {useState} from 'react';
import {FaSearch} from "react-icons/fa";
import "./Serachbar.css"


export const Searchbar = ({setResults})=> {
    // this will refresh the page with our chosen input (setInput)
        const [input, setInput] = useState("")

        const getData = (value) => {
            // getting data from:
            fetch("https://jsonplaceholder.typicode.com/users")
              .then((response) => response.json())
              .then((json) => {
                const results = json.filter((user) =>{
                    // filtering on:
                    return (
                        value &&
                        user &&
                        user.name &&
                        user.name.toLowerCase().includes(value)
                      );
                })
                setResults(results);
               });
        };
    const handleChange = (value) => {
        setInput(value);
        getData(value);
    };

    return (
        <div className ="input-wrapper">
        <FaSearch id="search-icon" /> 
        <input placeholder="Selecteer product..." value={input} onChange={(e) => handleChange(e.target.value)}/>
        </div>

    )
}

