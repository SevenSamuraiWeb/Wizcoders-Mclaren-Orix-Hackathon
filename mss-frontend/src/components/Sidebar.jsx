import React from 'react';
import { LayoutDashboard, FileText, Settings, PieChart } from 'lucide-react';

const Sidebar = () => {
    return (
        <div className="w-64 bg-slate-900 text-white flex flex-col h-full border-r border-slate-800">
            <div className="p-6">
                <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-emerald-400 bg-clip-text text-transparent">
                    CreditMemo AI
                </h1>
            </div>

            <nav className="flex-1 px-4 space-y-2">
                <a href="#" className="flex items-center space-x-3 px-4 py-3 bg-slate-800 rounded-lg text-emerald-400">
                    <FileText size={20} />
                    <span className="font-medium">Analysis</span>
                </a>
                <a href="#" className="flex items-center space-x-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                    <LayoutDashboard size={20} />
                    <span className="font-medium">Dashboard</span>
                </a>
                <a href="#" className="flex items-center space-x-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                    <PieChart size={20} />
                    <span className="font-medium">Reports</span>
                </a>
                <a href="#" className="flex items-center space-x-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors">
                    <Settings size={20} />
                    <span className="font-medium">Settings</span>
                </a>
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
