// components/WelcomeView.tsx (Zerodha Version)
import { useEffect, useState } from 'react';
import {
  ArrowRight,
  LineChart,
  TrendingUp,
  ShieldCheck,
  PhoneCall,
  Wallet,
} from 'lucide-react';
import { Button } from '@/components/livekit/button';

interface WelcomeViewProps {
  startButtonText?: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText = 'Talk to a Zerodha Expert',
  onStartCall,
}: WelcomeViewProps) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  return (
    <div className="relative min-h-screen overflow-hidden bg-white text-slate-900">
      
      {/* Subtle Fintech Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50" />

      {/* Floating stock icons */}
      <div className="pointer-events-none absolute inset-0">
        {[LineChart, TrendingUp, Wallet].map((Icon, i) => (
          <div
            key={i}
            className="animate-float absolute opacity-20 text-blue-500"
            style={{
              top: `${15 + i * 20}%`,
              left: i % 2 ? '75%' : '10%',
            }}
          >
            <Icon className="h-20 w-20" />
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-6 py-12">
        <div
          className={`max-w-4xl text-center transition-all duration-1000 ${
            mounted ? 'translate-y-0 opacity-100' : 'translate-y-12 opacity-0'
          }`}
        >
          {/* Zerodha Style Logo */}
          <div className="mb-10">
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <LineChart className="h-16 w-16 text-blue-600" strokeWidth={2.5} />
            </div>
          </div>

          {/* Hero Title */}
          <h1 className="mb-5 text-5xl font-extrabold tracking-tight text-slate-900">
            Invest Smart with India’s #1 Broker
          </h1>

          <p className="mx-auto mb-12 max-w-2xl text-lg leading-relaxed text-slate-600">
            1.5+ crore investors trust Zerodha  
            <span className="font-semibold text-blue-600"> • Zero brokerage on equity delivery</span>
          </p>

          {/* Benefits */}
          <div className="mb-12 grid grid-cols-2 gap-6 md:grid-cols-4">
            {[
              { icon: TrendingUp, label: '₹0 Equity Delivery' },
              { icon: ShieldCheck, label: 'Highest Safety' },
              { icon: Wallet, label: 'Lowest Charges' },
              { icon: PhoneCall, label: 'Expert Assistance' },
            ].map(({ icon: Icon, label }) => (
              <div
                key={label}
                className="flex flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-6 shadow-sm transition hover:scale-105"
              >
                <Icon className="h-8 w-8 text-blue-600" />
                <span className="text-sm font-semibold">{label}</span>
              </div>
            ))}
          </div>

          {/* CTA */}
          <Button
            onClick={onStartCall}
            className="rounded-full bg-blue-600 px-14 py-6 text-xl font-semibold text-white transition hover:bg-blue-700"
          >
            {startButtonText}
            <ArrowRight className="ml-3 h-6 w-6" />
          </Button>

          {/* Subtext */}
          <p className="mt-5 text-sm text-slate-500">
            Quick consultation • Safe & regulated investments
          </p>
        </div>
      </div>

      {/* Float Animation */}
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-12px); }
        }
        .animate-float {
          animation: float 8s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};
