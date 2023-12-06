import React from "react";

import "./SearchResultsList.css";
/**
 * SearchResultsList Component
 * Displays a list of search results in the Searchbar component.
 */

export const SearchResultsList = ({ results, clickAction }) => {
  return (
    <div className="results--list">
      {results.map((result) => {
        return (
          <div
            className="search--result"
            key={result.name}
            onClick={() => clickAction(result)}
          >
            {result.name}
          </div>
        );
      })}
    </div>
  );
};
