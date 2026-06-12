import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { FiMessageSquare, FiStar, FiPlus } from 'react-icons/fi';

const Wishlist = () => {
    const [wishlist, setWishlist] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({title: '', description: '', category: 'other'});
    const [showForm, setShowForm] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => { loadWishlist(); }, []);

    const loadWishlist = async () => {
        try {
            const res = await api.get('/wishlist/');
            setWishlist(res.data.wishlist || []);
        } catch (err) {} finally { setLoading(false); }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post('/wishlist/', formData);
            setMessage('✅ ' + res.data.message);
            setFormData({title: '', description: '', category: 'other'});
            setShowForm(false);
            loadWishlist();
        } catch (err) { setMessage('❌ Xeta bash verdi'); }
    };

    const handleVote = async (itemId) => {
        try {
            await api.post('/wishlist/' + itemId + '/vote');
            loadWishlist();
        } catch (err) {}
    };

    return (
        <div className='space-y-6 fade-in max-w-4xl mx-auto'>
            <div className='flex items-center justify-between'>
                <h1 className='text-3xl font-bold'><FiMessageSquare className='inline mr-2' /><span className='cyber-gradient-text'>Istek Qutusu</span></h1>
                <button onClick={() => setShowForm(!showForm)} className='cyber-btn-primary'><FiPlus className='inline mr-1' />Yeni Istek</button>
            </div>

            {message && <div className='p-3 rounded-lg bg-green-500/10 border border-green-500/30 text-green-400'>{message}</div>}

            {showForm && (
                <div className='cyber-card'>
                    <h2 className='text-lg font-bold text-white mb-4'>Istek Gonder</h2>
                    <form onSubmit={handleSubmit} className='space-y-4'>
                        <div><input type='text' value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})} className='cyber-input' placeholder='Istek basligi...' required /></div>
                        <div><textarea value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} className='cyber-input' rows='3' placeholder='Aciqlama (vacib deyil)' /></div>
                        <div className='flex gap-3'>
                            <button type='submit' className='cyber-btn-primary'>Gonder</button>
                            <button type='button' onClick={() => setShowForm(false)} className='text-gray-400 hover:text-white px-4 py-2'>Legv et</button>
                        </div>
                    </form>
                </div>
            )}

            <div className='space-y-3'>
                {wishlist.map(item => (
                    <div key={item.id} className='cyber-card'>
                        <div className='flex items-start justify-between'>
                            <div>
                                <h3 className='text-white font-semibold text-lg'>{item.title}</h3>
                                {item.description && <p className='text-gray-400 mt-1'>{item.description}</p>}
                                <div className='flex items-center gap-4 mt-2 text-sm'>
                                    <span className='cyber-badge bg-cyber-500/20 text-cyber-400'>{item.category}</span>
                                    <span className='text-gray-500'>@{item.username}</span>
                                    <span className={'cyber-badge ' + (item.status === 'approved' ? 'bg-green-500/20 text-green-400' : item.status === 'rejected' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400')}>
                                        {item.status === 'approved' ? '✅ Tesdiqlendi' : item.status === 'rejected' ? '❌ Redd edildi' : '⏳ Gozlemede'}
                                    </span>
                                </div>
                            </div>
                            <button onClick={() => handleVote(item.id)} className='flex items-center gap-1 text-yellow-400 hover:text-yellow-300 transition-colors bg-transparent border-none cursor-pointer'>
                                <FiStar /> {item.votes}
                            </button>
                        </div>
                    </div>
                ))}
                {wishlist.length === 0 && !loading && <p className='text-center text-gray-400 py-10'>Hec bir istek yoxdur. Ilk isteyi siz gonderin!</p>}
            </div>
        </div>
    );
};

export default Wishlist;