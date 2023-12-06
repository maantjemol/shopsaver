// The search bar component is for filtering the data based on user input

import { useState } from "react";
import { FaSearch } from "react-icons/fa";
import "./Serachbar.css";

export const Searchbar = ({ setResults, data }) => {
  // this will refresh the page with our chosen input (setInput)

  const [input, setInput] = useState("");
  // This is to manage user input in the search bar. 
  const getData = (value) => {
    // getting data from:
    const results = data.filter((element) => {
      // filtering on the 'name':
      return element.name.toLowerCase().includes(value.toLowerCase());
    });

    setResults(results);
  };

  const handleChange = (value) => {
    // This handles input changes based on the new input and update it
    setInput(value);
    // Trigger data filtering with the updated input value
    getData(value);
  };

  return (
    <div className="input-wrapper">
      <FaSearch id="search-icon" />
      <input
        placeholder="Selecteer product..."
        value={input}
        onChange={(e) => handleChange(e.target.value)}
      />
    </div>
  );
};
