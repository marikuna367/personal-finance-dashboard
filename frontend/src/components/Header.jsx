import React, { useState } from 'react'
import axios from 'axios'

export default function Header() {
  const [email, setEmail] = useState('demo@example.com')
  const [password, setPassword] = useState('password')

  const handleSignIn = async () => {
    try {
      const response = await axios.post('http://localhost:8000/auth/login', {
        email,
        password
      })
      console.log('Login successful', response.data)
      alert('Signed in successfully!')
    } catch (error) {
      console.error('Login failed', error)
      alert('Sign in failed')
    }
  }

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
          <button
            className="px-3 py-1 border rounded"
            onClick={handleSignIn}
          >
            Sign in
          </button>
        </div>
      </div>
    </header>
  )
}
