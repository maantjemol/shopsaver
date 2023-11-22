import { useEffect, useState } from "react";
import "./App.css";
import { Searchbar } from "./components/Searchbar";
import { SearchResultsList } from "./components/SearchresultsList";
// import { DataFetcher } from "./components/DataFetcher";

function App() {
  const [results, setResults] = useState([]);
  const [groceryList, setGroceryList] = useState([]);
  const [data, setData] = useState([]);
  const [priceData, setPriceData] = useState([]);

  const serverPort = "http://127.0.0.1:5000";

  useEffect(() => {
    fetch(serverPort + "/api/getalltaxonomies")
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.log(error));
  }, []);

  const clickAction = (id) => {
    setGroceryList((oldlist) => {
      if (oldlist.includes(id)) {
        return oldlist;
      }
      return [...oldlist, id];
    });
  };

  useEffect(() => {
    fetchData();
  }, [groceryList]);

  const fetchData = async () => {
    const taxlist = groceryList.map((item) => item.product_id);
    let headersList = {
      Accept: "*/*",
      "User-Agent": "Thunder Client (https://www.thunderclient.com)",
      "Content-Type": "application/json",
    };
    let bodyContent = JSON.stringify(taxlist);
    let response = await fetch(
      "http://127.0.0.1:5000/api/getitemsbytaxonomie",
      {
        method: "POST",
        body: bodyContent,
        headers: headersList,
      }
    );
    let data = await response.json();
    setPriceData(data);
  };

  return (
    <div className="App">
      <div className="search-bar-container">
        <Searchbar setResults={setResults} data={data} />
        <SearchResultsList results={results} clickAction={clickAction} />
      </div>
      <ul>
        {groceryList.map((item, i) => (
          <li key={item + i}>
            {item.name}
            <button
              onClick={() =>
                setGroceryList((prevList) => {
                  const newList = [...prevList];
                  newList.splice(i, 1);
                  return newList;
                })
              }
            >
              X
            </button>
          </li>
        ))}
      </ul>
      <button onClick={() => setGroceryList([])}>Verwijder alles</button>
      <div>
        {priceData.map((item) => (
          <div key={item.Store_name}>
            <h2>
              {item.Store_name} - €
              {item.products.reduce((a, b) => a + b.Sales_price, 0).toFixed(2)}
            </h2>
            <ul>
              {item.products.map((product) => (
                <li key={product.Product_id}>
                  <a
                    href={product.Product_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {product.Product_name} - €{product.Sales_price}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
