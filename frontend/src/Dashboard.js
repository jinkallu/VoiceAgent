import React, { useState, useEffect } from "react";

const Dashboard = ({ token }) => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/protected/", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Unauthorized"));
  }, [token]);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
      <button onClick={() => localStorage.removeItem("token")}>Logout</button>
    </div>
  );
};

export default Dashboard;
