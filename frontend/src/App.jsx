import React from 'react'
import Dashboard from './components/Dashboard'
import Header from './components/Header'

export default function App(){
  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto p-4">
        <Dashboard />
      </main>
    </div>
  )
}
