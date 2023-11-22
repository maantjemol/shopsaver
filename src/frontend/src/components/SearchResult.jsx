import "./SearchResult.css";

export const SearchResult = ({ result, clickAction }) => {
  return (
    <div
      className="search-result"
      onClick={(e) => clickAction(result)}>{result}
    </div>
  );
};

