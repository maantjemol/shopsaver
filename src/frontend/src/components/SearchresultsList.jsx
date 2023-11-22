import React from "react";

import "./SearchResultsList.css";
import { SearchResult } from "./SearchResult";

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
