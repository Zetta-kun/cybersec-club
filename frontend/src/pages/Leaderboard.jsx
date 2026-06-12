import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import Loading from '../components/common/Loading';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/leaderboard/')
            .then(res => setLeaderboard(res.data.leaderboard || []))
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    const getBadge = (rank) => {
        if (rank === 1) return '🥇';
        if (rank === 2) return '🥈';
        if (rank === 3) return '🥉';
        return '#' + rank;
    };

    if (loading) return <Loading message='Leaderboard yuklenir...' />;

    return (
        <div className='space-y-6 fade-in'>
            <div className='text-center'>
                <h1 className='text-3xl font-bold'>🏆 <span className='cyber-gradient-text'>Leaderboard</span></h1>
                <p className='text-gray-400 mt-2'>En yaxshi kiber tehlukesizlik mutexessisleri</p>
            </div>
            
            <div className='cyber-card overflow-x-auto'>
                <table className='w-full border-collapse'>
                    <thead>
                        <tr className='border-b border-gray-700'>
                            <th className='px-4 py-3 text-left text-gray-400'>#</th>
                            <th className='px-4 py-3 text-left text-gray-400'>Istifadeci</th>
                            <th className='px-4 py-3 text-right text-gray-400'>Rating</th>
                            <th className='px-4 py-3 text-right text-gray-400'>Heller</th>
                            <th className='px-4 py-3 text-right text-gray-400'>Xal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leaderboard.map((entry) => (
                            <tr key={entry.user_id} className='border-b border-gray-700/50 hover:bg-gray-800/50'>
                                <td className='px-4 py-3 text-lg font-bold'>{getBadge(entry.rank)}</td>
                                <td className='px-4 py-3'>
                                    <div className='flex items-center gap-2'>
                                        <div className='w-8 h-8 rounded-full bg-cyber-500 flex items-center justify-center text-white font-bold text-sm'>
                                            {entry.username[0].toUpperCase()}
                                        </div>
                                        <div>
                                            <span className='font-medium' style={{ color: entry.rank_color }}>
                                                {entry.username}
                                            </span>
                                            <span className='text-xs text-gray-500 ml-2'>{entry.rank_name}</span>
                                        </div>
                                    </div>
                                </td>
                                <td className='px-4 py-3 text-right font-mono font-bold text-cyber-400'>{entry.rating}</td>
                                <td className='px-4 py-3 text-right text-gray-300'>{entry.total_solved}</td>
                                <td className='px-4 py-3 text-right text-gray-300'>{entry.total_points}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Leaderboard;