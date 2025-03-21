import React, { useState, useEffect } from "react";

const Dashboard = ({ token, setToken }) => {
  const [message, setMessage] = useState("");
  const [resourceGroups, setResourceGroups] = useState([]);
  const [products, setProducts] = useState([])


  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched data:", data);
        setResourceGroups(data.resource_groups || []);
        setMessage(data.message);
      })
      .catch(() => setMessage("Unauthorized"));
  }, [token]);

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
      <h2>Dashboard</h2>
      <p>{message}</p>
      <ul>
        {resourceGroups.length > 0 ? (
          resourceGroups.map((rg, index) => (
            <li key={index}>
              <strong>{rg.name}</strong> - {rg.location}
              <ul>
                {products.length > 0 ? (
                  products.map((p, pindex) => (
                    <li key={pindex}>
                      <strong>{p.name}</strong>
                    </li>
                  )
                  )
                ) : (
                  <p>No products found</p>
                )}
              </ul>
            </li>
          ))
        ) : (
          <p>No resource groups found</p>
        )}
      </ul>

      <button onClick={() => setToken("")}>Logout</button>
    </div>
  );
};

export default Dashboard;
