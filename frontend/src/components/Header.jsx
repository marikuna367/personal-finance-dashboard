import React from 'react'

export default function Header(){
  return (
    <header className="bg-white shadow p-4 mb-6">
      <div className="container mx-auto flex items-center justify-between">
        <h1 className="text-xl font-semibold">Personal Finance Dashboard</h1>
        <div>
          <button className="px-3 py-1 border rounded">Sign in</button>
        </div>
      </div>
    </header>
  )
}
