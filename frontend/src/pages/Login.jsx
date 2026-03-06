import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/state/AuthContext';
import { Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isLogin) {
        await login(email, password);
        toast.success('Login successful!');
        const from = location.state?.from?.pathname || '/dashboard';
        navigate(from, { replace: true });
      } else {
        await register(email, password, name);
        toast.success('Registration successful! Please login.');
        setIsLogin(true);
        setPassword('');
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-zinc-950 relative overflow-hidden">
      {/* Animated Neural Network Background */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-violet-900/20 to-zinc-950"></div>
        <svg className="absolute inset-0 w-full h-full">
          <defs>
            <linearGradient id="line-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#7c3aed" stopOpacity="0.1" />
            </linearGradient>
          </defs>
          {/* Neural network lines */}
          <line x1="10%" y1="20%" x2="30%" y2="60%" stroke="url(#line-gradient)" strokeWidth="1" />
          <line x1="20%" y1="80%" x2="40%" y2="40%" stroke="url(#line-gradient)" strokeWidth="1" />
          <line x1="15%" y1="50%" x2="35%" y2="30%" stroke="url(#line-gradient)" strokeWidth="1" />
          <line x1="25%" y1="70%" x2="45%" y2="50%" stroke="url(#line-gradient)" strokeWidth="1" />
          <line x1="30%" y1="20%" x2="50%" y2="70%" stroke="url(#line-gradient)" strokeWidth="1" />
          
          {/* Glowing nodes */}
          <circle cx="10%" cy="20%" r="4" fill="#3b82f6" opacity="0.6">
            <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2s" repeatCount="indefinite" />
          </circle>
          <circle cx="20%" cy="80%" r="3" fill="#7c3aed" opacity="0.6">
            <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3s" repeatCount="indefinite" />
          </circle>
          <circle cx="30%" cy="60%" r="5" fill="#06b6d4" opacity="0.6">
            <animate attributeName="opacity" values="0.4;0.8;0.4" dur="2.5s" repeatCount="indefinite" />
          </circle>
          <circle cx="40%" cy="40%" r="4" fill="#8b5cf6" opacity="0.6">
            <animate attributeName="opacity" values="0.4;0.8;0.4" dur="3.5s" repeatCount="indefinite" />
          </circle>
        </svg>
      </div>

      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative z-10 items-center justify-center p-12">
        <div className="max-w-lg">
          <h1 className="text-6xl font-bold text-white mb-4 leading-tight">
            Advanced RAG<br />System
          </h1>
          <p className="text-xl text-zinc-300 mb-12">
            Intelligent Knowledge Discovery from Excel Datasets
          </p>
          
          <div className="space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-3 h-3 rounded-full bg-blue-400 mt-1.5 flex-shrink-0">
                <div className="w-3 h-3 rounded-full bg-blue-400 animate-ping absolute"></div>
              </div>
              <p className="text-zinc-300 text-lg">Vector-based retrieval with explainable results</p>
            </div>
            
            <div className="flex items-start gap-4">
              <div className="w-3 h-3 rounded-full bg-purple-400 mt-1.5 flex-shrink-0">
                <div className="w-3 h-3 rounded-full bg-purple-400 animate-ping absolute"></div>
              </div>
              <p className="text-zinc-300 text-lg">Advanced transformer embeddings</p>
            </div>
            
            <div className="flex items-start gap-4">
              <div className="w-3 h-3 rounded-full bg-cyan-400 mt-1.5 flex-shrink-0">
                <div className="w-3 h-3 rounded-full bg-cyan-400 animate-ping absolute"></div>
              </div>
              <p className="text-zinc-300 text-lg">Real-time performance monitoring</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 relative z-10">
        <div className="w-full max-w-md">
          {/* Glass Card */}
          <div className="bg-zinc-900/40 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">
                {isLogin ? 'Welcome Back' : 'Create Account'}
              </h2>
              <p className="text-zinc-400">
                {isLogin ? 'Sign in to access your RAG dashboard' : 'Join us to start querying your data'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              {!isLogin && (
                <div>
                  <label className="text-sm font-medium text-zinc-300 block mb-2">Name</label>
                  <Input
                    data-testid="register-name-input"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="bg-zinc-800/50 border-zinc-700 text-white placeholder:text-zinc-500 h-12"
                    placeholder="John Doe"
                    required={!isLogin}
                  />
                </div>
              )}

              <div>
                <label className="text-sm font-medium text-zinc-300 block mb-2">Email</label>
                <Input
                  data-testid="login-email-input"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-zinc-800/50 border-zinc-700 text-white placeholder:text-zinc-500 h-12"
                  placeholder="you@example.com"
                  required
                />
              </div>

              <div>
                <label className="text-sm font-medium text-zinc-300 block mb-2">Password</label>
                <div className="relative">
                  <Input
                    data-testid="login-password-input"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="bg-zinc-800/50 border-zinc-700 text-white placeholder:text-zinc-500 h-12 pr-10"
                    placeholder="••••••••"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-300"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              <Button
                data-testid="login-submit-button"
                type="submit"
                className="w-full h-12 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-700 hover:to-violet-700 text-white font-medium text-base shadow-lg shadow-violet-500/25"
                disabled={loading}
              >
                {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
              </Button>
            </form>

            <div className="mt-6 text-center">
              <button
                data-testid="toggle-auth-mode"
                onClick={() => setIsLogin(!isLogin)}
                className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
              >
                {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Sign in'}
              </button>
            </div>
          </div>

          {/* Mobile Branding */}
          <div className="lg:hidden mt-8 text-center">
            <p className="text-zinc-500 text-sm">
              Advanced RAG System - Intelligent Knowledge Discovery
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
