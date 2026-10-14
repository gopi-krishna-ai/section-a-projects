import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, Send, Phone, Video } from 'lucide-react';
import api from '../api';

export default function Inbox() {
  const [contacts, setContacts] = useState([]);
  const [activeContact, setActiveContact] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [userId, setUserId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Get current user id from local profile
    api.get('/auth/me').then(res => setUserId(res.data.id)).catch(console.error);
    
    // Fetch contacts
    fetchContacts();
  }, []);

  async function fetchContacts() {
    try {
      const res = await api.get('/messages/contacts');
      setContacts(res.data);
      if (res.data.length > 0 && !activeContact) {
        setActiveContact(res.data[0]);
      }
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (activeContact) {
      fetchMessages(activeContact.id);
      // Optional polling can be added here
      const interval = setInterval(() => fetchMessages(activeContact.id), 3000);
      return () => clearInterval(interval);
    }
  }, [activeContact]);

  async function fetchMessages(contactId) {
    try {
      const res = await api.get(`/messages/${contactId}`);
      setMessages(res.data);
      scrollToBottom();
    } catch (err) {
      console.error(err);
    }
  }

  function scrollToBottom() {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  async function sendMessage(e) {
    e.preventDefault();
    if (!inputMessage.trim() || !activeContact) return;
    try {
      await api.post(`/messages/${activeContact.id}`, { content: inputMessage });
      setInputMessage('');
      fetchMessages(activeContact.id);
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-[calc(100vh-4rem)]">
      <div className="flex bg-white/80 backdrop-blur-md rounded-2xl shadow-sm border border-white/40 h-full overflow-hidden">
        
        {/* Contact List */}
        <div className="w-80 border-r border-gray-100 flex flex-col">
          <div className="p-4 border-b border-gray-100">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-blue-500" /> Inbox
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto">
            {contacts.length === 0 ? (
              <div className="p-4 text-gray-500 text-sm text-center">No active chats found.</div>
            ) : (
              contacts.map((contact) => (
                <div 
                  key={contact.id} 
                  onClick={() => setActiveContact(contact)}
                  className={`p-4 border-b border-gray-50 cursor-pointer hover:bg-gray-50 ${activeContact?.id === contact.id ? 'bg-blue-50/50' : ''}`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <h4 className="font-bold text-sm">{contact.name}</h4>
                    <span className="text-xs font-bold text-blue-500">{contact.role}</span>
                  </div>
                  <p className="text-xs text-gray-500 truncate">Regarding: {contact.rental_context}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 flex flex-col bg-gray-50/30">
          {activeContact ? (
            <>
              <div className="p-4 bg-white/50 border-b border-gray-100 flex justify-between items-center">
                <div>
                  <h3 className="font-bold">{activeContact.name}</h3>
                  <p className="text-xs text-green-500">Online • {activeContact.role}</p>
                </div>
                <div className="flex gap-3 text-gray-400">
                  <Phone className="w-5 h-5 cursor-pointer hover:text-blue-500" />
                  <Video className="w-5 h-5 cursor-pointer hover:text-blue-500" />
                </div>
              </div>
              
              <div className="flex-1 p-4 overflow-y-auto space-y-4">
                {messages.map(msg => {
                  const isMine = msg.sender_id === userId;
                  return (
                    <div key={msg.id} className={`flex ${isMine ? 'justify-end' : 'justify-start'}`}>
                      <div className={`${isMine ? 'bg-rentmate-green text-white rounded-tr-sm' : 'bg-white rounded-tl-sm border border-gray-100'} p-3 rounded-2xl shadow-sm max-w-md`}>
                        {msg.content}
                        <div className={`text-[10px] mt-1 ${isMine ? 'text-green-100' : 'text-gray-400'}`}>
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  );
                })}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={sendMessage} className="p-4 bg-white/80 border-t border-gray-100 flex gap-2">
                <input 
                  type="text" 
                  value={inputMessage}
                  onChange={e => setInputMessage(e.target.value)}
                  placeholder="Type a message..." 
                  className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:border-rentmate-green" 
                />
                <button type="submit" disabled={!inputMessage.trim()} className="bg-blue-500 text-white p-2 w-10 h-10 rounded-full flex items-center justify-center hover:bg-blue-600 disabled:opacity-50">
                  <Send className="w-4 h-4 ml-1" />
                </button>
              </form>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-400 flex-col">
              <MessageSquare className="w-12 h-12 mb-2 text-gray-300" />
              <p>Select a contact to view your conversation.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
