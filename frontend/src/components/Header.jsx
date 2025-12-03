import React from 'react';

export default function Header() {
  const handleSignOut = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  return (
    <header className="bg-white shadow p-4 mb-6">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-xl font-semibold">Personal Finance Dashboard</h1>
        <button 
          className="px-3 py-1 border rounded hover:bg-gray-100" 
          onClick={handleSignOut}
        >
          Sign out
        </button>
      </div>
    </header>
  );
}
