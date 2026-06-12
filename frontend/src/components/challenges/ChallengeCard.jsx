import React from 'react';
import { Link } from 'react-router-dom';

const icons = { web_exploitation: '🌐', cryptography: '🔐', forensics: '🔍', reverse_engineering: '⚙️', binary_exploitation: '💻', osint: '🕵️', misc: '🎯' };

const ChallengeCard = ({ challenge }) => {
    return (
        <Link to={'/challenges/' + challenge.id} className='cyber-card hover:scale-[1.02] cursor-pointer group relative block text-white no-underline'>
            <div className='text-4xl mb-3'>{icons[challenge.category] || '🎯'}</div>
            <h3 className='text-lg font-semibold text-white mb-2 group-hover:text-cyber-400 transition-colors'>{challenge.title}</h3>
            <div className='flex items-center justify-between mb-3'>
                <span className='cyber-badge bg-cyber-500/20 text-cyber-400'>{challenge.difficulty}</span>
                <span className='text-cyber-400 font-bold'>{challenge.current_points} XP</span>
            </div>
            <div className='flex items-center justify-between text-sm text-gray-400'>
                <span>{challenge.total_solves} hell</span>
                <span className='capitalize'>{(challenge.category || '').replace(/_/g, ' ')}</span>
            </div>
            {challenge.is_solved && <div className='absolute top-3 right-3 text-green-400 text-xl'>✅</div>}
        </Link>
    );
};

export default ChallengeCard;