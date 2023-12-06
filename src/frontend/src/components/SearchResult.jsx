import "./SearchResult.css";

/**
 * SearchResult Component
 * Represents a single item in the search results displayed by the Searchbar component.
 */

export const SearchResult = ({ result, clickAction }) => {
  /**
 * This handles the click action on the search result.
 */
  return (
    <div className="search-result" onClick={() => clickAction(result)}>
      {result.name}
    </div>
  );
};
