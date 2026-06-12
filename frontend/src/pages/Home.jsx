import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    const isAuth = !!localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');

    const stats = [
        { label: 'Aktiv İstifadəçi', value: '100+' },
        { label: 'CTF Sualları', value: '50+' },
        { label: 'Kateqoriya', value: '10' },
        { label: 'Ən Yüksək Rating', value: '3000' }
    ];

    const features = [
        { icon: '🏆', title: 'CTF Sualları', desc: '10 fərqli kateqoriyada, 5 çətinlik səviyyəsində kiber təhlükəsizlik sualları', link: '/challenges' },
        { icon: '📊', title: 'Rating Sistemi', desc: 'Codeforces tipli ELO rating sistemi ilə öz səviyyənizi ölçün', link: '/leaderboard' },
        { icon: '👥', title: 'Komanda', desc: 'Komanda yaradın, birlikdə yarışın və biliklərinizi paylaşın', link: '/teams' },
        { icon: '📈', title: 'Statistika', desc: 'Ətraflı statistika və analitika ilə inkişafınızı izləyin', link: '/profile' }
    ];

    return (<div className='space-y-16 fade-in'>
        <section className='text-center py-12'>
            <div className='max-w-4xl mx-auto'>
                <div className='text-6xl mb-6'>🛡️</div>
                <h1 className='text-5xl md:text-6xl font-bold mb-4'><span className='cyber-gradient-text'>CyberSec Club</span></h1>
                <p className='text-xl text-gray-300 mb-8'>Kiber Təhlükəsizlik üzrə peşəkar CTF platforması. Öz bacarıqlarınızı sınayın, yarışın və ən yaxşılar sırasında olun!</p>
                {isAuth ? (<div className='space-y-4'><div className='cyber-card inline-block'><div className='flex items-center gap-4'><div className='w-16 h-16 rounded-full bg-cyber-500 flex items-center justify-center text-white font-bold text-2xl'>{user?.username?.[0]?.toUpperCase()}</div><div className='text-left'><h3 className='text-xl font-bold text-white'>{user?.username}</h3><p className='text-cyber-400 font-mono text-lg'>{user?.rating} ELO</p></div></div></div><Link to='/challenges' className='cyber-btn-primary text-lg inline-block no-underline'>Suallara Başla</Link></div>) : (<div className='flex gap-4 justify-center'><Link to='/register' className='cyber-btn-primary text-lg no-underline'>Qeydiyyatdan Keç</Link><Link to='/login' className='border border-cyber-500 text-cyber-400 hover:bg-cyber-500/10 text-lg py-3 px-6 rounded-lg transition-colors no-underline'>Daxil Ol</Link></div>)}
            </div>
        </section>
        <section className='grid grid-cols-2 md:grid-cols-4 gap-4'>
            {stats.map((s, i) => (<div key={i} className='cyber-card text-center'><div className='text-3xl font-bold cyber-gradient-text mb-1'>{s.value}</div><div className='text-gray-400 text-sm'>{s.label}</div></div>))}
        </section>
        <section>
            <h2 className='text-3xl font-bold text-center mb-10'>Nə <span className='cyber-gradient-text'>Təklif</span> Edirik?</h2>
            <div className='grid md:grid-cols-2 lg:grid-cols-4 gap-6'>
                {features.map((f, i) => (<Link key={i} to={f.link} className='cyber-card group hover:scale-105 text-center block text-white no-underline'><div className='text-4xl mb-4'>{f.icon}</div><h3 className='text-lg font-semibold text-white mb-2 group-hover:text-cyber-400 transition-colors'>{f.title}</h3><p className='text-gray-400 text-sm'>{f.desc}</p></Link>))}
            </div>
        </section>
    </div>);
};

export default Home;
