import React from 'react';
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle, ArrowRight, File as FileIcon } from 'lucide-react';

const Card = ({ title, icon: Icon, children, className = "" }) => (
    <div className={`bg-white rounded-xl shadow-sm border border-slate-200 p-5 ${className}`}>
        <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-slate-800 flex items-center space-x-2">
                {Icon && <Icon size={18} className="text-indigo-500" />}
                <span>{title}</span>
            </h3>
        </div>
        {children}
    </div>
);

const AnalysisDashboard = () => {
    return (
        <div className="h-full overflow-y-auto space-y-6 pr-2">
            {/* Executive Summary */}
            <Card title="Executive Summary" icon={FileIcon}>
                <div className="space-y-3 animate-pulse">
                    <div className="h-4 bg-slate-100 rounded w-full"></div>
                    <div className="h-4 bg-slate-100 rounded w-5/6"></div>
                    <div className="h-4 bg-slate-100 rounded w-4/6"></div>
                </div>
                <div className="mt-4 pt-4 border-t border-slate-100 flex justify-end">
                    <button className="text-sm text-indigo-600 font-medium flex items-center hover:text-indigo-700">
                        View detailed summary <ArrowRight size={14} className="ml-1" />
                    </button>
                </div>
            </Card>

            {/* Key Metrics Grid */}
            <div className="grid grid-cols-2 gap-4">
                <Card title="Revenue Growth" icon={TrendingUp}>
                    <div className="h-16 flex items-end space-x-2 justify-between px-2">
                        <div className="w-2 bg-indigo-100 h-8 rounded-t"></div>
                        <div className="w-2 bg-indigo-200 h-10 rounded-t"></div>
                        <div className="w-2 bg-indigo-300 h-14 rounded-t"></div>
                        <div className="w-2 bg-indigo-400 h-12 rounded-t"></div>
                        <div className="w-2 bg-indigo-500 h-16 rounded-t"></div>
                    </div>
                    <div className="mt-2 text-right">
                        <span className="text-2xl font-bold text-slate-800">+12%</span>
                        <span className="text-xs text-emerald-500 ml-1">YoY</span>
                    </div>
                </Card>
                <Card title="Risk Score" icon={AlertTriangle}>
                    <div className="flex items-center justify-center h-16">
                        <div className="text-3xl font-bold text-emerald-500">
                            Low
                        </div>
                    </div>
                    <div className="mt-2 text-center text-xs text-slate-400">
                        Calculated based on 15 factors
                    </div>
                </Card>
            </div>

            {/* Financial Metrics */}
            <Card title="Financial Metrics" icon={BarChart3}>
                <div className="space-y-4">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400">
                                    #
                                </div>
                                <div>
                                    <div className="h-3 w-24 bg-slate-100 rounded mb-1"></div>
                                    <div className="h-2 w-16 bg-slate-50 rounded"></div>
                                </div>
                            </div>
                            <div className="h-4 w-12 bg-slate-100 rounded"></div>
                        </div>
                    ))}
                </div>
            </Card>

            {/* Risk Assessment */}
            <Card title="Risk Assessment" icon={CheckCircle}>
                <div className="space-y-2">
                    <div className="flex items-start space-x-3 p-3 rounded-lg bg-emerald-50 border border-emerald-100">
                        <CheckCircle size={16} className="text-emerald-500 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-emerald-800">Strong Cash Flow Support</p>
                            <p className="text-xs text-emerald-600">Company shows consistent positive operating cash flow.</p>
                        </div>
                    </div>
                    <div className="flex items-start space-x-3 p-3 rounded-lg bg-amber-50 border border-amber-100">
                        <AlertTriangle size={16} className="text-amber-500 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-amber-800">High Leverage Ratio</p>
                            <p className="text-xs text-amber-600">Debt-to-equity ratio is slightly above industry average.</p>
                        </div>
                    </div>
                </div>
            </Card>
        </div>
    );
};

export default AnalysisDashboard;
