import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Challenges from './pages/Challenges';
import ChallengeDetail from './pages/ChallengeDetail';
import Leaderboard from './pages/Leaderboard';
import Profile from './pages/Profile';
import AdminDashboard from './pages/admin/AdminDashboard';
import Wishlist from './pages/Wishlist';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<Layout />}>
                    <Route index element={<Home />} />
                    <Route path='login' element={<Login />} />
                    <Route path='register' element={<Register />} />
                    <Route path='challenges' element={<Challenges />} />
                    <Route path='challenges/:id' element={<ChallengeDetail />} />
                    <Route path='leaderboard' element={<Leaderboard />} />
                    <Route path='profile' element={<Profile />} />
                    <Route path='wishlist' element={<Wishlist />} />
                    <Route path='admin' element={<AdminDashboard />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;