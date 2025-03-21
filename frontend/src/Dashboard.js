import React, { useState, useEffect } from "react";
import ResourceGroup from "./ResourceGroup";

const Dashboard = ({ token, setToken }) => {
  const [message, setMessage] = useState("");
  const [resourceGroups, setResourceGroups] = useState([]);
  


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

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
      <ResourceGroup token={token} resourceGroups={resourceGroups} />

      <button onClick={() => setToken("")}>Logout</button>
    </div>
  );
};

export default Dashboard;
