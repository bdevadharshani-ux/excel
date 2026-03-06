import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, Upload, MessageSquare, Activity, LogOut } from 'lucide-react';
import { useAuth } from '@/state/AuthContext';

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/upload', icon: Upload, label: 'Upload' },
    { path: '/query', icon: MessageSquare, label: 'Query' },
    { path: '/monitoring', icon: Activity, label: 'Monitoring' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="fixed left-0 top-0 h-screen w-64 glass-effect border-r border-white/5 flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-gradient">RAG System</h1>
        <p className="text-xs text-zinc-500 mt-1">Knowledge Discovery</p>
      </div>

      <nav className="flex-1 px-4">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.label.toLowerCase()}`}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all duration-200 ${
                isActive
                  ? 'bg-violet-600/20 text-violet-400 border border-violet-500/30'
                  : 'text-zinc-400 hover:bg-white/5 hover:text-white'
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/5">
        <div className="px-4 py-2 mb-2">
          <p className="text-xs text-zinc-500">Logged in as</p>
          <p className="text-sm text-zinc-300 truncate">{user?.email}</p>
        </div>
        <button
          data-testid="logout-button"
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-3 rounded-lg w-full text-zinc-400 hover:bg-red-500/10 hover:text-red-400 transition-all"
        >
          <LogOut size={20} />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </div>
  );
}