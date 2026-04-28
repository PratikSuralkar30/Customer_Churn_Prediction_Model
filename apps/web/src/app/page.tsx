"use client";

import { useState } from "react";
import { AlertCircle, ArrowRight, BarChart3, CheckCircle2, ShieldAlert, User, Zap } from "lucide-react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [explanation, setExplanation] = useState<any>(null);

  const [formData, setFormData] = useState({
    gender: "Female",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "No",
    tenure: 12,
    PhoneService: "Yes",
    MultipleLines: "No",
    InternetService: "Fiber optic",
    OnlineSecurity: "No",
    OnlineBackup: "Yes",
    DeviceProtection: "No",
    TechSupport: "No",
    StreamingTV: "Yes",
    StreamingMovies: "Yes",
    Contract: "Month-to-month",
    PaperlessBilling: "Yes",
    PaymentMethod: "Electronic check",
    MonthlyCharges: 85.5,
    TotalCharges: 1000.0
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === "tenure" || name === "SeniorCitizen" || name.includes("Charges") || name.includes("tickets") || name.includes("breaches") || name.includes("days") || name.includes("hours")
        ? Number(value) : value
    }));
  };

  const handlePredict = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setExplanation(null);

    try {
      const scoreRes = await fetch("http://localhost:8000/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const scoreData = await scoreRes.json();
      setResult(scoreData);

      const explainRes = await fetch("http://localhost:8000/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const explainData = await explainRes.json();
      setExplanation(explainData);
    } catch (err) {
      console.error(err);
      alert("Error connecting to prediction backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <header className="mb-12 border-b border-white/10 pb-6 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
              <Zap className="text-indigo-400 h-8 w-8" />
              SuccessOps<span className="text-indigo-400"> AI</span>
            </h1>
            <p className="mt-2 text-slate-400 text-lg">Predict customer churn and deploy targeted retention actions.</p>
          </div>
          <div className="hidden sm:flex items-center gap-4 bg-white/5 px-4 py-2 rounded-full border border-white/10">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-sm font-medium text-emerald-400">Models Online</span>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-7 bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-sm shadow-2xl">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                <User className="h-6 w-6 text-indigo-400" /> Customer Profile
              </h2>
            </div>
            
            <form onSubmit={handlePredict} className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Contract Type</label>
                  <select name="Contract" value={formData.Contract} onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all">
                    <option>Month-to-month</option>
                    <option>One year</option>
                    <option>Two year</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Tenure (Months)</label>
                  <input type="number" name="tenure" value={formData.tenure} onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-400 mb-2">Monthly Charges ($)</label>
                  <input type="number" step="0.1" name="MonthlyCharges" value={formData.MonthlyCharges} onChange={handleChange} className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all" />
                </div>
              </div>

              <div className="pt-6">
                <button 
                  type="submit" 
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-bold py-4 px-8 rounded-xl shadow-lg shadow-indigo-500/25 transition-all transform hover:-translate-y-1 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <span className="flex items-center gap-2">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Analyzing Profile...
                    </span>
                  ) : (
                    <>Run Churn Prediction <ArrowRight className="h-5 w-5" /></>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-5 space-y-8">
            {result ? (
              <div className={`p-8 rounded-3xl border backdrop-blur-sm shadow-2xl transition-all duration-500 ${result.risk_level === 'High' ? 'bg-rose-500/10 border-rose-500/30 shadow-rose-500/10' : result.risk_level === 'Medium' ? 'bg-amber-500/10 border-amber-500/30 shadow-amber-500/10' : 'bg-emerald-500/10 border-emerald-500/30 shadow-emerald-500/10'}`}>
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-white flex items-center gap-2">
                    {result.risk_level === 'High' ? <ShieldAlert className="text-rose-400" /> : <CheckCircle2 className="text-emerald-400" />}
                    Risk Assessment
                  </h3>
                  <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-wide ${result.risk_level === 'High' ? 'bg-rose-500/20 text-rose-300' : result.risk_level === 'Medium' ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'}`}>
                    {result.risk_level.toUpperCase()} RISK
                  </span>
                </div>
                
                <div className="mt-8 flex flex-col items-center justify-center relative">
                  <div className="text-7xl font-black tabular-nums tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white to-slate-400 mb-2">
                    {(result.churn_probability * 100).toFixed(1)}%
                  </div>
                  <p className="text-slate-400 font-medium">Probability of Churn</p>
                </div>
              </div>
            ) : (
              <div className="h-[250px] bg-white/5 border border-white/10 rounded-3xl flex flex-col items-center justify-center text-slate-500 border-dashed">
                <BarChart3 className="h-12 w-12 mb-4 opacity-50" />
                <p>Run prediction to view risk assessment</p>
              </div>
            )}

            {explanation && (
              <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-sm shadow-2xl transition-all duration-500">
                <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-6">
                  <BarChart3 className="text-indigo-400" /> Key Risk Drivers
                </h3>
                <div className="space-y-5">
                  {explanation.top_drivers.map((driver: any, idx: number) => {
                    const impactPercent = Math.min(100, Math.abs(driver.impact) * 40); // Scaling for visual purpose
                    const isPositive = driver.impact > 0;
                    
                    return (
                      <div key={idx} className="relative">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="font-medium text-slate-200 truncate pr-4">{driver.feature.replace(/cat__|num__/g, '')}</span>
                          <span className={isPositive ? "text-rose-400 font-mono" : "text-emerald-400 font-mono"}>
                            {isPositive ? "+" : ""}{driver.impact.toFixed(3)}
                          </span>
                        </div>
                        <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden flex">
                          {isPositive ? (
                            <>
                              <div className="w-1/2"></div>
                              <div className="bg-rose-500 h-full rounded-full" style={{ width: `${impactPercent/2}%` }}></div>
                            </>
                          ) : (
                            <>
                              <div className="w-1/2 flex justify-end">
                                <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${impactPercent/2}%` }}></div>
                              </div>
                              <div className="w-1/2"></div>
                            </>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                <div className="mt-8 pt-6 border-t border-white/10 flex gap-4">
                  <button className="flex-1 bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-4 rounded-xl transition-all text-sm flex items-center justify-center gap-2">
                    Send Discount Offer
                  </button>
                  <button className="flex-1 bg-white/10 hover:bg-white/20 text-white font-medium py-3 px-4 rounded-xl transition-all text-sm flex items-center justify-center gap-2">
                    Schedule Success Call
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
