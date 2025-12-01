import React, { useState } from 'react'

export default function BudgetForm(){
  const [category, setCategory] = useState('')
  const [amount, setAmount] = useState('')

  const submit = (e) => {
    e.preventDefault()
    // TODO: call API to save
    alert(`Saved budget ${category} ${amount}`)
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-2">
      <input value={category} onChange={e=>setCategory(e.target.value)} placeholder="Category" className="p-2 border rounded" />
      <input value={amount} onChange={e=>setAmount(e.target.value)} placeholder="Amount" className="p-2 border rounded" />
      <button className="p-2 bg-blue-600 text-white rounded">Save Budget</button>
    </form>
  )
}
