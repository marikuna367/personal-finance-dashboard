import React, { useState } from 'react';
import api from '../api';

export default function Header() {
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('password');

  const handleSignIn = async () => {
    try {
      const response = await api.post('/auth/login', { email, password });
      if (response?.data?.access_token) {
        localStorage.setItem('token', response.data.access_token);
        alert('Signed in successfully!');
        window.location.reload();
      } else {
        alert('Sign in failed');
      }
    } catch (error) {
      console.error('Login failed', error);
      alert('Sign in failed');
    }
  };

  const handleSignOut = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  return (
    <header className="bg-white shadow p-4 mb-6">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-xl font-semibold">Personal Finance Dashboard</h1>
        <div className="flex items-center space-x-2">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="border px-2 py-1 rounded"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border px-2 py-1 rounded"
          />
          <button className="px-3 py-1 border rounded" onClick={handleSignIn}>
            Sign in
          </button>
          <button className="px-3 py-1 border rounded" onClick={handleSignOut}>
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
}
