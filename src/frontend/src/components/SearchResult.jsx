import "./SearchResult.css";

export const SearchResult = ({ result, clickAction }) => {
  return (
    <div className="search-result" onClick={() => clickAction(result)}>
      {result.name}
    </div>
  );
};
