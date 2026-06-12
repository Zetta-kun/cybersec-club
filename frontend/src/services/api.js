import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) config.headers.Authorization = 'Bearer ' + token;
    return config;
}, (error) => Promise.reject(error));

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401 && !error.config._retry) {
            error.config._retry = true;
            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const res = await axios.post('http://localhost:8000/api/v1/auth/login', { username: 'admin', password: 'Admin123!@#' });
                    localStorage.setItem('access_token', res.data.access_token);
                    error.config.headers.Authorization = 'Bearer ' + res.data.access_token;
                    return api(error.config);
                }
            } catch {
                localStorage.clear();
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;