import React, {useState, useEffect } from 'react';

function DataFetcher() {
    const [data, setData] = useState(null);
  
    useEffect(() => {
      fetch('https://api.example.com/data')
        .then(response => response.json())
        .then(json => setData(json))
        .catch(error => console.error(error));
    }, []);

    return (
        <div>

          {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
        </div>
      );
    }
    
export default DataFetcher;
