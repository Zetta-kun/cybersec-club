import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { FiShield, FiUsers, FiFlag, FiPlus, FiTrash2, FiCalendar, FiCheckSquare, FiMessageSquare, FiBarChart2, FiStar } from 'react-icons/fi';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('challenges');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [stats, setStats] = useState(null);
    const [wishlist, setWishlist] = useState([]);
    
    const [formData, setFormData] = useState({title: '', description: '', category: 'web_exploitation', difficulty: 'easy', base_points: 100, flag: '', tags: ''});
    const [contestData, setContestData] = useState({title: '', description: '', start_time: '', end_time: '', challenge_ids: ''});
    
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isAdmin = user && (user.role === 'admin' || user.role === 'super_admin');

    useEffect(() => {
        if (isAdmin && activeTab === 'stats') loadStats();
        if (isAdmin && activeTab === 'wishlist') loadWishlist();
    }, [activeTab]);

    const loadStats = async () => {
        try { const res = await api.get('/admin/dashboard'); setStats(res.data); } catch (err) {}
    };

    const loadWishlist = async () => {
        try { const res = await api.get('/wishlist/'); setWishlist(res.data.wishlist || []); } catch (err) {}
    };

    if (!isAdmin) return <div className='text-center py-20'><h1 className='text-2xl text-red-400'>❌ Admin icazesi teleb olunur</h1></div>;

    const handleCreateChallenge = async (e) => {
        e.preventDefault(); setLoading(true); setMessage('');
        try {
            const res = await api.post('/admin/challenges', {...formData, base_points: parseInt(formData.base_points), tags: formData.tags.split(',').map(t => t.trim()).filter(t => t)});
            setMessage('✅ ' + res.data.message);
            setFormData({title: '', description: '', category: 'web_exploitation', difficulty: 'easy', base_points: 100, flag: '', tags: ''});
        } catch (err) { setMessage('❌ Xeta: ' + (err.response?.data?.detail || '')); }
        finally { setLoading(false); }
    };

    const handleCreateContest = async (e) => {
        e.preventDefault(); setLoading(true); setMessage('');
        try {
            const res = await api.post('/admin/competitions', {...contestData, challenge_ids: contestData.challenge_ids.split(',').map(t => t.trim()).filter(t => t)});
            setMessage('✅ ' + res.data.message);
            setContestData({title: '', description: '', start_time: '', end_time: '', challenge_ids: ''});
        } catch (err) { setMessage('❌ Xeta'); }
        finally { setLoading(false); }
    };

    const handleWishlistStatus = async (itemId, status) => {
        try { await api.put('/admin/wishlist/' + itemId + '?status=' + status); loadWishlist(); } catch (err) {}
    };

    return (
        <div className='space-y-6 fade-in'>
            <h1 className='text-3xl font-bold'><FiShield className='inline-block mr-2' /><span className='cyber-gradient-text'>Admin Panel</span></h1>

            <div className='flex gap-2 border-b border-gray-700 overflow-x-auto'>
                {[
                    {id: 'challenges', label: 'Suallar', icon: '🏆'},
                    {id: 'contests', label: 'Yarislar', icon: '📅'},
                    {id: 'wishlist', label: 'Istekler', icon: '💡'},
                    {id: 'stats', label: 'Statistika', icon: '📊'},
                ].map(tab => (
                    <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                        className={'px-4 py-2 rounded-t-lg transition-colors whitespace-nowrap ' + (activeTab === tab.id ? 'bg-cyber-500/20 text-cyber-400 border-b-2 border-cyber-500' : 'text-gray-400 hover:text-white')}>
                        {tab.icon} {tab.label}
                    </button>
                ))}
            </div>

            {message && <div className={'p-3 rounded-lg ' + (message.startsWith('✅') ? 'bg-green-500/10 border border-green-500/30 text-green-400' : 'bg-red-500/10 border border-red-500/30 text-red-400')}>{message}</div>}

            {activeTab === 'challenges' && (
                <div className='cyber-card'>
                    <h2 className='text-xl font-bold text-white mb-4'>🏆 Yeni Sual Elave Et</h2>
                    <form onSubmit={handleCreateChallenge} className='space-y-4'>
                        <div className='grid md:grid-cols-2 gap-4'>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Basliq</label>
                                <input type='text' value={formData.title} onChange={(e) => setFormData({...formData, title: e.target.value})} className='cyber-input' placeholder='SQL Injection Advanced' required />
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Kateqoriya</label>
                                <select value={formData.category} onChange={(e) => setFormData({...formData, category: e.target.value})} className='cyber-input'>
                                    <option value='web_exploitation'>🌐 Web</option>
                                    <option value='cryptography'>🔐 Kripto</option>
                                    <option value='forensics'>🔍 Forensics</option>
                                    <option value='reverse_engineering'>⚙️ Reverse</option>
                                    <option value='binary_exploitation'>💻 PWN</option>
                                    <option value='osint'>🕵️ OSINT</option>
                                    <option value='misc'>🎯 Misc</option>
                                </select>
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Cetinlik</label>
                                <select value={formData.difficulty} onChange={(e) => setFormData({...formData, difficulty: e.target.value})} className='cyber-input'>
                                    <option value='easy'>🟢 Asan</option>
                                    <option value='medium'>🟡 Orta</option>
                                    <option value='hard'>🔴 Çetin</option>
                                    <option value='expert'>🟣 Ekspert</option>
                                </select>
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Xal</label>
                                <input type='number' value={formData.base_points} onChange={(e) => setFormData({...formData, base_points: e.target.value})} className='cyber-input' min='50' max='1000' />
                            </div>
                        </div>
                        <div>
                            <label className='block text-sm text-gray-300 mb-2'>Aciqlama</label>
                            <textarea value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} className='cyber-input' rows='3' required />
                        </div>
                        <div>
                            <label className='block text-sm text-gray-300 mb-2'>Flag (CTF formatinda)</label>
                            <input type='text' value={formData.flag} onChange={(e) => setFormData({...formData, flag: e.target.value})} className='cyber-input' placeholder='CTF{flag_buraya}' required />
                        </div>
                        <div>
                            <label className='block text-sm text-gray-300 mb-2'>Taglar (vergul ile)</label>
                            <input type='text' value={formData.tags} onChange={(e) => setFormData({...formData, tags: e.target.value})} className='cyber-input' placeholder='web, sql' />
                        </div>
                        <button type='submit' disabled={loading} className='cyber-btn-primary w-full'>{loading ? 'Elave edilir...' : '✅ Sual Elave Et'}</button>
                    </form>
                </div>
            )}

            {activeTab === 'contests' && (
                <div className='cyber-card'>
                    <h2 className='text-xl font-bold text-white mb-4'>📅 Yeni Yarish Yarad</h2>
                    <form onSubmit={handleCreateContest} className='space-y-4'>
                        <div className='grid md:grid-cols-2 gap-4'>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Yarish Adi</label>
                                <input type='text' value={contestData.title} onChange={(e) => setContestData({...contestData, title: e.target.value})} className='cyber-input' placeholder='Heftelik CTF Yarishi' required />
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Sual ID-leri (vergul ile)</label>
                                <input type='text' value={contestData.challenge_ids} onChange={(e) => setContestData({...contestData, challenge_ids: e.target.value})} className='cyber-input' placeholder='1,2,3' />
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Baslama Vaxti</label>
                                <input type='datetime-local' value={contestData.start_time} onChange={(e) => setContestData({...contestData, start_time: e.target.value})} className='cyber-input' />
                            </div>
                            <div>
                                <label className='block text-sm text-gray-300 mb-2'>Bitme Vaxti</label>
                                <input type='datetime-local' value={contestData.end_time} onChange={(e) => setContestData({...contestData, end_time: e.target.value})} className='cyber-input' />
                            </div>
                        </div>
                        <div>
                            <label className='block text-sm text-gray-300 mb-2'>Aciqlama</label>
                            <textarea value={contestData.description} onChange={(e) => setContestData({...contestData, description: e.target.value})} className='cyber-input' rows='3' />
                        </div>
                        <button type='submit' disabled={loading} className='cyber-btn-primary w-full'>{loading ? 'Yaradilir...' : '🏆 Yarish Yarad'}</button>
                    </form>
                </div>
            )}

            {activeTab === 'wishlist' && (
                <div className='cyber-card'>
                    <h2 className='text-xl font-bold text-white mb-4'>💡 Istek Qutusu</h2>
                    {wishlist.length === 0 ? <p className='text-gray-400'>Hec bir istek yoxdur</p> : (
                        <div className='space-y-3'>
                            {wishlist.map(item => (
                                <div key={item.id} className='p-4 bg-gray-800/50 rounded-lg flex items-center justify-between'>
                                    <div>
                                        <h3 className='text-white font-medium'>{item.title}</h3>
                                        <p className='text-gray-400 text-sm'>{item.description || 'Aciqlama yoxdur'}</p>
                                        <div className='flex items-center gap-3 mt-1 text-xs'>
                                            <span className='text-cyber-400'>{item.category}</span>
                                            <span className='text-yellow-400'>⭐ {item.votes} ses</span>
                                            <span className='text-gray-500'>@{item.username}</span>
                                        </div>
                                    </div>
                                    <div className='flex gap-2'>
                                        <button onClick={() => handleWishlistStatus(item.id, 'approved')} className='px-3 py-1 bg-green-600/20 text-green-400 rounded text-sm hover:bg-green-600/40'>✅ Tesdiqle</button>
                                        <button onClick={() => handleWishlistStatus(item.id, 'rejected')} className='px-3 py-1 bg-red-600/20 text-red-400 rounded text-sm hover:bg-red-600/40'>❌ Redd et</button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {activeTab === 'stats' && stats && (
                <div className='space-y-6'>
                    <div className='grid md:grid-cols-4 gap-4'>
                        <div className='cyber-card text-center'><div className='text-3xl font-bold text-cyber-400'>{stats.total_users}</div><div className='text-gray-400 text-sm mt-1'>Istifadeci</div></div>
                        <div className='cyber-card text-center'><div className='text-3xl font-bold text-green-400'>{stats.total_challenges}</div><div className='text-gray-400 text-sm mt-1'>Suallar</div></div>
                        <div className='cyber-card text-center'><div className='text-3xl font-bold text-yellow-400'>{stats.correct_submissions}</div><div className='text-gray-400 text-sm mt-1'>Hell Edilib</div></div>
                        <div className='cyber-card text-center'><div className='text-3xl font-bold text-purple-400'>{stats.weekly_solves}</div><div className='text-gray-400 text-sm mt-1'>Bu Hefte</div></div>
                    </div>
                    
                    <div className='cyber-card'>
                        <h3 className='text-lg font-bold text-white mb-4'>Kateqoriya Statistikasi</h3>
                        <div className='space-y-2'>
                            {(stats.category_distribution || []).map(cat => (
                                <div key={cat.category} className='flex items-center justify-between'>
                                    <span className='text-gray-300'>{cat.category}</span>
                                    <span className='text-cyber-400'>{cat.solves}/{cat.total} hell</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className='cyber-card'>
                        <h3 className='text-lg font-bold text-white mb-4'>Top 10 Istifadeci</h3>
                        <div className='space-y-2'>
                            {(stats.top_users || []).slice(0, 10).map((u, i) => (
                                <div key={i} className='flex items-center justify-between'>
                                    <span className='text-gray-300'>#{i+1} {u.username}</span>
                                    <span className='text-cyber-400'>{u.rating} ELO ({u.solved} hell)</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdminDashboard;