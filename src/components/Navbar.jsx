// src/components/Navbar.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

const Navbar = ({ role }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  return (
    <nav className="bg-blue-700 text-white px-6 py-4 flex justify-between items-center shadow">
      <div className="text-lg font-bold">Feedback System ({role})</div>
      <button
        onClick={handleLogout}
        className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded text-sm"
      >
        Logout
      </button>
    </nav>
  );
};

export default Navbar;
