import { useState } from "react";
import { FaSearch } from "react-icons/fa";
import "./Searchbar.css";

export const Searchbar = ({ setResults, data }) => {
  // this will refresh the page with our chosen input (setInput)

  const [input, setInput] = useState("");

  const getData = (value) => {
    const results = data.filter((element) => {
      return element.name.toLowerCase().includes(value.toLowerCase());
    });
    setResults(results);
  };

  const handleChange = (value) => {
    setInput(value);
    getData(value);
  };

  return (
    <div className="input">
      <FaSearch id="input--search-icon" />
      <input
        placeholder="Selecteer product..."
        value={input}
        onChange={(e) => handleChange(e.target.value)}
      />
    </div>
  );
};
