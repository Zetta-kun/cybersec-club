import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import Loading from '../components/common/Loading';

const ChallengeDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [challenge, setChallenge] = useState(null);
    const [loading, setLoading] = useState(true);
    const [flag, setFlag] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState(null);

    const loadChallenge = async () => {
        try {
            setLoading(true);
            const res = await api.get('/challenges/' + id);
            setChallenge(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { loadChallenge(); }, [id]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!flag.trim()) return;
        setSubmitting(true);
        setResult(null);
        try {
            const res = await api.post('/challenges/solve', { challenge_id: id, flag });
            setResult(res.data);
            if (res.data.status === 'correct') {
                setFlag('');
                setTimeout(() => loadChallenge(), 500);
            }
        } catch (err) {
            setResult({ status: 'error', message: 'Xeta bash verdi' });
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <Loading message='Challenge yuklenir...' />;
    if (!challenge) return <div className='text-center py-20 text-gray-400'>Challenge tapilmadi</div>;

    return (
        <div className='max-w-4xl mx-auto space-y-6 fade-in'>
            <button onClick={() => navigate(-1)} className='text-cyber-400 hover:text-cyber-300 bg-transparent border-none cursor-pointer text-lg'>← Geri</button>
            
            <div className='cyber-card'>
                <div className='flex items-start justify-between mb-4'>
                    <div>
                        <h1 className='text-2xl font-bold text-white mb-2'>{challenge.title}</h1>
                        <div className='flex items-center gap-3'>
                            <span className='cyber-badge bg-cyber-500/20 text-cyber-400'>{challenge.category}</span>
                            <span className='cyber-badge bg-gray-500/20 text-gray-400'>{challenge.difficulty}</span>
                        </div>
                    </div>
                    <div className='text-right'>
                        <div className='text-3xl font-bold cyber-gradient-text'>{challenge.current_points}</div>
                        <div className='text-sm text-gray-400'>XP</div>
                    </div>
                </div>
                
                <p className='text-gray-300 whitespace-pre-wrap leading-relaxed mb-4'>{challenge.description}</p>
                
                <div className='flex items-center gap-6 text-sm text-gray-400'>
                    <span>👥 {challenge.total_solves} hell</span>
                    <span>🚩 {challenge.total_attempts} cehd</span>
                </div>
            </div>

            {!challenge.is_solved ? (
                <div className='cyber-card'>
                    <h2 className='text-lg font-semibold text-white mb-4'>Flag Gonder</h2>
                    
                    {result && (
                        <div className={'mb-4 p-3 rounded-lg flex items-center gap-2 ' + 
                            (result.status === 'correct' 
                                ? 'bg-green-500/10 border border-green-500/30 text-green-400' 
                                : 'bg-red-500/10 border border-red-500/30 text-red-400')}>
                            <span>{result.status === 'correct' ? '✅' : '❌'}</span>
                            <span>{result.message}</span>
                        </div>
                    )}
                    
                    <form onSubmit={handleSubmit} className='flex gap-3'>
                        <input 
                            type='text' 
                            value={flag} 
                            onChange={(e) => setFlag(e.target.value)} 
                            className='cyber-input flex-grow' 
                            placeholder='CTF{...}' 
                            disabled={submitting} 
                        />
                        <button type='submit' disabled={submitting} className='cyber-btn-primary whitespace-nowrap'>
                            {submitting ? 'Gonderilir...' : 'Gonder'}
                        </button>
                    </form>
                </div>
            ) : (
                <div className='cyber-card bg-green-500/5 border-green-500/30'>
                    <div className='flex items-center gap-3'>
                        <span className='text-3xl'>✅</span>
                        <div>
                            <h2 className='text-xl font-bold text-green-400'>Hell Edildi!</h2>
                            <p className='text-gray-400'>Bu challenge-i ugurla hell etdiniz!</p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ChallengeDetail;