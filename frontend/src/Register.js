import React, { useState } from "react";

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async () => {
    setIsLoading(true); // Disable button and show loading indicator
  
    try {
      const response = await fetch("http://127.0.0.1:8000/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
  
      const data = await response.json();
      console.log("Response Data:", data);  // Log the response data
  
      if (!response.ok) {
        setMessage(data.msg || data.detail || "Registration failed");
        return;
      }
  
      setMessage(data.message || "Registration successful!");
    } catch (error) {
      console.error("Error during registration:", error);
      setMessage("An error occurred during registration.");
    } finally {
      setIsLoading(false); // Re-enable the button after the response
    }
  };
  
  return (
    <div>
      <h2>Register</h2>
      {message && <p>{typeof message === 'object' ? JSON.stringify(message) : message}</p>}
      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleRegister} disabled={isLoading}>
        {isLoading ? "Registering..." : "Register"}
      </button>
      <p>Already have an account? <a href="/login/">Login here</a></p>
    </div>
  );
};

export default Register;
