import React, { useEffect, useState } from 'react';
import api from '../api';
import TransactionsTable from './TransactionsTable';
import BudgetForm from './BudgetForm';
import QuickActions from './QuickActions';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const accountsRes = await api.get('/finances/linked-accounts').catch(() => ({ data: [] }));
        setAccounts(accountsRes.data || []);
        if (accountsRes.data && accountsRes.data.length > 0) {
          const id = accountsRes.data[0].id;
          const tx = await api.get(`/finances/transactions/${id}`).catch(() => ({ data: [] }));
          setTransactions(tx.data || []);
        }
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const chartData = transactions.slice(0, 30).map((t) => ({ date: new Date(t.date).toLocaleDateString(), amount: t.amount }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <section className="lg:col-span-2">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-lg font-medium mb-2">Recent Transactions</h2>
          <TransactionsTable transactions={transactions} />
        </div>

        <div className="bg-white p-4 rounded shadow mt-6">
          <h2 className="text-lg font-medium mb-2">Balance over time</h2>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={chartData}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="amount" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <aside>
        <div className="bg-white p-4 rounded shadow mb-6">
          <QuickActions />
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium">Budgets</h3>
          <BudgetForm />
        </div>
      </aside>
    </div>
  );
}
