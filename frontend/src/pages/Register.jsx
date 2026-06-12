import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const Register = () => {
    const [formData, setFormData] = useState({ username: '', email: '', password: '', confirmPassword: '', full_name: '' });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); setSuccess('');
        if (formData.password !== formData.confirmPassword) { setError('Şifrələr uyğun gəlmir'); return; }
        if (formData.password.length < 8) { setError('Şifrə minimum 8 simvol olmalıdır'); return; }
        setLoading(true);
        try {
            const { confirmPassword, ...userData } = formData;
            await api.post('/auth/register', userData);
            setSuccess('Qeydiyyat uğurla tamamlandı! Daxil ola bilərsiniz.');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Qeydiyyat uğursuz oldu. Məlumatları yoxlayın.');
        } finally {
            setLoading(false);
        }
    };

    return (<div className='min-h-[80vh] flex items-center justify-center px-4 py-8'><div className='w-full max-w-md'><div className='text-center mb-8'><span className='text-5xl mb-4 block'>🚀</span><h1 className='text-3xl font-bold cyber-gradient-text mb-2'>Qeydiyyat</h1><p className='text-gray-400'>CyberSec Club-a qoşulun</p></div><div className='cyber-card'>{error && <div className='mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm'>{error}</div>}{success && <div className='mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded-lg text-green-400 text-sm'>{success}</div>}<form onSubmit={handleSubmit} className='space-y-4'><div><label className='block text-sm font-medium text-gray-300 mb-2'>Ad Soyad</label><input type='text' name='full_name' value={formData.full_name} onChange={handleChange} className='cyber-input' placeholder='Ali Aliyev' required disabled={loading} /></div><div><label className='block text-sm font-medium text-gray-300 mb-2'>İstifadəçi adı</label><input type='text' name='username' value={formData.username} onChange={handleChange} className='cyber-input' placeholder='aliyev123' required minLength={3} disabled={loading} /></div><div><label className='block text-sm font-medium text-gray-300 mb-2'>Email</label><input type='email' name='email' value={formData.email} onChange={handleChange} className='cyber-input' placeholder='ali@example.com' required disabled={loading} /></div><div><label className='block text-sm font-medium text-gray-300 mb-2'>Şifrə</label><input type='password' name='password' value={formData.password} onChange={handleChange} className='cyber-input' placeholder='Minimum 8 simvol' required minLength={8} disabled={loading} /></div><div><label className='block text-sm font-medium text-gray-300 mb-2'>Şifrə Təkrarı</label><input type='password' name='confirmPassword' value={formData.confirmPassword} onChange={handleChange} className='cyber-input' placeholder='Şifrəni təkrarlayın' required disabled={loading} /></div><button type='submit' disabled={loading} className='cyber-btn-primary w-full flex items-center justify-center gap-2'>{loading ? <><span className='w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin'></span> Qeydiyyat...</> : 'Qeydiyyatdan Keç'}</button></form><div className='mt-6 text-center'><p className='text-gray-400 text-sm'>Artıq hesabınız var? <Link to='/login' className='text-cyber-400 hover:text-cyber-300 font-medium'>Daxil olun</Link></p></div></div></div></div>);
};

export default Register;
