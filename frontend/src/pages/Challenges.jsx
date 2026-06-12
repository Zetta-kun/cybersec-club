import React, { useState, useEffect } from 'react';
import api from '../services/api';
import ChallengeCard from '../components/challenges/ChallengeCard';
import Loading from '../components/common/Loading';

const Challenges = () => {
    const [challenges, setChallenges] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [category, setCategory] = useState('');

    const loadChallenges = async () => {
        try {
            setLoading(true);
            setError(null);
            const params = {};
            if (category) params.category = category;
            const res = await api.get('/challenges/', { params });
            setChallenges(res.data.challenges || []);
        } catch (err) {
            console.error('Suallar yuklene bilmedi:', err);
            setError('Suallar yuklene bilmedi. Backend ishleyirmi?');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { loadChallenges(); }, [category]);

    if (loading) return <Loading message='Suallar yuklenir...' />;

    return (
        <div className='space-y-6 fade-in'>
            <h1 className='text-3xl font-bold'>CTF <span className='cyber-gradient-text'>Suallari</span></h1>
            
            {error && (
                <div className='p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400'>
                    {error}
                    <button onClick={loadChallenges} className='ml-4 underline'>Yeniden cehd et</button>
                </div>
            )}

            <div className='cyber-card'>
                <div className='grid md:grid-cols-3 gap-4'>
                    <select value={category} onChange={(e) => setCategory(e.target.value)} className='cyber-input'>
                        <option value=''>Butun kateqoriyalar</option>
                        <option value='web_exploitation'>🌐 Web Exploitation</option>
                        <option value='cryptography'>🔐 Cryptography</option>
                        <option value='forensics'>🔍 Forensics</option>
                        <option value='reverse_engineering'>⚙️ Reverse Engineering</option>
                        <option value='binary_exploitation'>💻 Binary Exploitation</option>
                        <option value='osint'>🕵️ OSINT</option>
                        <option value='misc'>🎯 Misc</option>
                    </select>
                </div>
            </div>

            <div className='grid md:grid-cols-2 lg:grid-cols-3 gap-4'>
                {challenges.map((c) => (
                    <ChallengeCard key={c.id} challenge={c} />
                ))}
            </div>

            {challenges.length === 0 && !error && (
                <div className='text-center py-20 text-gray-400'>
                    <p className='text-xl'>Hec bir sual tapilmadi</p>
                </div>
            )}
        </div>
    );
};

export default Challenges;