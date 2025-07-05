import React from "react";

const Dashboard = () => {
  const role = localStorage.getItem("role") || "unknown";

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-green-100 text-center">
      <h1 className="text-3xl font-bold mb-4">🎉 Welcome to the Dashboard</h1>
      <p className="text-lg">Logged in as: <strong>{role}</strong></p>
    </div>
  );
};

export default Dashboard;
