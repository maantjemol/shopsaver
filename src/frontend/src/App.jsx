import { useEffect, useState } from "react";
import "./App.css";
import { Searchbar } from "./components/Searchbar";
import { SearchResultsList } from "./components/SearchresultsList";
import logo from "./images/shopsaver1.png"
import logo1 from"./images/shopsaver.jpg"
import logo2 from "./images/shop.qua.png"
import logo3 from "./images/shop.png"
import Winkels from "./components/Winkels";
import ahimg from "./images/ah.png"
import jumboimg from "./images/jumbo.logo.png"
import hoogvlietimg from "./images/hoogvliet.logo.png"

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
        <div className="header">
            <img className = "header--img"
                src={logo}/>
            <h1 className="header--title">Shopsaver</h1>
        </div>

        <div className="main">
          <div className="main--welcome">
            <h2 className="main--welcome-text1">Welkom bij</h2>
            <h3 className="main--welcome-text2">ShopSaver</h3>
            <p className="main--p1">De site waar je kan kijken bij welke winkel jij het goedkoopst jou boodschappen kan doen</p>
              <div className="main--search-bar-container">
                <Searchbar setResults={setResults} data={data} />
                <SearchResultsList results={results} clickAction={clickAction} />
              </div>
            </div>

          <div className="main--big-img">
            <img className="main--image-big"
                 src={logo2} width="400px"/>
          </div>

        </div>
            <div className="grocery-list">
              <ul className="list-of-groceries">
                {groceryList.map((item, i) => (
                  <li key={item + i} className="grocery-list-li">
                    <span>{item.name}</span>
                    
                      <button className="removeButton"
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
              </div>
        <div className="button-div">
        <button className="verwijder-button" onClick={() => setGroceryList([])}>Verwijder alles</button>
        </div>
        

        <div className="Winkels">
          {priceData.map((item) => {
            let imgSrc = ""

            if(item.Store_name === "AH") imgSrc = ahimg
            if(item.Store_name === "Jumbo") imgSrc = jumboimg
            if(item.Store_name === "Hoogvliet") imgSrc = hoogvlietimg

            return (
            <div 
             key={item.Store_name}
              className="winkel-container"
              
            >
              
                <div className="winkel-item">
                <img src={imgSrc} className="winkel-image" />
                  <h2>
                    {item.Store_name} - €
                    {item.products.reduce((a, b) => a + b.Sales_price, 0).toFixed(2)}
                  </h2>
                </div>
              
              <ul>
                <div>
                {item.products.map((product) => (
                  <li key={product.Product_id} className="winkel-li">
                    <a className="winkel-text"
                      href={product.Product_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {product.Product_name} - €{product.Sales_price}
                    </a>
                  </li>
                ))}
                </div>
              </ul>
              
            </div>
          )})}
        </div>








        <div>
        {/* <footer className="footer">
          <p>Dit is de footer!</p>
            
        </footer> */}

        </div>





      </div>
    );
  }

export default App;
