import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const [activeTab, setActiveTab] = useState("login"); // Toggle between 'login' and 'register'
  const [registerData, setRegisterData] = useState({ username: "", password: "", role: "employee" });
  const [loginData, setLoginData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const res = await fetch("https://lightweight-feedback-system-backend.onrender.com/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(registerData),
      });
      const data = await res.json();
      setMessage(res.ok ? "✅ " + data.msg : "❌ " + data.detail);
    } catch {
      setMessage("❌ Registration failed.");
    }
  };

  const handleLogin = async () => {
    try {
      const res = await fetch("https://lightweight-feedback-system-backend.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });
      const data = await res.json();
      if (res.ok) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("role", data.role);

        if (data.role === "manager"){
          navigate("/manager-dashboard");
        } else if (data.role === "employee"){
          navigate("/employee-dashboard");
        }
        else {
          navigate("/unauthorized");
        }
        
      } else {
        setMessage("❌ " + data.detail);
      }
    } catch {
      setMessage("❌ Login failed.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-lg w-full max-w-md p-6">
        {/* Tabs */}
        <div className="flex justify-center mb-6">
          <button
            className={`px-4 py-2 rounded-t-md font-semibold ${activeTab === "login" ? "bg-green-500 text-white" : "bg-gray-200"}`}
            onClick={() => {
              setActiveTab("login");
              setMessage("");
            }}
          >
            Login
          </button>
          <button
            className={`px-4 py-2 rounded-t-md font-semibold ml-2 ${activeTab === "register" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
            onClick={() => {
              setActiveTab("register");
              setMessage("");
            }}
          >
            Register
          </button>
        </div>

        {/* Form */}
        {activeTab === "login" ? (
          <div>
            <input
              type="text"
              placeholder="Username"
              onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
              className="w-full p-2 border mb-3 rounded"
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
              className="w-full p-2 border mb-3 rounded"
            />
            <button
              onClick={handleLogin}
              className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600"
            >
              Login
            </button>
          </div>
        ) : (
          <div>
            <input
              type="text"
              placeholder="Username"
              onChange={(e) => setRegisterData({ ...registerData, username: e.target.value })}
              className="w-full p-2 border mb-3 rounded"
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })}
              className="w-full p-2 border mb-3 rounded"
            />
            <select
              value={registerData.role}
              onChange={(e) => setRegisterData({ ...registerData, role: e.target.value })}
              className="w-full p-2 border mb-3 rounded"
            >
              <option value="employee">Employee</option>
              <option value="manager">Manager</option>
            </select>
            <button
              onClick={handleRegister}
              className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              Register
            </button>
          </div>
        )}
        {/* Message */}
        {message && <p className="text-sm mt-3 text-red-500">{message}</p>}
      </div>
    </div>
  );
};

export default Home;
