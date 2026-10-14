import React, { useState, useEffect } from 'react';
import api from '../../api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';

const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#64748b'];

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [items, setItems] = useState([]);
  const [users, setUsers] = useState([]);

  async function fetchData() {
    try {
      const [statsRes, itemsRes, usersRes] = await Promise.all([
        api.get('/admin/analytics'),
        api.get('/admin/items'),
        api.get('/admin/users')
      ]);
      setStats(statsRes.data);
      setItems(itemsRes.data);
      setUsers(usersRes.data);
    } catch(err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  const handleItemStatus = async (id, status) => {
    await api.put(`/admin/items/${id}/status`, { status });
    fetchData();
  };

  if (!stats) return <div className="p-12 text-center">Loading Admin Data...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-6 rounded-xl border shadow-sm text-center">
          <p className="text-sm text-gray-500 mb-1">Total Users</p>
          <p className="text-3xl font-bold">{stats.total_users}</p>
        </div>
        <div className="bg-white p-6 rounded-xl border shadow-sm text-center">
          <p className="text-sm text-gray-500 mb-1">Total Items</p>
          <p className="text-3xl font-bold">{stats.total_items}</p>
        </div>
        <div className="bg-white p-6 rounded-xl border shadow-sm text-center">
          <p className="text-sm text-gray-500 mb-1">Total Rentals</p>
          <p className="text-3xl font-bold">{stats.total_rentals}</p>
        </div>
        <div className="bg-white p-6 rounded-xl border shadow-sm text-center">
          <p className="text-sm text-gray-500 mb-1">Total Revenue</p>
          <p className="text-3xl font-bold">₹{stats.total_revenue}</p>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-8 mb-8">
        <div className="md:col-span-1 bg-white p-6 rounded-xl border shadow-sm h-80">
          <h3 className="font-bold mb-4">Items by Category</h3>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={stats.categories_data} cx="50%" cy="40%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {stats.categories_data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <RechartsTooltip />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div className="md:col-span-2 bg-white rounded-xl border shadow-sm overflow-hidden flex flex-col h-80">
          <div className="p-4 border-b bg-gray-50">
            <h3 className="font-bold">Pending Item Approvals</h3>
          </div>
          <div className="overflow-y-auto p-0 flex-1">
            <table className="w-full text-left text-sm">
              <thead className="bg-white sticky top-0 border-b">
                <tr>
                  <th className="p-3">Item</th>
                  <th className="p-3">Category</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {items.filter(i => i.status === 'PENDING_APPROVAL').map(item => (
                  <tr key={item.id}>
                    <td className="p-3 font-medium">{item.name}</td>
                    <td className="p-3 text-gray-500">{item.category}</td>
                    <td className="p-3"><span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">PENDING</span></td>
                    <td className="p-3 flex gap-2">
                      <button onClick={() => handleItemStatus(item.id, 'APPROVED')} className="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200">Approve</button>
                      <button onClick={() => handleItemStatus(item.id, 'REJECTED')} className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200">Reject</button>
                    </td>
                  </tr>
                ))}
                {items.filter(i => i.status === 'PENDING_APPROVAL').length === 0 && (
                  <tr><td colSpan="4" className="p-6 text-center text-gray-500">No pending approvals.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border shadow-sm overflow-hidden">
        <div className="p-4 border-b bg-gray-50">
          <h3 className="font-bold">User Directory</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="bg-white border-b">
                <th className="p-4">Name</th>
                <th className="p-4">Email</th>
                <th className="p-4">Role</th>
                <th className="p-4">Eco Score</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {users.map(user => (
                <tr key={user.id}>
                  <td className="p-4 font-medium">{user.name}</td>
                  <td className="p-4 text-gray-500">{user.email}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${user.role==='OWNER'?'bg-blue-100 text-blue-800':user.role==='RENTER'?'bg-green-100 text-green-800':'bg-purple-100 text-purple-800'}`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-1">
                      <span className="text-green-600 font-bold">+{user.eco_score}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
