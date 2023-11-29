import React from 'react'

export default function Winkels(props){
    return(
        <div className='Winkels'>
          <img src={props.img} />
            {/* {priceData.map((item) => (
            <div 
             key={item.Store_name}>
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
          ))} */}
        </div>
    )
}