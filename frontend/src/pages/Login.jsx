import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const res = await api.post('/auth/login', { username, password });
            localStorage.setItem('access_token', res.data.access_token);
            localStorage.setItem('refresh_token', res.data.refresh_token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            navigate('/');
        } catch (err) {
            setError(err.response?.data?.detail || 'Giriş uğursuz oldu. İstifadəçi adı və ya şifrə yanlışdır.');
        } finally {
            setLoading(false);
        }
    };

    return (<div className='min-h-[80vh] flex items-center justify-center px-4'><div className='w-full max-w-md'><div className='text-center mb-8'><span className='text-5xl mb-4 block'>🛡️</span><h1 className='text-3xl font-bold cyber-gradient-text mb-2'>Xoş Gəldiniz</h1><p className='text-gray-400'>CyberSec Club-a daxil olun</p></div><div className='cyber-card'>{error && <div className='mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm'>{error}</div>}<form onSubmit={handleSubmit} className='space-y-4'><div><label className='block text-sm font-medium text-gray-300 mb-2'>İstifadəçi adı</label><input type='text' value={username} onChange={(e) => setUsername(e.target.value)} className='cyber-input' placeholder='admin' required disabled={loading} /></div><div><label className='block text-sm font-medium text-gray-300 mb-2'>Şifrə</label><input type='password' value={password} onChange={(e) => setPassword(e.target.value)} className='cyber-input' placeholder='••••••••' required disabled={loading} /></div><button type='submit' disabled={loading} className='cyber-btn-primary w-full flex items-center justify-center gap-2'>{loading ? <><span className='w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin'></span> Daxil olunur...</> : 'Daxil Ol'}</button></form><div className='mt-6 text-center'><p className='text-gray-400 text-sm'>Hesabınız yoxdur? <Link to='/register' className='text-cyber-400 hover:text-cyber-300 font-medium'>Qeydiyyatdan keçin</Link></p></div><div className='mt-6 p-4 bg-gray-800/50 rounded-lg'><p className='text-xs text-gray-500 mb-2'>Demo hesablar:</p><p className='text-xs text-gray-400 font-mono'>Admin: admin / Admin123!@#</p><p className='text-xs text-gray-400 font-mono'>Moderator: moderator / Mod123!@#</p></div></div></div></div>);
};

export default Login;
