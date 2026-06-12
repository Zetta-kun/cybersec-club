import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';

const Layout = () => {
    const navigate = useNavigate();
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isAuth = !!localStorage.getItem('access_token');
    const isAdmin = user && (user.role === 'admin' || user.role === 'super_admin');
    
    const logout = () => { localStorage.clear(); navigate('/'); };
    
    return (
        <div className='min-h-screen flex flex-col'>
            <nav className='bg-gray-900/95 backdrop-blur-md border-b border-gray-700/50 sticky top-0 z-50'>
                <div className='max-w-7xl mx-auto px-4 flex items-center justify-between h-16'>
                    <Link to='/' className='flex items-center space-x-2 text-white no-underline'>
                        <span className='text-2xl'>🛡️</span><span className='text-xl font-bold cyber-gradient-text'>CyberSec Club</span>
                    </Link>
                    <div className='hidden md:flex items-center space-x-4'>
                        <Link to='/' className='text-gray-300 hover:text-white px-3 py-2 rounded-lg transition-colors no-underline'>Ana Sehife</Link>
                        <Link to='/challenges' className='text-gray-300 hover:text-white px-3 py-2 rounded-lg transition-colors no-underline'>Suallar</Link>
                        <Link to='/leaderboard' className='text-gray-300 hover:text-white px-3 py-2 rounded-lg transition-colors no-underline'>Reytinq</Link>
                        <Link to='/wishlist' className='text-gray-300 hover:text-white px-3 py-2 rounded-lg transition-colors no-underline'>💡 Istekler</Link>
                        {isAuth ? (<>
                            <Link to='/profile' className='text-gray-300 hover:text-white px-3 py-2 rounded-lg transition-colors no-underline'>{user?.username} ({user?.rating} ELO)</Link>
                            {isAdmin && <Link to='/admin' className='text-yellow-400 hover:text-yellow-300 px-3 py-2 rounded-lg transition-colors no-underline font-semibold'>⚙️ Admin</Link>}
                            <button onClick={logout} className='text-red-400 hover:text-red-300 px-3 py-2 rounded-lg transition-colors bg-transparent border-none cursor-pointer'>Çıxış</button>
                        </>) : (<>
                            <Link to='/login' className='cyber-btn-primary text-sm py-2 px-4 no-underline'>Daxil Ol</Link>
                            <Link to='/register' className='border border-cyber-500 text-cyber-400 hover:bg-cyber-500/10 text-sm py-2 px-4 rounded-lg transition-colors no-underline'>Qeydiyyat</Link>
                        </>)}
                    </div>
                </div>
            </nav>
            <main className='flex-grow max-w-7xl mx-auto px-4 py-8 w-full'><Outlet /></main>
            <footer className='bg-gray-900/80 border-t border-gray-700/50 py-6 text-center text-gray-400 text-sm'><p>© 2024 CyberSec Club. Butun huquqlar qorunur.</p></footer>
        </div>
    );
};

export default Layout;