import React from "react";

import "./SearchResultsList.css";
//import { SearchResult } from "./SearchResult";

export const SearchResultsList = ({ results, clickAction }) => {
  return (
    <div className="results--list">
      {results.map((result) => {
        return (
          <div className="search--result" onClick={() => clickAction(result)}>
            {result.name}
          </div>
        );
      })}
    </div>
  );
};
