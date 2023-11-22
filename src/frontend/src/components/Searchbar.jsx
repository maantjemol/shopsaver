import { useState } from "react";
import { FaSearch } from "react-icons/fa";
import "./Serachbar.css";

export const Searchbar = ({ setResults, data }) => {
  // this will refresh the page with our chosen input (setInput)

  const [input, setInput] = useState("");

  const getData = (value) => {
    // getting data from:
    const results = data.filter((element) => {
      // filtering on:
      return element.name.toLowerCase().includes(value.toLowerCase());
    });

    setResults(results);
  };

  const handleChange = (value) => {
    setInput(value);
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
