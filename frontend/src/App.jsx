import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import Header from "./components/Header";
import api from "./api";

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(Boolean(localStorage.getItem("token")));
  const [email, setEmail] = useState("demo@example.com");
  const [password, setPassword] = useState("demo123");

  const handleSignIn = async () => {
    try {
      const res = await api.post("/auth/login", { email, password });
      if (!res || !res.data || !res.data.access_token) {
        throw new Error("Login failed");
      }
      localStorage.setItem("token", res.data.access_token);
      setIsLoggedIn(true);
    } catch (err) {
      alert(err?.response?.data?.detail ?? err.message ?? "Login failed");
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="bg-white p-6 rounded shadow w-full max-w-md">
          <h1 className="text-2xl mb-4">Personal Finance Dashboard</h1>
          <input
            type="email"
            placeholder="Email"
            className="w-full p-2 border rounded mb-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full p-2 border rounded mb-4"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleSignIn} className="w-full py-2 bg-blue-600 text-white rounded">
            Sign In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto p-4">
        <Dashboard />
      </main>
    </div>
  );
}

