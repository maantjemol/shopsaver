import React from "react";

import "./SearchResultsList.css";
import { SearchResult } from "./SearchResult";
/**
 * SearchResultsList Component
 * Displays a list of search results in the Searchbar component.
 */

export const SearchResultsList = ({ results, clickAction }) => {
  return (
    <div className="results-list">
      {results.map((result) => {
        return (
          <SearchResult
            result={result}
            key={result.product_id}
            clickAction={clickAction}
          />
        );
      })}
    </div>
  );
};
