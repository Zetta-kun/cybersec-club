import React, { useState, useEffect } from 'react';
import api from '../services/api';
import Loading from '../components/common/Loading';

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/users/me').then(res => setProfile(res.data)).catch(err => console.error('Profil yüklənə bilmədi:', err)).finally(() => setLoading(false));
    }, []);

    if (loading) return <Loading message='Profil yüklənir...' />;
    if (!profile) return <div className='text-center py-20 text-gray-400'>Profil tapılmadı. Zəhmət olmasa daxil olun.</div>;

    return (<div className='max-w-4xl mx-auto space-y-6 fade-in'>
        <div className='cyber-card text-center'>
            <div className='w-24 h-24 rounded-full bg-gradient-to-br from-cyber-500 to-blue-600 flex items-center justify-center text-white font-bold text-4xl mx-auto mb-4'>{profile.username?.[0]?.toUpperCase()}</div>
            <h1 className='text-2xl font-bold text-white'>{profile.username}</h1>
            <p className='text-gray-400'>{profile.full_name}</p>
            <div className='mt-2'><span className='text-3xl font-bold font-mono cyber-gradient-text'>{profile.rating}</span><span className='text-gray-500 text-sm ml-2'>ELO</span></div>
            {profile.rank && <p className='text-sm mt-1' style={{ color: profile.rank_color }}>{profile.rank}</p>}
        </div>
        <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
            <div className='cyber-card text-center'><div className='text-2xl font-bold text-white'>{profile.total_solved || 0}</div><div className='text-sm text-gray-400'>Həll edilib</div></div>
            <div className='cyber-card text-center'><div className='text-2xl font-bold text-white'>{profile.total_points || 0}</div><div className='text-sm text-gray-400'>Ümumi Xal</div></div>
            <div className='cyber-card text-center'><div className='text-2xl font-bold text-white'>{profile.max_rating || 0}</div><div className='text-sm text-gray-400'>Max Rating</div></div>
            <div className='cyber-card text-center'><div className='text-2xl font-bold text-white'>{profile.consecutive_days || 0}</div><div className='text-sm text-gray-400'>Ardıcıl Gün</div></div>
        </div>
    </div>);
};

export default Profile;
