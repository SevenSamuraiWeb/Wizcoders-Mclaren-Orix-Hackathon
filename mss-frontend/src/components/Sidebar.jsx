import React from 'react';
import { LayoutDashboard, FileText, Settings, PieChart } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { path: '/', label: 'Analysis', icon: FileText },
        { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/reports', label: 'Reports', icon: PieChart },
        { path: '/settings', label: 'Settings', icon: Settings },
    ];

    return (
        <div className="w-64 bg-slate-900 text-white flex flex-col h-full border-r border-slate-800">
            <div className="p-6">
                <Link to="/">
                    <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-emerald-400 bg-clip-text text-transparent">
                        CreditMemo AI
                    </h1>
                </Link>
            </div>

            <nav className="flex-1 px-4 space-y-2">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;
                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${isActive
                                    ? 'bg-slate-800 text-emerald-400'
                                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                }`}
                        >
                            <Icon size={20} />
                            <span className="font-medium">{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-slate-800">
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-sm font-bold">
                        JD
                    </div>
                    <div className="text-sm">
                        <p className="text-white font-medium">John Doe</p>
                        <p className="text-slate-500">Analyst</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
