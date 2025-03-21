import React, { useState, useEffect } from "react";
import Products from "./Products";

const ResourceGroup = ({ token, resourceGroups }) => {
  const [message, setMessage] = useState("");
  const [products, setProducts] = useState([])

  useEffect(() => {
    
    if (resourceGroups.length === 0) {
      return
    }
    console.log("Calling products")

    // Define your request payload
    const requestData = {
      rg_name: resourceGroups[0].name,  // Example data to send
    };


    fetch("http://127.0.0.1:8000/products/", {
      method: "POST",  // Use POST method to send data
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'  // Ensure you're sending JSON 
      },
      body: JSON.stringify(requestData),  // Convert the JavaScript object to JSON string
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        setProducts(data.products || []);
      })
      .catch(() => setMessage("Unauthorized"));

  }, resourceGroups)

  return (
    <div>
      <p>{message}</p>
      <ul>
        {resourceGroups.length > 0 ? (
          resourceGroups.map((rg, index) => (
            <li key={index}>
              <strong>{rg.name}</strong> - {rg.location}
              <Products token={token} products={products}/>
            </li>
          ))
        ) : (
          <p>No resource groups found</p>
        )}
      </ul>
    </div>
  );
};

export default ResourceGroup;
