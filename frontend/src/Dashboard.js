import React, { useState, useEffect } from "react";

const Dashboard = ({ token }) => {
  const [message, setMessage] = useState("");
  const [resourceGroups, setResourceGroups] = useState([]);


  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setResourceGroups(data.resource_groups || []))
      .catch(() => setMessage("Unauthorized"));
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
      <ul>
          {resourceGroups.length > 0 ? (
            resourceGroups.map((rg, index) => (
              <li key={index}>
                <strong>{rg.name}</strong> - {rg.location}
              </li>
            ))
          ) : (
            <p>No resource groups found</p>
          )}
        </ul>
      <button onClick={() => localStorage.removeItem("token")}>Logout</button>
    </div>
  );
};

export default Dashboard;
