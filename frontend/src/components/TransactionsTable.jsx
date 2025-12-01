import React from 'react'

export default function TransactionsTable({ transactions = [] }){
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-left">
        <thead>
          <tr>
            <th className="p-2">Date</th>
            <th className="p-2">Description</th>
            <th className="p-2">Category</th>
            <th className="p-2 text-right">Amount</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map(tx => (
            <tr key={tx.id} className="border-t">
              <td className="p-2">{new Date(tx.date).toLocaleDateString()}</td>
              <td className="p-2">{tx.description || '—'}</td>
              <td className="p-2">{tx.category || 'Uncategorized'}</td>
              <td className="p-2 text-right">{Number(tx.amount).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
