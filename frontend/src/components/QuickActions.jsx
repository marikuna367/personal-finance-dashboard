import React, { useState } from "react";
import api from "../api";

export default function QuickActions({}) {
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLinkBankAccount() {
    setLoading(true); setMsg("");
    try {
      
      const payload = { provider_account_id: 1, name: "Mock Checking" };
      const res = await api.post("/finances/link-account", payload);
      console.log("linked:", res.data);
      if (res.data?.id) localStorage.setItem("last_linked_account_id", res.data.id);
      setMsg("Linked: " + (res.data?.id ?? JSON.stringify(res.data)));
    } catch (e) {
      console.error(e);
      setMsg("Link failed: " + (e?.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  }

  async function handleSyncAccounts() {
    setLoading(true); setMsg("");
    try {
      const localId = localStorage.getItem("last_linked_account_id") || "1";
      const res = await api.post(`/finances/sync/${localId}`);
      console.log("sync:", res.data);
      setMsg("Synced: " + JSON.stringify(res.data));
    } catch (e) {
      console.error(e);
      setMsg("Sync failed: " + (e?.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  }

  async function handleCreateTransaction() {
    setLoading(true); setMsg("");
    try {
      const payload = {
        account_id: Number(localStorage.getItem("last_linked_account_id") || 1),
        date: new Date().toISOString().slice(0, 10),
        description: "Quick Action Test",
        category: "Misc",
        amount: 7.5
      };
      const res = await api.post("/finances/transactions", payload);
      console.log("create tx:", res.data);
      setMsg("Created tx: " + JSON.stringify(res.data));
    } catch (e) {
      console.error(e);
      setMsg("Create tx failed: " + (e?.response?.data?.detail || e.message));
    } finally { setLoading(false); }
  }

  return (
    <div className="bg-white p-4 rounded shadow-sm">
      <h3 className="font-semibold mb-3">Quick Actions</h3>
      <div className="space-y-2">
        <button onClick={handleLinkBankAccount} disabled={loading} className="w-full border rounded py-2">Link Bank Account</button>
        <button onClick={handleSyncAccounts} disabled={loading} className="w-full border rounded py-2">Sync Accounts</button>
        <button onClick={handleCreateTransaction} disabled={loading} className="w-full border rounded py-2">Create Transaction</button>
        {msg && <div className="text-sm mt-2">{msg}</div>}
      </div>
    </div>
  );
}
